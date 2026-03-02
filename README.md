# Risk Analytics Agent

**Google ADK multi-agent system for financial liquidity risk analytics**

A sophisticated AI-powered agent system built with Google's Agent Development Kit (ADK) for analyzing liquidity risk metrics, detecting anomalies, and generating regulatory reports.

## 🎯 Overview

This application implements a multi-agent architecture using Google ADK, featuring:

- **📊 Liquidity Analysis**: MLO (Modeled Liquidity Outflow) variance analysis
- **🔍 Anomaly Detection**: Statistical methods (Z-score, IQR, time-series)
- **📈 Quantitative Analysis**: Risk metrics and regulatory calculations
- **🗃️ Data Retrieval**: Safe SQL query generation and execution
- **📄 Report Generation**: Automated HTML/PDF/Markdown reports
- **🧠 Skills System**: Modular knowledge packages (ADK 1.25.0+)

## 🏗️ Architecture

```
Orchestrator Agent (Root)
├── Schema Discovery Agent
├── Data Retrieval Agent
├── Quantitative Analysis Agent
├── Variance Analysis Agent (+ MLO Analysis Skill)
├── Drilldown Analysis Agent
├── Anomaly Detection Agent (+ Anomaly Detection Skill)
└── Report Generation Agent
```

Each agent specializes in a specific domain and can be invoked directly or through the orchestrator.

## ✨ Features

### Multi-Agent Orchestration
- Hierarchical agent delegation
- LLM-driven routing and task decomposition
- Sub-agent coordination

### Skills System (NEW!)
- **MLO Analysis Skill**: Variance calculations, materiality thresholds, DESCIFR scenarios
- **Anomaly Detection Skill**: Statistical methods and ensemble scoring
- Incremental knowledge loading (L1→L2→L3)
- Reusable across agents

### Data Integration
- Snowflake database connectivity
- Safe SQL generation (read-only enforcement)
- Schema introspection
- Query validation

### Analysis Capabilities
- Day-over-day variance analysis
- Multi-hierarchy support (CUSIP, FLB, Entity)
- Stress scenario analysis (Baseline, Moderate, Severe, Idiosyncratic)
- Pattern detection and anomaly identification

### Reporting
- Multiple formats (HTML, PDF, Markdown)
- Template-based generation
- Chart and visualization support

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (you have 3.13 ✅)
- Virtual environment
- Google API key (for Gemini models)
- Snowflake credentials (optional, for database features)

### Installation

```powershell
# 1. Clone the repository (if not already)
cd risk_analytics_agent

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -e .

# Or install specific packages
pip install google-adk>=1.25.0 snowflake-connector-python>=3.12.0 polars>=1.0.0
```

### Configuration

Create a `.env` file in the project root:

```env
# Required: Google AI API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role
```

### Running

#### Interactive CLI (Recommended)
```powershell
python main.py
```

#### Single Query Mode
```powershell
python main.py "What can you help me with?"
```

#### ADK Web UI (Browser-based)
```powershell
adk web src/risk_analytics_agent/agent.py
```

#### ADK Command Line
```powershell
adk run src/risk_analytics_agent/agent.py
```

See **[RUNNING_THE_APP.md](RUNNING_THE_APP.md)** for detailed running instructions.

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[RUNNING_THE_APP.md](RUNNING_THE_APP.md)** | Complete guide on running the application |
| **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** | App + InMemoryRunner migration details |
| **[SKILLS_IMPLEMENTATION.md](SKILLS_IMPLEMENTATION.md)** | Skills feature overview and benefits |
| **[skills/README.md](skills/README.md)** | Skills implementation guide |
| **[skills/QUICKSTART.md](skills/QUICKSTART.md)** | Quick reference for Skills |

## 🧩 Project Structure

```
risk_analytics_agent/
├── src/
│   └── risk_analytics_agent/
│       ├── agent.py                # Root agent + App definition
│       ├── app.py                  # Application runner (InMemoryRunner)
│       ├── config.py               # Configuration management
│       ├── models.py               # Model selection logic
│       ├── snowflake_client.py     # Database client
│       │
│       ├── orchestrator/           # Root orchestrator agent
│       │   ├── agent.py
│       │   └── prompt.py
│       │
│       └── sub_agents/             # Specialized sub-agents
│           ├── schema_discovery/
│           ├── data_retrieval/
│           ├── quantitative_analysis/
│           ├── variance_analysis/   # Uses MLO Analysis Skill
│           ├── drilldown_analysis/
│           ├── anomaly_detection/   # Uses Anomaly Detection Skill
│           └── report_generation/
│
├── skills/                          # ADK Skills (domain knowledge)
│   ├── mlo_analysis/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── mlo_calculations.md
│   │   └── assets/
│   │       └── mlo_schema.sql
│   │
│   ├── anomaly_detection/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── statistical_methods.md
│   │
│   ├── README.md
│   ├── QUICKSTART.md
│   └── test_skills.py
│
├── main.py                         # Application entry point
├── test_app_runner.py             # Runner tests
├── pyproject.toml                 # Dependencies
└── adk.yaml                       # ADK configuration
```

