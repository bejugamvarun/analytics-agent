"""Orchestrator agent that routes to specialized sub-agents."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.orchestrator.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.anomaly_detection.agent import (
    anomaly_detection_agent,
)
from risk_analytics_agent.sub_agents.data_retrieval.agent import data_retrieval_agent
from risk_analytics_agent.sub_agents.drilldown_analysis.agent import (
    drilldown_analysis_agent,
)
from risk_analytics_agent.sub_agents.quantitative_analysis.agent import (
    quantitative_analysis_agent,
)
from risk_analytics_agent.sub_agents.report_generation.agent import (
    report_generation_agent,
)
from risk_analytics_agent.sub_agents.schema_discovery.agent import (
    schema_discovery_agent,
)
from risk_analytics_agent.sub_agents.variance_analysis.agent import (
    variance_analysis_agent,
)

orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model=get_model("orchestrator_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description="Root orchestrator that coordinates liquidity risk analysis across sub-agents.",
    sub_agents=[
        schema_discovery_agent,
        data_retrieval_agent,
        quantitative_analysis_agent,
        variance_analysis_agent,
        drilldown_analysis_agent,
        anomaly_detection_agent,
        report_generation_agent,
    ],
)
