"""
Example: Creating and using inline Skills in ADK agents.

This module demonstrates how to define Skills programmatically
rather than loading from files.
"""

import pathlib

from google.adk.agents import LlmAgent
from google.adk.skills import load_skill_from_dir, models
from google.adk.tools import skill_toolset


def create_inline_skill_example():
    """Example of creating a skill inline using the models API."""
    
    # Define a skill programmatically
    sql_safety_skill = models.Skill(
        frontmatter=models.Frontmatter(
            name="sql-safety-validator",
            description=(
                "Validates SQL queries for safety, ensuring only SELECT statements "
                "are executed against production databases"
            ),
            version="1.0.0",
            author="Risk Analytics Team",
            tags=["security", "sql", "validation"],
        ),
        instructions="""
# SQL Safety Validation

## Purpose
Prevent destructive SQL operations against production databases by validating
queries before execution.

## Instructions

### Step 1: Parse the SQL Query
Extract the SQL statement type from the query string.

### Step 2: Check for Forbidden Operations
Reject queries containing:
- DDL: CREATE, ALTER, DROP, TRUNCATE
- DML: INSERT, UPDATE, DELETE, MERGE
- DCL: GRANT, REVOKE
- TCL: COMMIT, ROLLBACK, SAVEPOINT

### Step 3: Validate SELECT Queries
For SELECT queries, ensure:
- No subqueries with DML operations
- No function calls that modify state
- No EXECUTE/EXEC statements
- Row limit does not exceed 100,000

### Step 4: Return Validation Result
Output:
```json
{
    "is_safe": true/false,
    "query_type": "SELECT|DML|DDL|OTHER",
    "violations": ["list of issues if any"],
    "recommendation": "suggestion if unsafe"
}
```

## Safety Rules
- Only SELECT queries are allowed
- Queries must include LIMIT clause (<= 100,000 rows)
- No nested DML in subqueries
- No dynamic SQL execution
        """,
        resources=models.Resources(
            references={
                "allowed_patterns.txt": """
# Allowed SQL Patterns

✅ SELECT col1, col2 FROM table WHERE condition LIMIT 1000
✅ SELECT * FROM table1 JOIN table2 ON ... LIMIT 500
✅ SELECT COUNT(*) FROM table
✅ SELECT AVG(amount) FROM transactions WHERE date = ...

❌ DELETE FROM table WHERE ...
❌ UPDATE table SET col = ...
❌ CREATE TABLE ...
❌ DROP TABLE ...
❌ INSERT INTO table VALUES (...)
❌ SELECT * FROM table (no LIMIT)
❌ SELECT * FROM (DELETE FROM ...) AS subq  -- DML in subquery
                """,
                "enforcement_policy.md": """
# SQL Safety Enforcement Policy

## Production Databases
- Read-only access enforced at application layer
- All queries validated before submission
- Query results cached when possible
- Audit log for all database access

## Development Databases
- Full access for authorized developers
- Safety validation optional but recommended
- Separate credentials and connection strings

## Emergency Override
Contact: data-platform-team@company.com
Process: Submit ticket with business justification
Approval: Requires VP+ sign-off
                """,
            },
            assets={
                "deny_list.json": '{"forbidden_keywords": ["DELETE", "DROP", "TRUNCATE", "INSERT", "UPDATE"]}',
            },
        ),
    )
    
    return sql_safety_skill


def create_agent_with_inline_skill():
    """Example agent that uses an inline skill."""
    
    # Create inline skill
    sql_skill = create_inline_skill_example()
    
    # Create skill toolset
    sql_skillset = skill_toolset.SkillToolset(skills=[sql_skill])
    
    # Create agent with the skill
    agent = LlmAgent(
        name="safe_sql_agent",
        model="gemini-2.0-flash-exp",
        instruction=(
            "You are a database query assistant. Before executing any SQL, "
            "use your SQL safety skill to validate the query. Only proceed "
            "with safe, read-only SELECT queries."
        ),
        description="Executes validated, safe SQL queries against production databases",
        tools=[sql_skillset],
    )
    
    return agent


