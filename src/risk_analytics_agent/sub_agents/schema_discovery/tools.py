"""Schema discovery tools for exploring Snowflake metadata."""

from __future__ import annotations

import json
import logging

from google.adk.tools import ToolContext

from risk_analytics_agent.snowflake_client import get_client

logger = logging.getLogger(__name__)


def list_databases(tool_context: ToolContext) -> dict:
    """List all accessible databases in Snowflake."""
    client = get_client()
    rows = client.execute("SHOW DATABASES")
    databases = [
        {
            "name": r["name"],
            "owner": r.get("owner", ""),
            "comment": r.get("comment", ""),
        }
        for r in rows
    ]

    metadata = tool_context.state.get("schema_metadata", {})
    metadata["databases"] = databases
    tool_context.state["schema_metadata"] = metadata

    return {"databases": databases, "count": len(databases)}


def list_schemas(database: str, tool_context: ToolContext) -> dict:
    """List all schemas in a given database.

    Args:
        database: Name of the database to list schemas for.
    """
    client = get_client()
    rows = client.execute(f"SHOW SCHEMAS IN DATABASE {database}")
    schemas = [
        {
            "name": r["name"],
            "database": database,
            "owner": r.get("owner", ""),
            "comment": r.get("comment", ""),
        }
        for r in rows
    ]

    metadata = tool_context.state.get("schema_metadata", {})
    metadata.setdefault("schemas", {})[database] = schemas
    tool_context.state["schema_metadata"] = metadata

    return {"schemas": schemas, "count": len(schemas)}


def list_tables(database: str, schema: str, tool_context: ToolContext) -> dict:
    """List all tables and views in a given schema.

    Args:
        database: Name of the database.
        schema: Name of the schema.
    """
    client = get_client()
    rows = client.execute(f"SHOW TABLES IN {database}.{schema}")
    tables = [
        {
            "name": r["name"],
            "database": database,
            "schema": schema,
            "kind": r.get("kind", "TABLE"),
            "rows": r.get("rows", 0),
            "comment": r.get("comment", ""),
        }
        for r in rows
    ]

    # Also get views
    view_rows = client.execute(f"SHOW VIEWS IN {database}.{schema}")
    views = [
        {
            "name": r["name"],
            "database": database,
            "schema": schema,
            "kind": "VIEW",
            "comment": r.get("comment", ""),
        }
        for r in view_rows
    ]

    all_objects = tables + views
    metadata = tool_context.state.get("schema_metadata", {})
    key = f"{database}.{schema}"
    metadata.setdefault("tables", {})[key] = all_objects
    tool_context.state["schema_metadata"] = metadata

    return {"tables": all_objects, "count": len(all_objects)}


def describe_table(
    database: str, schema: str, table: str, tool_context: ToolContext
) -> dict:
    """Describe the columns of a specific table.

    Args:
        database: Name of the database.
        schema: Name of the schema.
        table: Name of the table.
    """
    client = get_client()
    fqn = f"{database}.{schema}.{table}"
    rows = client.execute(f"DESCRIBE TABLE {fqn}")
    columns = [
        {
            "name": r["name"],
            "type": r["type"],
            "nullable": r.get("null?", "Y") == "Y",
            "default": r.get("default", None),
            "comment": r.get("comment", ""),
        }
        for r in rows
    ]

    metadata = tool_context.state.get("schema_metadata", {})
    metadata.setdefault("columns", {})[fqn] = columns
    tool_context.state["schema_metadata"] = metadata

    return {"table": fqn, "columns": columns, "column_count": len(columns)}


def sample_table(
    database: str,
    schema: str,
    table: str,
    tool_context: ToolContext,
    limit: int = 10,
) -> dict:
    """Retrieve a sample of rows from a table.

    Args:
        database: Name of the database.
        schema: Name of the schema.
        table: Name of the table.
        limit: Maximum number of rows to return (default 10).
    """
    client = get_client()
    fqn = f"{database}.{schema}.{table}"
    rows = client.execute(f"SELECT * FROM {fqn} LIMIT {int(limit)}")

    # Convert to JSON-serializable format
    sample = json.loads(json.dumps(rows, default=str))
    return {"table": fqn, "sample": sample, "row_count": len(sample)}


def search_columns(
    pattern: str, tool_context: ToolContext, database: str | None = None
) -> dict:
    """Search for columns matching a name pattern across schemas.

    Args:
        pattern: Column name pattern (SQL LIKE syntax, e.g. '%MLO%').
        database: Optional database to limit the search to.
    """
    client = get_client()
    sql = """
        SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
        FROM {db}INFORMATION_SCHEMA.COLUMNS
        WHERE COLUMN_NAME LIKE %(pattern)s
        ORDER BY TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
        LIMIT 200
    """.format(
        db=f"{database}." if database else ""
    )
    rows = client.execute(sql, {"pattern": pattern})
    matches = [
        {
            "database": r["TABLE_CATALOG"],
            "schema": r["TABLE_SCHEMA"],
            "table": r["TABLE_NAME"],
            "column": r["COLUMN_NAME"],
            "type": r["DATA_TYPE"],
        }
        for r in rows
    ]
    return {"pattern": pattern, "matches": matches, "count": len(matches)}
