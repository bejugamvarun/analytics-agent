"""Quantitative Analysis sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.quantitative_analysis.prompt import (
    SYSTEM_INSTRUCTION,
)
from risk_analytics_agent.sub_agents.quantitative_analysis.tools import (
    compute_correlation,
    compute_distribution,
    compute_percentiles,
    compute_statistics,
)

quantitative_analysis_agent = LlmAgent(
    name="quantitative_analysis_agent",
    model=get_model("quantitative_analysis_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Performs statistical analysis on retrieved data including descriptive "
        "statistics, percentiles, distribution analysis, and correlations. "
        "Use after data has been retrieved into session state."
    ),
    tools=[
        compute_statistics,
        compute_percentiles,
        compute_distribution,
        compute_correlation,
    ],
)