def create_agent_with_multiple_skills():
    """Example of an agent using both file-based and inline skills."""
    
    # Load file-based skill
    mlo_skill_path = pathlib.Path(__file__).parent / "skills" / "mlo_analysis"
    mlo_skill = load_skill_from_dir(mlo_skill_path)
    
    # Create inline skill
    sql_skill = create_inline_skill_example()
    
    # Another inline skill - date handling
    date_handling_skill = models.Skill(
        frontmatter=models.Frontmatter(
            name="treasury-date-handling",
            description="Handles business day calculations and treasury calendar logic",
            version="1.0.0",
        ),
        instructions="""
# Treasury Date Handling

## Purpose
Calculate business days, skip holidays, and handle treasury-specific date logic.

## Instructions
1. Check if date is a valid business day (Mon-Fri, not a holiday)
2. If weekend/holiday, find next valid business day
3. For lookback periods, count only business days
4. Handle month-end and quarter-end special rules

## Output Format
```json
{
    "input_date": "2024-03-15",
    "is_business_day": true,
    "next_business_day": "2024-03-15",
    "prior_business_day": "2024-03-14"
}
```
        """,
        resources=models.Resources(
            references={
                "holidays.txt": "2024-01-01: New Year's Day\n2024-07-04: Independence Day\n...",
            }
        ),
    )
    
    # Combine multiple skills into one toolset
    combined_skillset = skill_toolset.SkillToolset(
        skills=[mlo_skill, sql_skill, date_handling_skill]
    )
    
    # Create agent with multiple skills
    agent = LlmAgent(
        name="comprehensive_liquidity_agent",
        model="gemini-2.0-flash-exp",
        instruction=(
            "You are a comprehensive liquidity analysis agent. "
            "Use your skills for MLO analysis, SQL safety, and date handling "
            "to provide accurate, safe, and context-aware liquidity insights."
        ),
        description="Full-featured liquidity analysis with safety and domain expertise",
        tools=[combined_skillset],
    )
    
    return agent


def dynamic_skill_generation_example(metric_name: str, calculation_formula: str):
    """Example of dynamically generating a skill based on parameters."""
    
    skill = models.Skill(
        frontmatter=models.Frontmatter(
            name=f"{metric_name.lower().replace(' ', '-')}-calculator",
            description=f"Calculates {metric_name} for liquidity reporting",
            version="1.0.0",
        ),
        instructions=f"""
# {metric_name} Calculator

## Purpose
Calculate {metric_name} according to regulatory requirements.

## Formula
{calculation_formula}

## Instructions
1. Retrieve required input data
2. Apply the formula
3. Round to 2 decimal places
4. Return result with metadata

## Output Format
```json
{{
    "metric_name": "{metric_name}",
    "value": <number>,
    "calculation_date": "<date>",
    "formula_used": "{calculation_formula}"
}}
```
        """,
    )
    
    return skill


# Example usage
if __name__ == "__main__":
    # Example 1: Simple inline skill
    print("Example 1: Creating inline skill")
    skill = create_inline_skill_example()
    print(f"Created skill: {skill.frontmatter.name}")
    
    # Example 2: Dynamic skill generation
    print("\nExample 2: Dynamic skill generation")
    lcr_skill = dynamic_skill_generation_example(
        metric_name="Liquidity Coverage Ratio (LCR)",
        calculation_formula="LCR = HQLA / Net Cash Outflows * 100"
    )
    print(f"Generated skill: {lcr_skill.frontmatter.name}")
    
    # Example 3: Agent with skills
    print("\nExample 3: Creating agent with skills")
    agent = create_agent_with_inline_skill()
    print(f"Created agent: {agent.name} with {len(agent.tools)} tool(s)")
