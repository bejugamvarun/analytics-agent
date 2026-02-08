"""Quantitative analysis tools using Polars, NumPy, and SciPy."""

from __future__ import annotations

import json
import logging

import numpy as np
import polars as pl
from scipy import stats as scipy_stats

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


def _get_dataframe(tool_context: ToolContext) -> pl.DataFrame | None:
    """Load query_result from state into a Polars DataFrame."""
    data = tool_context.state.get("query_result")
    if not data:
        return None
    return pl.DataFrame(data)


def compute_statistics(
    columns: list[str], tool_context: ToolContext
) -> dict:
    """Compute descriptive statistics for specified numeric columns.

    Args:
        columns: List of column names to analyze.
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    results = {}
    for col in columns:
        if col not in df.columns:
            results[col] = {"error": f"Column '{col}' not found"}
            continue

        series = df[col].drop_nulls().cast(pl.Float64, strict=False)
        if series.is_empty():
            results[col] = {"error": "No non-null values"}
            continue

        values = series.to_numpy()
        results[col] = {
            "count": len(values),
            "mean": float(np.mean(values)),
            "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "median": float(np.median(values)),
            "sum": float(np.sum(values)),
        }

    tool_context.state["statistics"] = results
    return {"statistics": results, "columns_analyzed": len(results)}


def compute_percentiles(
    columns: list[str],
    tool_context: ToolContext,
    percentiles: list[float] | None = None,
) -> dict:
    """Compute percentiles for specified numeric columns.

    Args:
        columns: List of column names to analyze.
        percentiles: List of percentile values (0-100). Defaults to [5,10,25,50,75,90,95].
    """
    if percentiles is None:
        percentiles = [5, 10, 25, 50, 75, 90, 95]

    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    results = {}
    for col in columns:
        if col not in df.columns:
            results[col] = {"error": f"Column '{col}' not found"}
            continue

        series = df[col].drop_nulls().cast(pl.Float64, strict=False)
        if series.is_empty():
            results[col] = {"error": "No non-null values"}
            continue

        values = series.to_numpy()
        pct_values = np.percentile(values, percentiles)
        results[col] = {
            f"p{int(p)}": float(v) for p, v in zip(percentiles, pct_values)
        }

    existing = tool_context.state.get("statistics", {})
    existing["percentiles"] = results
    tool_context.state["statistics"] = existing

    return {"percentiles": results}


def compute_distribution(
    column: str, tool_context: ToolContext, bins: int = 20
) -> dict:
    """Analyze the distribution of a numeric column.

    Args:
        column: Column name to analyze.
        bins: Number of histogram bins (default 20).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    if column not in df.columns:
        return {"error": f"Column '{column}' not found"}

    series = df[column].drop_nulls().cast(pl.Float64, strict=False)
    values = series.to_numpy()

    if len(values) < 3:
        return {"error": "Need at least 3 values for distribution analysis"}

    hist_counts, hist_edges = np.histogram(values, bins=bins)
    skewness = float(scipy_stats.skew(values))
    kurtosis = float(scipy_stats.kurtosis(values))

    # Normality test (Shapiro-Wilk for small samples, D'Agostino for large)
    if len(values) <= 5000:
        stat, p_value = scipy_stats.shapiro(values[:5000])
        normality_test = "shapiro-wilk"
    else:
        stat, p_value = scipy_stats.normaltest(values)
        normality_test = "dagostino-pearson"

    result = {
        "column": column,
        "n": len(values),
        "skewness": skewness,
        "kurtosis": kurtosis,
        "normality_test": normality_test,
        "normality_stat": float(stat),
        "normality_p_value": float(p_value),
        "is_normal": p_value > 0.05,
        "histogram": {
            "counts": hist_counts.tolist(),
            "edges": hist_edges.tolist(),
        },
    }

    existing = tool_context.state.get("statistics", {})
    existing.setdefault("distributions", {})[column] = result
    tool_context.state["statistics"] = existing

    return result


def compute_correlation(
    columns: list[str], tool_context: ToolContext
) -> dict:
    """Compute pairwise correlation matrix for specified numeric columns.

    Args:
        columns: List of column names to compute correlations for (minimum 2).
    """
    df = _get_dataframe(tool_context)
    if df is None:
        return {"error": "No data in state['query_result']. Run a query first."}

    if len(columns) < 2:
        return {"error": "Need at least 2 columns for correlation"}

    available = [c for c in columns if c in df.columns]
    if len(available) < 2:
        return {"error": f"Found only {len(available)} valid columns: {available}"}

    sub = df.select(available).drop_nulls().cast({c: pl.Float64 for c in available})
    arr = sub.to_numpy()
    corr_matrix = np.corrcoef(arr, rowvar=False)

    result = {
        "columns": available,
        "matrix": corr_matrix.tolist(),
        "pairs": {},
    }

    for i, c1 in enumerate(available):
        for j, c2 in enumerate(available):
            if i < j:
                result["pairs"][f"{c1}_vs_{c2}"] = float(corr_matrix[i, j])

    existing = tool_context.state.get("statistics", {})
    existing["correlation"] = result
    tool_context.state["statistics"] = existing

    return result
