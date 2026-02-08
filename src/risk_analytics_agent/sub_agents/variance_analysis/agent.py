"""Variance Analysis sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.variance_analysis.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.variance_analysis.tools import (
    compute_day_over_day,
    get_variance_timeseries,
    identify_significant_moves,
)

variance_analysis_agent = LlmAgent(
    name="variance_analysis_agent",
    model=get_model("variance_analysis_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Tracks day-over-day changes in liquidity metrics and identifies "
        "statistically significant moves. Use when analyzing metric changes "
        "over time or detecting unusual daily movements."
    ),
    tools=[
        compute_day_over_day,
        identify_significant_moves,
        get_variance_timeseries,
    ],
)
