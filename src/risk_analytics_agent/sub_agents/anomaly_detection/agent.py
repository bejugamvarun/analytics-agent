"""Anomaly Detection sub-agent."""

import pathlib

from google.adk.agents import LlmAgent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.anomaly_detection.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.anomaly_detection.tools import (
    detect_iqr_anomalies,
    detect_rolling_anomalies,
    detect_zscore_anomalies,
    summarize_anomalies,
)

# Load Anomaly Detection Skill
anomaly_skill_path = pathlib.Path(__file__).parent.parent.parent.parent.parent / "skills" / "anomaly-detection"
anomaly_skill = load_skill_from_dir(anomaly_skill_path)

# Create skill toolset
anomaly_skillset = skill_toolset.SkillToolset(
    skills=[anomaly_skill]
)

anomaly_detection_agent = LlmAgent(
    name="anomaly_detection_agent",
    model=get_model("anomaly_detection_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Detects anomalies in liquidity data using z-score, IQR, and rolling "
        "window methods with consensus scoring. Use when you need to identify "
        "unusual patterns or outliers in time-series data. Enhanced with statistical methods skill."
    ),
    tools=[
        anomaly_skillset,
        detect_zscore_anomalies,
        detect_iqr_anomalies,
        detect_rolling_anomalies,
        summarize_anomalies,
    ],
)
