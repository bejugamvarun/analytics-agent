"""Drill-Down Analysis sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.drilldown_analysis.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.drilldown_analysis.tools import (
    drill_by_cusip,
    drill_by_entity,
    drill_by_flb,
    waterfall_decomposition,
)

drilldown_analysis_agent = LlmAgent(
    name="drilldown_analysis_agent",
    model=get_model("drilldown_analysis_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Decomposes aggregate metric changes across entity, FLB, and CUSIP "
        "hierarchies. Use when you need to identify which entities, funding "
        "buckets, or securities are driving a metric change."
    ),
    tools=[
        drill_by_entity,
        drill_by_flb,
        drill_by_cusip,
        waterfall_decomposition,
    ],
)
