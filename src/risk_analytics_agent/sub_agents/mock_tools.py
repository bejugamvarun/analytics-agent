"""Mock data generation tools for demo purposes when Snowflake is not available."""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any

import polars as pl
from google.adk.tools import ToolContext


def generate_mock_liquidity_data(
    tool_context: ToolContext,
    num_rows: int = 100,
    metric_type: str = "MLO",
) -> dict[str, Any]:
    """Generate mock liquidity data for demonstration.
    
    Args:
        tool_context: The tool context
        num_rows: Number of rows to generate (default: 100)
        metric_type: Type of metric (MLO, HQLA, etc.)
        
    Returns:
        Dictionary with mock data and metadata
    """
    # Generate dates for the last N days
    base_date = datetime.now()
    dates = [(base_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_rows)]
    
    # Generate entities
    entities = [f"ENTITY_{i:03d}" for i in range(1, 11)]
    
    # Generate mock data
    data = []
    for date in dates:
        for entity in random.sample(entities, k=min(5, len(entities))):
            mlo_value = random.uniform(1e9, 50e9)  # 1B to 50B
            variance = random.uniform(-5, 5)  # -5% to +5%
            
            data.append({
                "date": date,
                "entity": entity,
                "metric_type": metric_type,
                "value": round(mlo_value, 2),
                "variance_pct": round(variance, 2),
                "currency": "USD",
                "scenario": random.choice(["BASE", "STRESS_1", "STRESS_2"]),
            })
    
    df = pl.DataFrame(data)
    result_data = df.head(50).to_dicts()
    
    # Store in UI state for rendering
    tool_context.state["ui_display"] = {
        "type": "table",
        "title": f"Mock {metric_type} Liquidity Data",
        "data": result_data,
        "timestamp": datetime.now().isoformat(),
    }
    
    return {
        "status": "success",
        "message": f"Generated {len(df)} rows of {metric_type} data. Displaying first 50 rows in the UI.",
        "rows": len(df),
        "columns": df.columns,
        "summary": {
            "total_rows": len(df),
            "unique_dates": df["date"].n_unique(),
            "unique_entities": df["entity"].n_unique(),
            "avg_value": float(df["value"].mean()),
            "total_value": float(df["value"].sum()),
        },
    }


def generate_variance_analysis(
    tool_context: ToolContext,
    entity: str | None = None,
) -> dict[str, Any]:
    """Generate mock variance analysis results.
    
    Args:
        tool_context: The tool context
        entity: Optional entity to filter by
        
    Returns:
        Dictionary with variance analysis results
    """
    # Generate variance data
    base_date = datetime.now()
    today = base_date.strftime("%Y-%m-%d")
    yesterday = (base_date - timedelta(days=1)).strftime("%Y-%m-%d")
    
    entities = [entity] if entity else [f"ENTITY_{i:03d}" for i in range(1, 6)]
    
    results = []
    for ent in entities:
        today_value = random.uniform(1e9, 50e9)
        yesterday_value = today_value * random.uniform(0.95, 1.05)
        variance = ((today_value - yesterday_value) / yesterday_value) * 100
        
        results.append({
            "entity": ent,
            "date": today,
            "previous_date": yesterday,
            "current_value": round(today_value, 2),
            "previous_value": round(yesterday_value, 2),
            "absolute_change": round(today_value - yesterday_value, 2),
            "variance_percent": round(variance, 2),
            "status": "increase" if variance > 0 else "decrease",
        })
    
    # Store in UI state
    tool_context.state["ui_display"] = {
        "type": "table",
        "title": "Day-over-Day Variance Analysis",
        "data": results,
        "timestamp": datetime.now().isoformat(),
    }
    
    return {
        "status": "success",
        "message": f"Variance analysis complete for {len(results)} entities. Results displayed in UI.",
        "analysis_type": "variance",
        "date_range": f"{yesterday} to {today}",
        "summary": {
            "total_entities": len(results),
            "avg_variance": round(sum(r["variance_percent"] for r in results) / len(results), 2),
            "entities_increased": len([r for r in results if r["variance_percent"] > 0]),
            "entities_decreased": len([r for r in results if r["variance_percent"] < 0]),
        },
    }


