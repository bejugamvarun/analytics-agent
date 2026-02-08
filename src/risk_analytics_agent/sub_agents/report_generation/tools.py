"""Report generation tools for charts, tables, and formatted reports."""

from __future__ import annotations

import base64
import io
import json
import logging
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from jinja2 import Environment, FileSystemLoader

from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "output"
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def _ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def _fig_to_base64(fig: plt.Figure) -> str:
    """Convert a matplotlib figure to a base64 PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return b64


def generate_chart(
    chart_type: str,
    title: str,
    data: dict,
    tool_context: ToolContext,
    filename: str | None = None,
) -> dict:
    """Generate a chart and save it to the output directory.

    Args:
        chart_type: Type of chart — one of: line, bar, waterfall, histogram, heatmap, scatter.
        title: Chart title.
        data: Chart data. Structure depends on chart_type:
            - line/bar/scatter: {"x": [...], "y": [...], "labels": {...}}
            - waterfall: {"categories": [...], "values": [...]}
            - histogram: {"values": [...], "bins": 20}
            - heatmap: {"matrix": [[...]], "x_labels": [...], "y_labels": [...]}
        filename: Optional filename (without extension). Auto-generated if not provided.
    """
    out_dir = _ensure_output_dir()
    if filename is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{chart_type}_{ts}"

    filepath = out_dir / f"{filename}.png"

    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "line":
        ax.plot(data["x"], data["y"], marker="o", markersize=3)
        ax.set_xlabel(data.get("labels", {}).get("x", ""))
        ax.set_ylabel(data.get("labels", {}).get("y", ""))

    elif chart_type == "bar":
        ax.bar(data["x"], data["y"])
        ax.set_xlabel(data.get("labels", {}).get("x", ""))
        ax.set_ylabel(data.get("labels", {}).get("y", ""))
        plt.xticks(rotation=45, ha="right")

    elif chart_type == "waterfall":
        categories = data["categories"]
        values = data["values"]
        cumulative = []
        running = 0
        for v in values:
            cumulative.append(running)
            running += v
        colors = ["green" if v >= 0 else "red" for v in values]
        ax.bar(categories, values, bottom=cumulative, color=colors)
        plt.xticks(rotation=45, ha="right")

    elif chart_type == "histogram":
        bins = data.get("bins", 20)
        ax.hist(data["values"], bins=bins, edgecolor="black", alpha=0.7)
        ax.set_xlabel(data.get("labels", {}).get("x", "Value"))
        ax.set_ylabel("Frequency")

    elif chart_type == "heatmap":
        im = ax.imshow(data["matrix"], aspect="auto", cmap="RdYlGn_r")
        if "x_labels" in data:
            ax.set_xticks(range(len(data["x_labels"])))
            ax.set_xticklabels(data["x_labels"], rotation=45, ha="right")
        if "y_labels" in data:
            ax.set_yticks(range(len(data["y_labels"])))
            ax.set_yticklabels(data["y_labels"])
        fig.colorbar(im, ax=ax)

    elif chart_type == "scatter":
        ax.scatter(data["x"], data["y"], alpha=0.6)
        ax.set_xlabel(data.get("labels", {}).get("x", ""))
        ax.set_ylabel(data.get("labels", {}).get("y", ""))

    else:
        plt.close(fig)
        return {"error": f"Unsupported chart type: {chart_type}"}

    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    b64 = _fig_to_base64(fig)

    artifacts = tool_context.state.get("report_artifacts", {})
    artifacts.setdefault("charts", []).append({
        "filename": filename,
        "path": str(filepath),
        "base64": b64,
        "chart_type": chart_type,
        "title": title,
    })
    tool_context.state["report_artifacts"] = artifacts

    return {
        "chart_type": chart_type,
        "title": title,
        "path": str(filepath),
        "note": "Chart saved and base64 stored in state['report_artifacts']",
    }


def generate_table_html(
    headers: list[str],
    rows: list[list],
    title: str | None = None,
) -> dict:
    """Generate an HTML table from headers and rows.

    Args:
        headers: List of column header strings.
        rows: List of row data (each row is a list of values).
        title: Optional table title.
    """
    html = ""
    if title:
        html += f"<h3>{title}</h3>\n"
    html += '<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">\n'
    html += "<thead><tr>"
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead>\n<tbody>\n"
    for row in rows:
        html += "<tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>\n"
    html += "</tbody></table>\n"

    return {"html": html, "row_count": len(rows)}


def render_markdown_report(
    title: str,
    sections: dict,
    tool_context: ToolContext,
    filename: str | None = None,
) -> dict:
    """Render a Markdown report using the Jinja2 template.

    Args:
        title: Report title.
        sections: Dict of section_name -> content (Markdown text).
        filename: Optional filename (without extension).
    """
    out_dir = _ensure_output_dir()
    if filename is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{ts}"

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.md.j2")

    content = template.render(
        title=title,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sections=sections,
    )

    filepath = out_dir / f"{filename}.md"
    filepath.write_text(content, encoding="utf-8")

    artifacts = tool_context.state.get("report_artifacts", {})
    artifacts["markdown_report"] = str(filepath)
    tool_context.state["report_artifacts"] = artifacts

    return {"path": str(filepath), "format": "markdown"}


def render_pdf_report(
    title: str,
    sections: dict,
    tool_context: ToolContext,
    filename: str | None = None,
) -> dict:
    """Render an HTML/PDF report using the Jinja2 template.

    Args:
        title: Report title.
        sections: Dict of section_name -> content (HTML text).
        filename: Optional filename (without extension).
    """
    out_dir = _ensure_output_dir()
    if filename is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{ts}"

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html.j2")

    # Gather charts from state
    artifacts = tool_context.state.get("report_artifacts", {})
    charts = artifacts.get("charts", [])

    html_content = template.render(
        title=title,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sections=sections,
        charts=charts,
    )

    html_path = out_dir / f"{filename}.html"
    html_path.write_text(html_content, encoding="utf-8")

    # Attempt PDF generation via WeasyPrint
    pdf_path = None
    try:
        from weasyprint import HTML
        pdf_path = str(out_dir / f"{filename}.pdf")
        HTML(string=html_content).write_pdf(pdf_path)
    except Exception as e:
        logger.warning("PDF generation failed (WeasyPrint): %s", e)
        pdf_path = None

    artifacts["html_report"] = str(html_path)
    if pdf_path:
        artifacts["pdf_report"] = pdf_path
    tool_context.state["report_artifacts"] = artifacts

    result = {"html_path": str(html_path), "format": "html"}
    if pdf_path:
        result["pdf_path"] = pdf_path
        result["format"] = "html+pdf"
    return result
