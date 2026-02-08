"""Schema Discovery sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.schema_discovery.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.schema_discovery.tools import (
    describe_table,
    list_databases,
    list_schemas,
    list_tables,
    sample_table,
    search_columns,
)

schema_discovery_agent = LlmAgent(
    name="schema_discovery_agent",
    model=get_model("schema_discovery_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Discovers and catalogs Snowflake database schemas, tables, "
        "columns, and sample data. Use this agent when you need to "
        "understand what data is available in the warehouse."
    ),
    tools=[
        list_databases,
        list_schemas,
        list_tables,
        describe_table,
        sample_table,
        search_columns,
    ],
)
