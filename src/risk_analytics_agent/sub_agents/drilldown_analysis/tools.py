"""Drill-down analysis tools for hierarchical decomposition."""

from __future__ import annotations

import json
import logging

from google.adk.tools import ToolContext

from risk_analytics_agent.snowflake_client import get_client

logger = logging.getLogger(__name__)


def _run_drilldown_query(
    sql: str,
    group_col: str,
    metric_col: str,
    top_n: int,
    tool_context: ToolContext,
    level: str,
) -> dict:
    """Common logic for executing a drill-down GROUP BY query."""
    client = get_client()
    try:
        rows = client.execute(sql)
    except Exception as e:
        return {"error": str(e)}

    if not rows:
        return {"level": level, "contributors": [], "count": 0}

    # Compute contributions
    total_change = sum(abs(r.get(metric_col, 0) or 0) for r in rows)
    contributors = []
    cumulative_pct = 0.0

    sorted_rows = sorted(rows, key=lambda r: abs(r.get(metric_col, 0) or 0), reverse=True)

    for r in sorted_rows[:top_n]:
        value = float(r.get(metric_col, 0) or 0)
        pct = (abs(value) / total_change * 100) if total_change != 0 else 0
        cumulative_pct += pct
        contributors.append({
            "name": r.get(group_col, "Unknown"),
            "value": value,
            "contribution_pct": round(pct, 2),
            "cumulative_pct": round(cumulative_pct, 2),
            "significant": pct > 25,
        })

    result = {
        "level": level,
        "group_by": group_col,
        "metric": metric_col,
        "total_absolute_change": total_change,
        "contributors": contributors,
        "count": len(contributors),
        "top_n": top_n,
    }

    existing = tool_context.state.get("drilldown_data", {})
    existing[level] = result
    tool_context.state["drilldown_data"] = existing

    return result


def drill_by_entity(
    table: str,
    entity_column: str,
    metric_column: str,
    date_column: str,
    current_date: str,
    previous_date: str,
    tool_context: ToolContext,
    top_n: int = 10,
) -> dict:
    """Drill down metric changes by entity (legal entity level).

    Args:
        table: Fully qualified table name (database.schema.table).
        entity_column: Column containing entity identifiers.
        metric_column: Column with the metric values.
        date_column: Column with dates.
        current_date: Current date string (YYYY-MM-DD).
        previous_date: Previous date string (YYYY-MM-DD).
        top_n: Number of top contributors to return (default 10).
    """
    sql = f"""
        SELECT
            curr.{entity_column} AS {entity_column},
            curr.{metric_column} - COALESCE(prev.{metric_column}, 0) AS {metric_column}
        FROM (
            SELECT {entity_column}, SUM({metric_column}) AS {metric_column}
            FROM {table}
            WHERE {date_column} = '{current_date}'
            GROUP BY {entity_column}
        ) curr
        LEFT JOIN (
            SELECT {entity_column}, SUM({metric_column}) AS {metric_column}
            FROM {table}
            WHERE {date_column} = '{previous_date}'
            GROUP BY {entity_column}
        ) prev ON curr.{entity_column} = prev.{entity_column}
        ORDER BY ABS(curr.{metric_column} - COALESCE(prev.{metric_column}, 0)) DESC
    """
    return _run_drilldown_query(
        sql, entity_column, metric_column, top_n, tool_context, "entity"
    )


