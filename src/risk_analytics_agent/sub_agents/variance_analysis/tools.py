"""Variance analysis tools for day-over-day change tracking."""

from __future__ import annotations

import json
import logging

import numpy as np
import polars as pl

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


def _get_dataframe(tool_context: ToolContext) -> pl.DataFrame | None:
    data = tool_context.state.get("query_result")
    if not data:
        return None
    return pl.DataFrame(data)


def compute_day_over_day(
    date_column: str,
    metric_columns: list[str],
    tool_context: ToolContext,
    group_by: str | None = None,
) -> dict:
    """Compute day-over-day absolute and percentage changes.

    Args:
        date_column: Name of the date column.
        metric_columns: List of numeric columns to compute DoD changes for.
        group_by: Optional column to group by (e.g., entity name).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    df = df.with_columns(pl.col(date_column).cast(pl.Date).alias(date_column))
    df = df.sort(date_column)

    if group_by:
        df = df.sort([group_by, date_column])

    results = {}
    for col in metric_columns:
        if col not in df.columns:
            results[col] = {"error": f"Column '{col}' not found"}
            continue

        if group_by:
            dod = df.with_columns([
                (pl.col(col) - pl.col(col).shift(1).over(group_by)).alias(f"{col}_dod_abs"),
                (
                    (pl.col(col) - pl.col(col).shift(1).over(group_by))
                    / pl.col(col).shift(1).over(group_by)
                    * 100
                ).alias(f"{col}_dod_pct"),
            ])
        else:
            dod = df.with_columns([
                (pl.col(col) - pl.col(col).shift(1)).alias(f"{col}_dod_abs"),
                (
                    (pl.col(col) - pl.col(col).shift(1))
                    / pl.col(col).shift(1)
                    * 100
                ).alias(f"{col}_dod_pct"),
            ])

        # Get the latest DoD values
        latest = dod.tail(1)
        results[col] = {
            "latest_abs_change": float(latest[f"{col}_dod_abs"][0]) if latest[f"{col}_dod_abs"][0] is not None else None,
            "latest_pct_change": float(latest[f"{col}_dod_pct"][0]) if latest[f"{col}_dod_pct"][0] is not None else None,
            "latest_value": float(latest[col][0]) if latest[col][0] is not None else None,
        }

    # Store full DoD data
    dod_data = json.loads(dod.write_json())
    tool_context.state["variance_data"] = {
        "dod_changes": results,
        "full_data": dod_data,
    }

    return {"dod_changes": results, "metric_count": len(results)}


def identify_significant_moves(
    date_column: str,
    metric_columns: list[str],
    tool_context: ToolContext,
    sigma_threshold: float = 2.0,
    lookback_days: int = 30,
) -> dict:
    """Identify statistically significant day-over-day moves.

    A move is significant when the DoD change exceeds sigma_threshold standard
    deviations from the trailing mean of daily changes.

    Args:
        date_column: Name of the date column.
        metric_columns: List of numeric columns to evaluate.
        sigma_threshold: Number of standard deviations for significance (default 2.0).
        lookback_days: Number of trailing days for baseline (default 30).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    df = df.with_columns(pl.col(date_column).cast(pl.Date).alias(date_column))
    df = df.sort(date_column)

    significant = []

    for col in metric_columns:
        if col not in df.columns:
            continue

        series = df[col].cast(pl.Float64, strict=False)
        diffs = series.diff().drop_nulls().to_numpy()

        if len(diffs) < lookback_days:
            continue

        # Trailing stats from the lookback window (excluding last day)
        trailing = diffs[-(lookback_days + 1):-1]
        if len(trailing) == 0:
            continue

        trail_mean = float(np.mean(trailing))
        trail_std = float(np.std(trailing, ddof=1))

        if trail_std == 0:
            continue

        latest_change = float(diffs[-1])
        z_score = (latest_change - trail_mean) / trail_std

        if abs(z_score) >= sigma_threshold:
            latest_value = float(series[-1]) if series[-1] is not None else None
            prev_value = float(series[-2]) if series[-2] is not None else None
            pct_change = (
                (latest_change / prev_value * 100) if prev_value and prev_value != 0 else None
            )
            significant.append({
                "metric": col,
                "latest_value": latest_value,
                "previous_value": prev_value,
                "absolute_change": latest_change,
                "percentage_change": pct_change,
                "z_score": z_score,
                "direction": "increase" if latest_change > 0 else "decrease",
                "trailing_mean": trail_mean,
                "trailing_std": trail_std,
                "sigma_threshold": sigma_threshold,
            })

    existing = tool_context.state.get("variance_data", {})
    existing["significant_moves"] = significant
    tool_context.state["variance_data"] = existing

    return {
        "significant_moves": significant,
        "count": len(significant),
        "threshold": f"{sigma_threshold}σ over {lookback_days}-day window",
    }


def get_variance_timeseries(
    date_column: str,
    metric_column: str,
    tool_context: ToolContext,
    last_n_days: int = 90,
) -> dict:
    """Get a variance time series for a specific metric.

    Args:
        date_column: Name of the date column.
        metric_column: Name of the metric column.
        last_n_days: Number of days of history to include (default 90).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    df = df.with_columns(pl.col(date_column).cast(pl.Date).alias(date_column))
    df = df.sort(date_column).tail(last_n_days + 1)

    series = df[metric_column].cast(pl.Float64, strict=False)
    dates = df[date_column].to_list()

    diffs = series.diff().to_list()
    values = series.to_list()

    timeseries = []
    for i in range(1, len(dates)):
        timeseries.append({
            "date": str(dates[i]),
            "value": float(values[i]) if values[i] is not None else None,
            "dod_change": float(diffs[i]) if diffs[i] is not None else None,
        })

    existing = tool_context.state.get("variance_data", {})
    existing.setdefault("timeseries", {})[metric_column] = timeseries
    tool_context.state["variance_data"] = existing

    return {
        "metric": metric_column,
        "days": len(timeseries),
        "timeseries": timeseries[-10:],
        "note": f"Full {len(timeseries)}-day timeseries stored in state",
    }
