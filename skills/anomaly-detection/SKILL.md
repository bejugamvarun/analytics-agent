---
name: anomaly-detection
description: Detects statistical anomalies in liquidity metrics using Z-score, IQR, and time-series analysis techniques
version: 1.0.0
author: Risk Analytics Team
tags:
  - anomaly-detection
  - statistical-analysis
  - outliers
  - time-series
---

# Anomaly Detection Skill

## Purpose
Identify unusual patterns, outliers, and statistical anomalies in liquidity data that may indicate data quality issues, operational problems, or emerging risks.

## When to Use This Skill
- Automated surveillance of daily liquidity metrics
- Data quality validation after batch processing
- Investigation of unexpected variance results
- Proactive risk monitoring

## Statistical Methods

### Method 1: Z-Score Analysis
Calculate standard deviations from mean:
- Flag values > 3 standard deviations as outliers
- Use rolling 90-day window for baseline calculation
- Best for normally distributed metrics

### Method 2: Interquartile Range (IQR)
Detect outliers using quartile-based boundaries:
- Calculate Q1, Q3, and IQR = Q3 - Q1
- Flag values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR
- Robust to non-normal distributions

### Method 3: Time Series Decomposition
Identify trend and seasonal anomalies:
- Decompose series into trend, seasonal, and residual components
- Analyze residuals for unexpected deviations
- Best for identifying pattern breaks

### Method 4: Moving Average Envelope
Track deviations from rolling average:
- Calculate N-day moving average and standard deviation
- Flag values outside ±2σ envelope
- Effective for trending metrics

## Instructions

### Step 1: Collect Historical Data
Retrieve at least 90 days of historical values for the metric being analyzed.

### Step 2: Apply Statistical Tests
Run multiple anomaly detection methods and compare results.

### Step 3: Calculate Anomaly Scores
Assign severity scores (1-10) based on:
- Magnitude of deviation
- Number of methods flagging the value
- Business impact of the metric
- Historical precedent

### Step 4: Contextualize Findings
Check for:
- Known corporate actions (acquisitions, divestitures)
- Market events (crisis periods)
- Data quality issues (missing data, late feeds)
- System changes (calculation updates)

### Step 5: Generate Alert
Produce human-readable explanation with:
- What is anomalous
- Why it's unusual (statistical basis)
- Potential causes
- Recommended actions

## Output Format
```json
{
  "anomalies_detected": <count>,
  "critical_alerts": [
    {
      "metric": "<metric_name>",
      "date": "<date>",
      "value": <number>,
      "expected_range": [<lower>, <upper>],
      "deviation_magnitude": <number>,
      "severity_score": <1-10>,
      "detection_methods": [<list>],
      "possible_causes": [<list>],
      "recommended_actions": [<list>]
    }
  ]
}
```

## Configurable Parameters
- `lookback_days`: Historical window (default: 90)
- `z_threshold`: Z-score cutoff (default: 3.0)
- `iqr_multiplier`: IQR boundary multiplier (default: 1.5)
- `min_severity_score`: Alert threshold (default: 7)

## References
See `references/statistical_methods.md` for detailed formulas and implementation notes.
