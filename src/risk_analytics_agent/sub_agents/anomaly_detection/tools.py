"""Anomaly detection tools using layered statistical methods."""

from __future__ import annotations

import logging
from datetime import date, timedelta

import numpy as np
import polars as pl

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


def _get_dataframe(tool_context: ToolContext) -> pl.DataFrame | None:
    data = tool_context.state.get("query_result")
    if not data:
        return None
    return pl.DataFrame(data)


def _is_calendar_boundary(d: date) -> str | None:
    """Check if a date is a month-end or quarter-end."""
    next_day = d + timedelta(days=1)
    if next_day.month != d.month:
        if d.month in (3, 6, 9, 12):
            return "quarter_end"
        return "month_end"
    return None


def detect_zscore_anomalies(
    date_column: str,
    metric_column: str,
    tool_context: ToolContext,
    threshold: float = 3.0,
) -> dict:
    """Detect anomalies using z-score method.

    Args:
        date_column: Name of the date column.
        metric_column: Name of the metric column to analyze.
        threshold: Z-score threshold for anomaly detection (default 3.0).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    df = df.with_columns(pl.col(date_column).cast(pl.Date).alias(date_column))
    series = df[metric_column].cast(pl.Float64, strict=False).to_numpy()
    dates = df[date_column].to_list()

    mean = np.nanmean(series)
    std = np.nanstd(series, ddof=1)

    if std == 0:
        return {"method": "zscore", "anomalies": [], "count": 0}

    z_scores = (series - mean) / std
    anomalies = []

    for i, (z, val) in enumerate(zip(z_scores, series)):
        if abs(z) >= threshold:
            d = dates[i]
            cal = _is_calendar_boundary(d) if isinstance(d, date) else None
            anomalies.append({
                "date": str(d),
                "value": float(val),
                "z_score": float(z),
                "direction": "high" if z > 0 else "low",
                "calendar_flag": cal,
            })

    existing = tool_context.state.get("anomaly_data", {})
    existing["zscore"] = {"anomalies": anomalies, "threshold": threshold}
    tool_context.state["anomaly_data"] = existing

    return {"method": "zscore", "threshold": threshold, "anomalies": anomalies, "count": len(anomalies)}


def detect_iqr_anomalies(
    date_column: str,
    metric_column: str,
    tool_context: ToolContext,
    factor: float = 2.0,
) -> dict:
    """Detect anomalies using Interquartile Range (IQR) method.

    Args:
        date_column: Name of the date column.
        metric_column: Name of the metric column to analyze.
        factor: IQR multiplier for fence calculation (default 2.0).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    df = df.with_columns(pl.col(date_column).cast(pl.Date).alias(date_column))
    series = df[metric_column].cast(pl.Float64, strict=False).to_numpy()
    dates = df[date_column].to_list()

    q1 = float(np.nanpercentile(series, 25))
    q3 = float(np.nanpercentile(series, 75))
    iqr = q3 - q1

    lower_fence = q1 - factor * iqr
    upper_fence = q3 + factor * iqr

    anomalies = []
    for i, val in enumerate(series):
        if val < lower_fence or val > upper_fence:
            d = dates[i]
            cal = _is_calendar_boundary(d) if isinstance(d, date) else None
            anomalies.append({
                "date": str(d),
                "value": float(val),
                "lower_fence": lower_fence,
                "upper_fence": upper_fence,
                "direction": "high" if val > upper_fence else "low",
                "calendar_flag": cal,
            })

    existing = tool_context.state.get("anomaly_data", {})
    existing["iqr"] = {
        "anomalies": anomalies,
        "factor": factor,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "fences": [lower_fence, upper_fence],
    }
    tool_context.state["anomaly_data"] = existing

    return {
        "method": "iqr",
        "factor": factor,
        "fences": [lower_fence, upper_fence],
        "anomalies": anomalies,
        "count": len(anomalies),
    }


def detect_rolling_anomalies(
    date_column: str,
    metric_column: str,
    tool_context: ToolContext,
    window: int = 30,
    threshold: float = 2.5,
) -> dict:
    """Detect anomalies using rolling window statistics.

    Args:
        date_column: Name of the date column.
        metric_column: Name of the metric column to analyze.
        window: Rolling window size in days (default 30).
        threshold: Number of rolling std deviations for detection (default 2.5).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    df = df.with_columns(pl.col(date_column).cast(pl.Date).alias(date_column))
    df = df.sort(date_column)

    series = df[metric_column].cast(pl.Float64, strict=False).to_numpy()
    dates = df[date_column].to_list()

    anomalies = []
    for i in range(window, len(series)):
        window_data = series[i - window : i]
        w_mean = np.nanmean(window_data)
        w_std = np.nanstd(window_data, ddof=1)

        if w_std == 0:
            continue

        deviation = abs(series[i] - w_mean) / w_std
        if deviation >= threshold:
            d = dates[i]
            cal = _is_calendar_boundary(d) if isinstance(d, date) else None
            anomalies.append({
                "date": str(d),
                "value": float(series[i]),
                "rolling_mean": float(w_mean),
                "rolling_std": float(w_std),
                "deviation_sigma": float(deviation),
                "direction": "high" if series[i] > w_mean else "low",
                "calendar_flag": cal,
            })

    existing = tool_context.state.get("anomaly_data", {})
    existing["rolling"] = {
        "anomalies": anomalies,
        "window": window,
        "threshold": threshold,
    }
    tool_context.state["anomaly_data"] = existing

    return {
        "method": "rolling",
        "window": window,
        "threshold": threshold,
        "anomalies": anomalies,
        "count": len(anomalies),
    }


def summarize_anomalies(tool_context: ToolContext) -> dict:
    """Summarize anomalies across all detection methods with consensus scoring.

    Points flagged by 2+ methods are marked as high-confidence anomalies.
    Calendar boundary dates are flagged for potential suppression.
    """
    ad = tool_context.state.get("anomaly_data", {})
    if not ad:
        return {"error": "No anomaly data. Run detection methods first."}

    # Collect all flagged dates by method
    date_methods: dict[str, list[str]] = {}
    date_details: dict[str, dict] = {}

    for method_name in ["zscore", "iqr", "rolling"]:
        method_data = ad.get(method_name, {})
        for a in method_data.get("anomalies", []):
            d = a["date"]
            date_methods.setdefault(d, []).append(method_name)
            if d not in date_details:
                date_details[d] = {
                    "date": d,
                    "value": a.get("value"),
                    "direction": a.get("direction"),
                    "calendar_flag": a.get("calendar_flag"),
                }

    # Build consensus summary
    summary = []
    for d, methods in sorted(date_methods.items()):
        details = date_details[d]
        confidence = "high" if len(methods) >= 2 else "low"
        # Suppress calendar boundaries
        if details.get("calendar_flag") and confidence == "low":
            confidence = "suppressed"
        summary.append({
            **details,
            "methods": methods,
            "method_count": len(methods),
            "confidence": confidence,
        })

    # Sort by method count descending
    summary.sort(key=lambda x: x["method_count"], reverse=True)

    ad["summary"] = summary
    ad["high_confidence_count"] = sum(1 for s in summary if s["confidence"] == "high")
    ad["total_anomaly_dates"] = len(summary)
    tool_context.state["anomaly_data"] = ad

    return {
        "total_anomaly_dates": len(summary),
        "high_confidence": ad["high_confidence_count"],
        "summary": summary[:20],
    }
