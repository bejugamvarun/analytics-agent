"""Variance Analysis sub-agent."""

import pathlib

from google.adk.agents import LlmAgent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.variance_analysis.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.variance_analysis.tools import (
    compute_day_over_day,
    get_variance_timeseries,
    identify_significant_moves,
)

# Load MLO Analysis Skill
mlo_skill_path = pathlib.Path(__file__).parent.parent.parent.parent.parent / "skills" / "mlo-analysis"
mlo_skill = load_skill_from_dir(mlo_skill_path)

# Create skill toolset
mlo_skillset = skill_toolset.SkillToolset(
    skills=[mlo_skill]
)

variance_analysis_agent = LlmAgent(
    name="variance_analysis_agent",
    model=get_model("variance_analysis_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Tracks day-over-day changes in liquidity metrics and identifies "
        "statistically significant moves. Use when analyzing metric changes "
        "over time or detecting unusual daily movements. Enhanced with MLO analysis skill."
    ),
    tools=[
        mlo_skillset,
        compute_day_over_day,
        identify_significant_moves,
        get_variance_timeseries,
    ],
)
