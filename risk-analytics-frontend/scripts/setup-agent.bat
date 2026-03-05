@echo off
REM Navigate to the root project directory
cd /d "%~dp0\..\.." || exit /b 1

uv sync
