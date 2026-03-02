---
name: mlo-analysis
description: Analyzes Modeled Liquidity Outflow (MLO) metrics, calculates variances, and identifies patterns in treasury liquidity data
version: 1.0.0
author: Risk Analytics Team
tags:
  - liquidity
  - mlo
  - variance-analysis
  - regulatory-reporting
---

# MLO Analysis Skill

## Purpose
This skill enables comprehensive analysis of Modeled Liquidity Outflow (MLO) data, including day-over-day variance calculation, trend identification, and regulatory metric computation.

## When to Use This Skill
- Calculate MLO variances between reporting dates
- Analyze liquidity trends at CUSIP, FLB, or entity level
- Identify significant outflow changes requiring investigation
- Generate regulatory compliance reports

## Instructions

### Step 1: Data Validation
- Verify that required date parameters are provided (current_date, prior_date)
- Ensure hierarchy level is specified (CUSIP, FLB, Entity)
- Validate Snowflake connection is available

### Step 2: Query MLO Data
- Retrieve MLO values for both current and prior dates
- Apply appropriate filters based on hierarchy level
- Include relevant dimensions (product type, entity, geography)

### Step 3: Calculate Variances
- Compute absolute variance: current_mlo - prior_mlo
- Calculate percentage variance: (variance / prior_mlo) * 100
- Identify materiality threshold breaches (default: >5% or >$10M)

### Step 4: Analyze Patterns
- Group variances by contributing factors
- Identify top movers (largest increases/decreases)
- Flag anomalies requiring deeper investigation

### Step 5: Generate Insights
- Summarize key findings
- Highlight risk implications
- Suggest drill-down areas for further analysis

## Expected Output Format
```json
{
  "summary": {
    "total_variance": <number>,
    "variance_pct": <number>,
    "material_changes": <count>
  },
  "top_movers": [
    {
      "identifier": "<cusip/flb/entity>",
      "variance": <number>,
      "variance_pct": <number>,
      "prior_value": <number>,
      "current_value": <number>
    }
  ],
  "risk_flags": [<list of concerns>],
  "recommended_actions": [<list of next steps>]
}
```

## Error Handling
- If data is missing for requested dates, notify user and suggest alternative dates
- If variance calculation fails, check for zero/null prior values
- Log all database errors for debugging

## References
See `references/mlo_calculations.md` for detailed formulas and `assets/mlo_schema.sql` for database schema.
