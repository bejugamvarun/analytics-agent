# Skills Implementation Guide

## Overview

This project now uses **Google ADK Skills** (v1.25.0+) to provide modular, self-contained capabilities to agents. Skills enable:

- **Context optimization**: Load instructions only when needed
- **Modularity**: Reusable knowledge packages across agents
- **Incremental loading**: L1 (metadata) → L2 (instructions) → L3 (resources)
- **Better organization**: Separate domain knowledge from code

## Skills Directory Structure

```
risk_analytics_agent/
├── skills/
│   ├── mlo_analysis/              # MLO variance analysis skill
│   │   ├── SKILL.md               # Main skill definition (L1 + L2)
│   │   ├── references/            # Detailed reference docs (L3)
│   │   │   └── mlo_calculations.md
│   │   └── assets/                # Schemas, templates (L3)
│   │       └── mlo_schema.sql
│   │
│   └── anomaly_detection/         # Statistical anomaly detection skill
│       ├── SKILL.md
│       └── references/
│           └── statistical_methods.md
```

## How Skills Work

### Three-Level Architecture

1. **L1 - Metadata** (Always loaded)
   - Skill name, description, tags
   - Helps agent decide which skill to activate
   - From frontmatter in SKILL.md

2. **L2 - Instructions** (Loaded when skill activated)
   - Step-by-step task instructions
   - Expected input/output formats
   - Error handling guidance
   - From body of SKILL.md

3. **L3 - Resources** (Loaded on-demand)
   - Detailed formulas and calculations
   - Database schemas and examples
   - Templates and reference materials
   - From references/ and assets/ directories

### Loading Process

```python
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset
import pathlib

# Load skill from directory
skill = load_skill_from_dir(
    pathlib.Path(__file__).parent / "skills" / "mlo_analysis"
)

# Create toolset
skillset = skill_toolset.SkillToolset(skills=[skill])

# Add to agent
agent = LlmAgent(
    name="my_agent",
    tools=[skillset, ...other_tools],
    ...
)
```

## Implemented Skills

### 1. MLO Analysis Skill

**Purpose**: Comprehensive MLO variance analysis and regulatory reporting

**When to use**:
- Day-over-day variance calculations
- Material change identification
- DESCIFR stress scenario analysis
- Regulatory metric computation

**Resources**:
- `mlo_calculations.md`: Formulas, thresholds, hierarchies
- `mlo_schema.sql`: Database schema reference

**Used by**: `variance_analysis_agent`

### 2. Anomaly Detection Skill

**Purpose**: Statistical anomaly detection in time-series liquidity data

**When to use**:
- Data quality validation
- Automated surveillance
- Outlier investigation
- Pattern break detection

**Methods**:
- Z-score analysis
- Interquartile Range (IQR)
- Time-series decomposition
- Moving average envelopes

**Resources**:
- `statistical_methods.md`: Detailed formulas and implementation

**Used by**: `anomaly_detection_agent`

## Creating New Skills

### Method 1: File-Based Skills (Recommended)

1. **Create skill directory**:
   ```bash
   mkdir -p skills/my_new_skill/references
   mkdir -p skills/my_new_skill/assets
   ```

2. **Create SKILL.md**:
   ```markdown
   ---
   name: my-skill
   description: What this skill does
   version: 1.0.0
   tags: [tag1, tag2]
   ---

   # Skill Name

   ## Purpose
   What problem this solves

   ## When to Use
   Specific scenarios

   ## Instructions
   Step-by-step task breakdown

   ## Output Format
   Expected structure
   ```

3. **Add references** (optional):
   - Detailed docs in `references/*.md`
   - Schemas/templates in `assets/*`

4. **Load in agent**:
   ```python
   skill = load_skill_from_dir(Path("skills/my_new_skill"))
   ```

### Method 2: Inline Skills

For dynamic or programmatically-generated skills:

```python
from google.adk.skills import models

my_skill = models.Skill(
    frontmatter=models.Frontmatter(
        name="dynamic-skill",
        description="Description here",
        version="1.0.0",
    ),
    instructions="""
    Step 1: Do this
    Step 2: Do that
    Step 3: Return result
    """,
    resources=models.Resources(
        references={
            "guide.md": "Reference content here",
            "example.txt": "Example data",
        },
        assets={
            "schema.sql": "CREATE TABLE...",
        },
    ),
)

skillset = skill_toolset.SkillToolset(skills=[my_skill])
```

## Benefits in This Project

### Before Skills
- Instructions embedded in agent prompts
- Large context windows always loaded
- Duplicate knowledge across agents
- Hard to maintain complex domain logic

### After Skills
- Domain knowledge externalized and reusable
- Instructions loaded only when needed
- Single source of truth for calculations
- Easy to update formulas and thresholds
- Better separation of concerns

## Best Practices

1. **Keep L2 instructions concise**: Step-by-step, high-level only
2. **Put details in L3 references**: Formulas, edge cases, examples
3. **Use descriptive skill names**: Help agents choose correctly
4. **Version your skills**: Track changes over time
5. **Test skill loading**: Ensure paths resolve correctly
6. **Document when to use**: Clear trigger conditions

## Example: Agent Using Skills

```python
# variance_analysis_agent.py
import pathlib
from google.adk.agents import LlmAgent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

# Load skill
mlo_skill = load_skill_from_dir(
    pathlib.Path(__file__).parent.parent.parent / "skills" / "mlo_analysis"
)

# Create toolset
skillset = skill_toolset.SkillToolset(skills=[mlo_skill])

# Define agent with skill + existing tools
agent = LlmAgent(
    name="variance_agent",
    model=model,
    instruction="You analyze variances in liquidity metrics...",
    tools=[
        skillset,              # Skill for domain knowledge
        compute_variance,      # Function tool for computation
        fetch_data,           # Function tool for data access
    ],
)
```

## Known Limitations

- ⚠️ **Script execution not supported**: `scripts/` directory content cannot be executed yet
- 🧪 **Experimental feature**: API may change in future versions
- 📦 **Python only**: Skills currently only in ADK Python v1.25.0+

## Additional Resources

- [ADK Skills Documentation](https://google.github.io/adk-docs/skills/index.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ADK Skills Sample Code](https://github.com/google/adk-python/tree/main/contributing/samples/skills_agent)

## Troubleshooting

### Skill not loading
Check path resolution:
```python
print(mlo_skill_path.exists())  # Should be True
print(list(mlo_skill_path.glob("*")))  # Should show SKILL.md
```

### Import errors
Ensure ADK version:
```bash
pip show google-adk | grep Version  # Should be >= 1.25.0
```

### Agent not using skill
- Check skill description in frontmatter
- Ensure skill name is relevant to task
- Review agent instruction for skill context