def detect_mock_anomalies(
    tool_context: ToolContext,
    threshold: float = 3.0,
) -> dict[str, Any]:
    """Detect mock anomalies in the data.
    
    Args:
        tool_context: The tool context
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        Dictionary with detected anomalies
    """
    # Generate anomaly data
    anomalies = []
    base_date = datetime.now()
    
    for i in range(random.randint(3, 10)):
        entity = f"ENTITY_{random.randint(1, 10):03d}"
        date = (base_date - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        value = random.uniform(1e9, 100e9)
        expected_value = value * random.uniform(0.5, 0.8)
        z_score = random.uniform(threshold, threshold + 2)
        
        anomalies.append({
            "entity": entity,
            "date": date,
            "metric": "MLO",
            "value": round(value, 2),
            "expected_value": round(expected_value, 2),
            "z_score": round(z_score, 2),
            "deviation_pct": round(((value - expected_value) / expected_value) * 100, 2),
            "severity": "HIGH" if z_score > threshold + 1 else "MEDIUM",
        })
    
    # Store in UI state
    tool_context.state["ui_display"] = {
        "type": "anomalies",
        "title": "Detected Anomalies",
        "data": anomalies,
        "timestamp": datetime.now().isoformat(),
    }
    
    return {
        "status": "success",
        "message": f"Detected {len(anomalies)} anomalies with threshold {threshold}. Results displayed in UI.",
        "analysis_type": "anomaly_detection",
        "threshold": threshold,
        "summary": {
            "total_anomalies": len(anomalies),
            "high_severity": len([a for a in anomalies if a["severity"] == "HIGH"]),
            "medium_severity": len([a for a in anomalies if a["severity"] == "MEDIUM"]),
            "avg_deviation": round(sum(a["deviation_pct"] for a in anomalies) / len(anomalies), 2) if anomalies else 0,
        },
    }


def generate_mock_metrics(
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Generate mock key metrics for the dashboard.
    
    Args:
        tool_context: The tool context
        
    Returns:
        Dictionary with key metrics
    """
    metrics = {
        "mlo_total": round(random.uniform(50e9, 200e9), 2),
        "hqla_ratio": round(random.uniform(110, 150), 2),
        "lcr": round(random.uniform(120, 180), 2),
        "nsfr": round(random.uniform(110, 140), 2),
        "variance_percent": round(random.uniform(-3, 3), 2),
        "anomaly_count": random.randint(0, 15),
        "stress_scenario_impact": round(random.uniform(-10, -2), 2),
        "concentration_risk_score": round(random.uniform(0.1, 0.5), 2),
    }
    
    # Store in UI state
    tool_context.state["ui_display"] = {
        "type": "metrics",
        "title": "Key Liquidity Metrics",
        "data": metrics,
        "timestamp": datetime.now().isoformat(),
    }
    
    return {
        "status": "success",
        "message": "Generated key liquidity metrics. Results displayed in UI.",
        "metrics": metrics,
        "timestamp": datetime.now().isoformat(),
        "currency": "USD",
    }


def list_mock_schemas(
    tool_context: ToolContext,
) -> dict[str, Any]:
    """List mock database schemas for demonstration.
    
    Args:
        tool_context: The tool context
        
    Returns:
        Dictionary with mock schema information
    """
    schemas = {
        "LIQUIDITY_DB": {
            "schemas": ["LIQUIDITY", "STRESS_TESTING", "REGULATORY"],
            "tables": {
                "LIQUIDITY": ["MLO_DAILY", "HQLA_POSITIONS", "CASH_FLOWS", "CONCENTRATION_METRICS"],
                "STRESS_TESTING": ["SCENARIOS", "RESULTS", "ASSUMPTIONS"],
                "REGULATORY": ["LCR_CALC", "NSFR_CALC", "REPORTING"],
            },
        },
    }
    
    # Flatten for table display
    schema_data = []
    for schema, tables in schemas["LIQUIDITY_DB"]["tables"].items():
        for table in tables:
            schema_data.append({
                "database": "LIQUIDITY_DB",
                "schema": schema,
                "table": table,
            })
    
    # Store in UI state
    tool_context.state["ui_display"] = {
        "type": "table",
        "title": "Available Database Schemas",
        "data": schema_data,
        "timestamp": datetime.now().isoformat(),
    }
    
    return {
        "status": "success",
        "message": f"Found {len(schema_data)} tables across {len(schemas['LIQUIDITY_DB']['schemas'])} schemas. Results displayed in UI.",
        "database": "LIQUIDITY_DB",
        "total_schemas": len(schemas["LIQUIDITY_DB"]["schemas"]),
        "total_tables": len(schema_data),
    }
