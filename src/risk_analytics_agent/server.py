"""FastAPI server for the Risk Analytics Agent.

This module provides a FastAPI endpoint for the CopilotKit UI to interact
with the Google ADK agent.
"""

from __future__ import annotations

import logging

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI

from risk_analytics_agent.agent import root_agent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
fastapi_app = FastAPI(
    title="Risk Analytics Agent API",
    description="Google ADK agent for financial liquidity risk analytics",
    version="0.1.0",
)

# Create ADK agent wrapper
adk_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="risk_analytics_agent",
    user_id="default_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# Add ADK endpoint for CopilotKit integration
add_adk_fastapi_endpoint(fastapi_app, adk_agent, path="/")

logger.info("Risk Analytics Agent server initialized")


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Risk Analytics Agent server on http://localhost:8000")
    uvicorn.run(
        "risk_analytics_agent.server:fastapi_app",
        host="0.0.0.0",
        port=8000,
    )
