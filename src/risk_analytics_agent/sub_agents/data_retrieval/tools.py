"""Data retrieval tools with SQL safety guards."""

from __future__ import annotations

import json
import logging
import re

from google.adk.tools import ToolContext

from risk_analytics_agent.snowflake_client import get_client

logger = logging.getLogger(__name__)

_FORBIDDEN_PATTERNS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|MERGE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


def _is_safe_sql(sql: str) -> tuple[bool, str]:
    """Check if SQL is safe (read-only)."""
    stripped = sql.strip().rstrip(";")
    # Remove comments
    cleaned = re.sub(r"--.*$", "", stripped, flags=re.MULTILINE)
    cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)

    match = _FORBIDDEN_PATTERNS.search(cleaned)
    if match:
        return False, f"Forbidden keyword detected: {match.group(0).upper()}"

    # Must start with SELECT, WITH, SHOW, DESCRIBE, or EXPLAIN
    first_word = cleaned.strip().split()[0].upper() if cleaned.strip() else ""
    allowed_starts = {"SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN", "DESC"}
    if first_word not in allowed_starts:
        return False, f"Query must start with SELECT/WITH/SHOW/DESCRIBE, got: {first_word}"

    return True, "OK"


def validate_sql(sql: str) -> dict:
    """Validate a SQL query for safety without executing it.

    Args:
        sql: The SQL query to validate.
    """
    is_safe, message = _is_safe_sql(sql)
    return {"valid": is_safe, "message": message, "sql": sql}


def execute_sql(
    sql: str, tool_context: ToolContext, row_limit: int = 50000
) -> dict:
    """Execute a read-only SQL query against Snowflake.

    Args:
        sql: The SQL query to execute. Must be a SELECT/WITH/SHOW/DESCRIBE statement.
        row_limit: Maximum number of rows to return (default 50000).
    """
    is_safe, message = _is_safe_sql(sql)
    if not is_safe:
        return {"error": message, "sql": sql, "row_count": 0}

    # Apply row limit if not already present
    stripped = sql.strip().rstrip(";")
    if "LIMIT" not in stripped.upper():
        sql = f"{stripped} LIMIT {int(row_limit)}"

    client = get_client()
    try:
        rows = client.execute(sql)
    except Exception as e:
        logger.error("SQL execution failed: %s", e)
        return {"error": str(e), "sql": sql, "row_count": 0}

    # Serialize for state storage
    result = json.loads(json.dumps(rows, default=str))

    tool_context.state["query_result"] = result
    tool_context.state["query_sql"] = sql

    # Track query history
    history = tool_context.state.get("query_history", [])
    history.append({"sql": sql, "row_count": len(result)})
    tool_context.state["query_history"] = history

    # Return summary (not full data) to the LLM
    preview = result[:5] if result else []
    columns = list(result[0].keys()) if result else []
    return {
        "row_count": len(result),
        "columns": columns,
        "preview": preview,
        "sql": sql,
        "note": "Full results stored in state['query_result']",
    }


def get_query_history(tool_context: ToolContext) -> dict:
    """Get the history of SQL queries executed in this session."""
    history = tool_context.state.get("query_history", [])
    return {"queries": history, "count": len(history)}
