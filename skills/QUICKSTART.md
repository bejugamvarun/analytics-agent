# Skills Quick Reference

## What Are Skills?

Skills are **modular knowledge packages** that agents can load on-demand. Think of them as:
- 📚 **Textbooks** that agents can reference when needed
- 🧩 **Plugins** that add domain expertise
- 📦 **Microservices** for agent capabilities

## Key Benefits

### 1. **Context Window Optimization**
- ✅ Load instructions only when needed
- ✅ Keep agent prompts concise
- ✅ Scale to more complex domains

### 2. **Knowledge Reusability**
- ✅ Share skills across multiple agents
- ✅ Single source of truth for domain logic
- ✅ No duplication of instructions

### 3. **Better Organization**
- ✅ Separate code from knowledge
- ✅ Version control for domain expertise
- ✅ Easy updates without code changes

## Quick Start

### Load a Skill

```python
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset
import pathlib

# Load from directory
skill = load_skill_from_dir(pathlib.Path("skills/my_skill"))

# Create toolset
toolset = skill_toolset.SkillToolset(skills=[skill])

# Add to agent
agent = LlmAgent(
    name="my_agent",
    tools=[toolset, ...other_tools],
    ...
)
```

### Create a Skill

```bash
# Directory structure
my_skill/
  SKILL.md          # Required: metadata + instructions
  references/       # Optional: detailed docs
    guide.md
  assets/           # Optional: schemas, templates
    schema.sql
```

```markdown
<!-- SKILL.md -->
---
name: my-skill
description: What it does
version: 1.0.0
tags: [domain, category]
---

# Skill Title

## Purpose
One sentence describing what this enables

## When to Use
- Scenario 1
- Scenario 2

## Instructions
Step 1: ...
Step 2: ...
Step 3: ...

## Output Format
Expected structure
```

## Skills in This Project

| Skill | Purpose | Used By | Files |
|-------|---------|---------|-------|
| **mlo_analysis** | MLO variance analysis & regulatory metrics | variance_analysis_agent | SKILL.md<br>references/mlo_calculations.md<br>assets/mlo_schema.sql |
| **anomaly_detection** | Statistical anomaly detection in time-series | anomaly_detection_agent | SKILL.md<br>references/statistical_methods.md |

## Common Patterns

### Pattern 1: Domain Calculations

**Use case**: Complex formulas with business rules

```
skill/
  SKILL.md         → High-level process
  references/
    formulas.md    → Detailed calculations
    edge_cases.md  → Special scenarios
  assets/
    examples.json  → Sample inputs/outputs
```

### Pattern 2: Data Schema Knowledge

**Use case**: Database query assistance

```
skill/
  SKILL.md         → Query patterns and best practices
  assets/
    schema.sql     → Table structures
    examples.sql   → Common queries
```

### Pattern 3: Regulatory Compliance

**Use case**: Policy enforcement

```
skill/
  SKILL.md         → Compliance steps
  references/
    regulations.md → Regulatory requirements
    thresholds.md  → Limits and triggers
  assets/
    templates/     → Report templates
```

## Testing Skills

```bash
# Run the test script
cd risk_analytics_agent
python skills/test_skills.py
```

**Expected output**:
```
✅ Skills loaded: 2/2
✅ SkillToolset created successfully
✅ All agent imports successful
🎉 All tests passed! Skills are ready to use.
```

## Debugging

### Skill Not Loading?

```python
# Check path
import pathlib
skill_path = pathlib.Path("skills/my_skill")
print(skill_path.exists())  # Should be True
print(list(skill_path.glob("*")))  # Should show SKILL.md

# Check SKILL.md syntax
# - Frontmatter must have '---' delimiters
# - name and description are required
# - YAML syntax must be valid
```

### Agent Not Using Skill?

- ✅ Check skill **description** matches the task
- ✅ Ensure skill **name** is descriptive
- ✅ Verify agent **instruction** mentions when to use skills
- ✅ Test with explicit prompts: "Use the [skill-name] skill to..."

### Import Errors?

```bash
# Check ADK version
pip show google-adk | grep Version
# Must be >= 1.25.0

# Update if needed
pip install --upgrade google-adk
```

## Best Practices

### ✅ DO

- **Keep L2 concise**: High-level steps only
- **Put details in L3**: Formulas go in references/
- **Use clear descriptions**: Help agents choose correctly
- **Version your skills**: Track changes over time
- **Test skill loading**: Run test_skills.py
- **Document trigger conditions**: When to use this skill

### ❌ DON'T

- **Don't put code in SKILL.md**: Use instructions, not Python
- **Don't make skills too broad**: One clear purpose per skill
- **Don't duplicate tools**: Skills are for knowledge, not actions
- **Don't skip frontmatter**: Metadata is required for discovery
- **Don't hardcode values**: Put configs in assets/

## Advanced: Inline Skills

For dynamic or programmatic skills:

```python
from google.adk.skills import models

skill = models.Skill(
    frontmatter=models.Frontmatter(
        name="dynamic-skill",
        description="Runtime-generated skill",
        version="1.0.0",
    ),
    instructions="""
    Step 1: Do X
    Step 2: Do Y
    """,
    resources=models.Resources(
        references={
            "guide.txt": "Reference content here",
        },
    ),
)
```

**When to use inline**:
- Skills generated from database configs
- User-specific customizations
- A/B testing different instructions
- Temporary/experimental skills

## Resources

- 📖 [Skills README](README.md) - Full implementation guide
- 🧪 [test_skills.py](test_skills.py) - Validation script
- 💡 [inline_skills_example.py](examples/inline_skills_example.py) - Code examples
- 🌐 [ADK Skills Docs](https://google.github.io/adk-docs/skills/index.md)
- 📋 [Agent Skills Spec](https://agentskills.io/specification)

## Troubleshooting Checklist

- [ ] ADK version >= 1.25.0
- [ ] SKILL.md exists with proper frontmatter
- [ ] Frontmatter has '---' delimiters
- [ ] Skill path resolves correctly
- [ ] Import statements include skill_toolset
- [ ] SkillToolset added to agent's tools list
- [ ] test_skills.py passes

## Next Steps

1. **Test current implementation**:
   ```bash
   python skills/test_skills.py
   ```

2. **Run your agent**:
   ```bash
   adk run src/risk_analytics_agent/orchestrator/agent.py
   ```

3. **Try a skills-based query**:
   ```
   "Calculate MLO variance between 2024-03-01 and 2024-03-15 
    at the entity level using your MLO analysis skill"
   ```

4. **Create new skills** for your other domains:
   - LCR calculations
   - NSFR reporting
   - Regulatory threshold monitoring
   - Data quality rules

---

**Questions?** Check the [full README](README.md) or [ADK documentation](https://google.github.io/adk-docs/).
