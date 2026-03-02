# Statistical Anomaly Detection Methods

## Z-Score Method

### Formula
```
Z = (X - μ) / σ

Where:
  X = observed value
  μ = mean of historical values
  σ = standard deviation of historical values
```

### Interpretation
- |Z| < 2: Normal variation
- 2 ≤ |Z| < 3: Moderate anomaly
- |Z| ≥ 3: Significant anomaly (typically < 0.3% probability)

### Implementation Notes
- Use rolling window to adapt to changing conditions
- Consider Welford's method for numerically stable online calculation
- Remove previous anomalies from baseline calculation

## Interquartile Range (IQR) Method

### Formula
```
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR

Where:
  Q1 = 25th percentile
  Q3 = 75th percentile
```

### Advantages
- Robust to outliers in historical data
- No assumption of normal distribution
- Effective for skewed distributions

### Tuning
- Use 1.5 multiplier for typical outliers
- Use 3.0 multiplier for extreme outliers only
- Adjust based on business tolerance

## Seasonal Decomposition

### STL Method (Seasonal and Trend decomposition using Loess)
```
Y(t) = T(t) + S(t) + R(t)

Where:
  Y(t) = observed value at time t
  T(t) = trend component
  S(t) = seasonal component
  R(t) = residual (anomalies appear here)
```

### Process
1. Remove trend using LOESS smoothing
2. Extract seasonal pattern (daily, weekly, monthly)
3. Analyze residuals for anomalies
4. Apply Z-score or IQR to residuals

## Ensemble Approach

### Voting System
Combine multiple methods for robust detection:

```python
def anomaly_confidence(value, methods_results):
    score = 0
    if methods_results['z_score'] > 3:
        score += 3
    if methods_results['iqr_outlier']:
        score += 2
    if methods_results['ts_residual'] > threshold:
        score += 2
    if methods_results['ma_envelope_breach']:
        score += 1
    
    return score / 8  # Normalize to 0-1
```

### Severity Classification
- Score 0.0-0.3: Normal
- Score 0.3-0.6: Monitor
- Score 0.6-0.8: Investigate
- Score 0.8-1.0: Critical Alert

## Time-Series Specific Techniques

### ARIMA Residuals
1. Fit ARIMA model to historical data
2. Generate forecasts
3. Flag large forecast errors as anomalies

### Exponential Smoothing
```
Forecast(t+1) = α × Y(t) + (1-α) × Forecast(t)

Anomaly if: |Y(t) - Forecast(t)| > threshold
```

## Context-Aware Adjustments

### Business Calendar
Ignore or adjust thresholds for:
- Month-end / quarter-end
- Reporting deadlines
- Market holidays
- Known corporate events

### Volatility Regimes
Adjust detection sensitivity based on market conditions:
- Low volatility: Tighter thresholds
- High volatility (crisis): Looser thresholds
- Use VIX or similar as regime indicator

## Performance Considerations

### For Large Datasets
- Use approximate quantiles (t-digest) for IQR
- Calculate Z-scores in batches
- Pre-aggregate to appropriate time granularity
- Cache statistical summaries

### Real-Time Detection
- Maintain running statistics (Welford's algorithm)
- Use exponential moving averages
- Implement streaming anomaly detection
- Set appropriate update frequencies
