"""Root agent entrypoint for ADK discovery.

ADK discovers the agent by looking for a `root_agent` variable in the
top-level `agent.py` (or the module's `agent.py`).
"""

from risk_analytics_agent.orchestrator.agent import orchestrator_agent

root_agent = orchestrator_agent