def drill_by_flb(
    table: str,
    flb_column: str,
    metric_column: str,
    date_column: str,
    current_date: str,
    previous_date: str,
    tool_context: ToolContext,
    entity_filter: str | None = None,
    entity_column: str | None = None,
    top_n: int = 10,
) -> dict:
    """Drill down metric changes by FLB (Funding Liquidity Bucket).

    Args:
        table: Fully qualified table name.
        flb_column: Column containing FLB identifiers.
        metric_column: Column with the metric values.
        date_column: Column with dates.
        current_date: Current date string (YYYY-MM-DD).
        previous_date: Previous date string (YYYY-MM-DD).
        entity_filter: Optional entity to filter to.
        entity_column: Column name for entity (required if entity_filter is set).
        top_n: Number of top contributors to return (default 10).
    """
    where_extra = ""
    if entity_filter and entity_column:
        where_extra = f" AND {entity_column} = '{entity_filter}'"

    sql = f"""
        SELECT
            curr.{flb_column} AS {flb_column},
            curr.{metric_column} - COALESCE(prev.{metric_column}, 0) AS {metric_column}
        FROM (
            SELECT {flb_column}, SUM({metric_column}) AS {metric_column}
            FROM {table}
            WHERE {date_column} = '{current_date}'{where_extra}
            GROUP BY {flb_column}
        ) curr
        LEFT JOIN (
            SELECT {flb_column}, SUM({metric_column}) AS {metric_column}
            FROM {table}
            WHERE {date_column} = '{previous_date}'{where_extra}
            GROUP BY {flb_column}
        ) prev ON curr.{flb_column} = prev.{flb_column}
        ORDER BY ABS(curr.{metric_column} - COALESCE(prev.{metric_column}, 0)) DESC
    """
    return _run_drilldown_query(
        sql, flb_column, metric_column, top_n, tool_context, "flb"
    )


def drill_by_cusip(
    table: str,
    cusip_column: str,
    metric_column: str,
    date_column: str,
    current_date: str,
    previous_date: str,
    tool_context: ToolContext,
    flb_filter: str | None = None,
    flb_column: str | None = None,
    entity_filter: str | None = None,
    entity_column: str | None = None,
    top_n: int = 10,
) -> dict:
    """Drill down metric changes by CUSIP (individual security level).

    Args:
        table: Fully qualified table name.
        cusip_column: Column containing CUSIP identifiers.
        metric_column: Column with the metric values.
        date_column: Column with dates.
        current_date: Current date string (YYYY-MM-DD).
        previous_date: Previous date string (YYYY-MM-DD).
        flb_filter: Optional FLB to filter to.
        flb_column: Column name for FLB (required if flb_filter is set).
        entity_filter: Optional entity to filter to.
        entity_column: Column name for entity (required if entity_filter is set).
        top_n: Number of top contributors to return (default 10).
    """
    where_extra = ""
    if entity_filter and entity_column:
        where_extra += f" AND {entity_column} = '{entity_filter}'"
    if flb_filter and flb_column:
        where_extra += f" AND {flb_column} = '{flb_filter}'"

    sql = f"""
        SELECT
            curr.{cusip_column} AS {cusip_column},
            curr.{metric_column} - COALESCE(prev.{metric_column}, 0) AS {metric_column}
        FROM (
            SELECT {cusip_column}, SUM({metric_column}) AS {metric_column}
            FROM {table}
            WHERE {date_column} = '{current_date}'{where_extra}
            GROUP BY {cusip_column}
        ) curr
        LEFT JOIN (
            SELECT {cusip_column}, SUM({metric_column}) AS {metric_column}
            FROM {table}
            WHERE {date_column} = '{previous_date}'{where_extra}
            GROUP BY {cusip_column}
        ) prev ON curr.{cusip_column} = prev.{cusip_column}
        ORDER BY ABS(curr.{metric_column} - COALESCE(prev.{metric_column}, 0)) DESC
    """
    return _run_drilldown_query(
        sql, cusip_column, metric_column, top_n, tool_context, "cusip"
    )


def waterfall_decomposition(tool_context: ToolContext) -> dict:
    """Generate a waterfall decomposition from existing drill-down data.

    Combines entity, FLB, and CUSIP drill-down results into a waterfall view
    showing how the total change decomposes through each hierarchy level.
    """
    dd = tool_context.state.get("drilldown_data", {})
    if not dd:
        return {"error": "No drill-down data available. Run drill_by_* tools first."}

    waterfall = {"levels": []}
    for level_name in ["entity", "flb", "cusip"]:
        level_data = dd.get(level_name)
        if level_data:
            waterfall["levels"].append({
                "level": level_name,
                "total_change": level_data.get("total_absolute_change", 0),
                "top_contributors": [
                    {
                        "name": c["name"],
                        "value": c["value"],
                        "pct": c["contribution_pct"],
                    }
                    for c in level_data.get("contributors", [])[:5]
                ],
            })

    existing = tool_context.state.get("drilldown_data", {})
    existing["waterfall"] = waterfall
    tool_context.state["drilldown_data"] = existing

    return waterfall
