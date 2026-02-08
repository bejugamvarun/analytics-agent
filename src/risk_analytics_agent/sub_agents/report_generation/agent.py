"""Report Generation sub-agent."""

from google.adk.agents import LlmAgent

from risk_analytics_agent.models import get_model
from risk_analytics_agent.sub_agents.report_generation.prompt import SYSTEM_INSTRUCTION
from risk_analytics_agent.sub_agents.report_generation.tools import (
    generate_chart,
    generate_table_html,
    render_markdown_report,
    render_pdf_report,
)

report_generation_agent = LlmAgent(
    name="report_generation_agent",
    model=get_model("report_generation_agent"),
    instruction=SYSTEM_INSTRUCTION,
    description=(
        "Generates professional HTML/PDF and Markdown reports with charts "
        "and tables from analysis results. Use after analysis is complete "
        "to produce deliverable reports."
    ),
    tools=[
        generate_chart,
        generate_table_html,
        render_markdown_report,
        render_pdf_report,
    ],
)