## 🛠️ Technology Stack

- **Google ADK**: Agent orchestration and runtime
- **Gemini 2.0 Flash**: LLM for agent reasoning
- **Snowflake**: Data warehouse integration
- **Polars**: High-performance data processing
- **Jinja2**: Template-based reporting
- **Matplotlib/Plotly**: Visualizations

## 💡 Usage Examples

### Example 1: MLO Variance Analysis

```powershell
python main.py "Calculate MLO variance between March 1 and March 15 at entity level"
```

The orchestrator will:
1. Route to **variance_analysis_agent**
2. Load **MLO Analysis Skill** (formulas, thresholds)
3. Execute **data_retrieval_agent** to fetch data
4. Apply variance calculations
5. Return formatted analysis

### Example 2: Anomaly Detection

```powershell
python main.py "Detect anomalies in yesterday's liquidity outflows"
```

The orchestrator will:
1. Route to **anomaly_detection_agent**
2. Load **Anomaly Detection Skill** (statistical methods)
3. Retrieve historical data
4. Apply Z-score, IQR, and time-series analysis
5. Generate alerts with severity scores

### Example 3: Schema Discovery

```powershell
python main.py "What tables and columns are available in the liquidity schema?"
```

The orchestrator routes to **schema_discovery_agent** for introspection.

### Example 4: Generate Report

```powershell
python main.py "Generate a liquidity risk report for this week in HTML format"
```

The orchestrator will:
1. Coordinate multiple agents for data gathering
2. Perform analysis (variance, anomalies, trends)
3. Route to **report_generation_agent**
4. Create formatted HTML report

## 🧪 Testing

### Test Skills Implementation
```powershell
python skills/test_skills.py
```

### Test App Runner
```powershell
python test_app_runner.py
```

### Run ADK Evaluation
```powershell
adk eval --dataset test_cases.yaml src/risk_analytics_agent/agent.py
```

## 🔬 Development

### Add a New Agent

1. Create agent directory in `sub_agents/`
2. Define agent with `LlmAgent` class
3. Create tools (functions) for the agent
4. Write system instruction/prompt
5. Register in orchestrator's `sub_agents` list

### Create a New Skill

1. Create directory in `skills/`
2. Add `SKILL.md` with frontmatter and instructions
3. Add references in `references/` (optional)
4. Add assets in `assets/` (optional)
5. Load in agent: `load_skill_from_dir(path)`
6. Add to agent's tools: `SkillToolset(skills=[skill])`

See [skills/README.md](skills/README.md) for details.

### Configuration

Edit `src/risk_analytics_agent/config/models.yaml` to configure model selection:

```yaml
orchestrator_agent:
  model_name: "gemini-2.0-flash-exp"
  temperature: 0.7
  
variance_analysis_agent:
  model_name: "gemini-2.0-flash-exp"
  temperature: 0.3
```

## 📊 Use Cases

- **Treasury Operations**: Daily liquidity monitoring
- **Risk Management**: Variance analysis and anomaly detection
- **Regulatory Reporting**: LCR, NSFR, and DESCIFR compliance
- **Data Quality**: Automated validation and monitoring
- **Executive Reporting**: Automated dashboards and insights

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional sub-agents (e.g., forecasting, stress testing)
- New Skills (LCR calculations, NSFR rules, etc.)
- Enhanced visualizations
- Integration with other data sources
- Evaluation datasets

## 📝 License

MIT License - see LICENSE file for details

## 🔗 Resources

### Google ADK
- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python GitHub](https://github.com/google/adk-python)
- [ADK Release Notes](https://github.com/google/adk-python/releases)

### Skills
- [Skills Documentation](https://google.github.io/adk-docs/skills/)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Skills Sample Code](https://github.com/google/adk-python/tree/main/contributing/samples/skills_agent)

### Models
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)

## 🆘 Troubleshooting

### "No module named 'google.adk'"
```powershell
pip install google-adk>=1.25.0
```

### Skills Not Loading
```powershell
# Check ADK version
pip show google-adk

# Test skills
python skills/test_skills.py
```

### Snowflake Connection Issues
- Verify credentials in `.env`
- Check network connectivity
- Ensure warehouse is running

### API Key Issues
- Verify `GOOGLE_API_KEY` in `.env`
- Check quota limits
- Ensure API is enabled

## 📧 Support

For issues or questions:
- Check the [documentation](RUNNING_THE_APP.md)
- Review [troubleshooting guide](MIGRATION_SUMMARY.md#troubleshooting)
- Open an issue on the repository

---

**Built with ❤️ using Google ADK**
