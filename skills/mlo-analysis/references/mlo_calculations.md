# MLO Calculation Reference

## Core Formulas

### Absolute Variance
```
Variance = MLO_Current - MLO_Prior
```

### Percentage Variance
```
Variance_Pct = (Variance / MLO_Prior) × 100
```

### Materiality Thresholds
- **Quantitative**: Absolute variance > $10,000,000
- **Relative**: Percentage variance > 5%
- **Combined**: Either threshold triggers material classification

## DESCIFR Stress Scenarios

MLO calculations must consider the following stress scenarios:
- **Baseline**: Normal operating conditions
- **Moderate Stress**: 1-in-10 year event
- **Severe Stress**: 1-in-100 year event
- **Idiosyncratic**: Firm-specific crisis scenario

## Hierarchy Levels

### CUSIP Level
Most granular level - individual security identifier
- Use for detailed position analysis
- Aggregate to FLB for risk reporting

### FLB (Functional Line of Business)
- Business unit grouping
- Primary level for management reporting
- Roll up to entity for regulatory reporting

### Entity Level
- Legal entity consolidated view
- Regulatory reporting level
- Used for LCR, NSFR calculations

## Time Periods

### Standard Reporting Dates
- T+0: Current reporting date
- T-1: Prior business day (variance analysis)
- T-30: Month-over-month comparison
- T-90: Quarter-over-quarter trends

### Data Freshness
- Real-time intraday updates available
- End-of-day final calculations at 5 PM ET
- Historical snapshots retained for 5 years

## Data Quality Checks

Before calculating variances, verify:
1. Both dates have complete data loads
2. No batch processing errors occurred
3. Adjustment factors applied consistently
4. Manual overrides documented
5. Reconciliation to source systems passed
