"""Anomaly Detection sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.anomaly_detection.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.anomaly_detection.tools import (
    detect_iqr_anomalies,
    detect_rolling_anomalies,
    detect_zscore_anomalies,
    summarize_anomalies,
)

anomaly_detection_agent = LlmAgent(
    name="anomaly_detection_agent",
    model=get_model("anomaly_detection_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Detects anomalies in liquidity data using z-score, IQR, and rolling "
        "window methods with consensus scoring. Use when you need to identify "
        "unusual patterns or outliers in time-series data."
    ),
    tools=[
        detect_zscore_anomalies,
        detect_iqr_anomalies,
        detect_rolling_anomalies,
        summarize_anomalies,
    ],
)
