"""Root agent entrypoint for ADK discovery.

ADK discovers the agent by looking for a `root_agent` variable in the
top-level `agent.py` (or the module's `agent.py`).

The App object provides centralized configuration, lifecycle management,
and plugin support for the agent workflow.
"""

from google.adk.apps import App

from risk_analytics_agent.orchestrator.agent import orchestrator_agent

# Define root agent
root_agent = orchestrator_agent

# Create App object (recommended for ADK workflows)
app = App(
    name="risk_analytics_agent",
    root_agent=root_agent,
    # App-level features can be configured here:
    # - plugins: Add cross-cutting concerns like logging, monitoring
    # - context_cache_config: Configure context caching
    # - resumability_config: Enable agent resume functionality
)
