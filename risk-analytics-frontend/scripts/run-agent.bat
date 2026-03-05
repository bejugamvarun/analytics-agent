@echo off
REM Navigate to the root project directory
cd /d %~dp0\..\..

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run the agent server
python -m risk_analytics_agent.server
