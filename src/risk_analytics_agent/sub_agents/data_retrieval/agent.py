"""Data Retrieval sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.data_retrieval.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.data_retrieval.tools import (
    execute_sql,
    get_query_history,
    validate_sql,
)

data_retrieval_agent = LlmAgent(
    name="data_retrieval_agent",
    model=get_model("data_retrieval_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Generates and executes safe, read-only SQL queries against Snowflake. "
        "Use this agent to retrieve data for analysis. It enforces SQL safety "
        "by rejecting any DDL/DML statements."
    ),
    tools=[validate_sql, execute_sql, get_query_history],
)
