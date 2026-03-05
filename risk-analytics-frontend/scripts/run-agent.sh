#!/bin/bash

# Navigate to the root project directory
cd "$(dirname "$0")/../.." || exit 1

# Activate the virtual environment
source .venv/bin/activate

# Run the agent server
python -m risk_analytics_agent.server
