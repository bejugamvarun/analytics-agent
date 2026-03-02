# Reasoning Model Configuration Guide

## Overview

Your application now supports **reasoning models** through LiteLLM, including:
- OpenAI o1/o1-mini/o1-preview
- DeepSeek R1/DeepSeek Reasoner
- Any other reasoning-capable models

## What Are Reasoning Models?

Reasoning models spend extra compute time "thinking" before responding, which makes them excellent for:
- ✅ Complex quantitative analysis
- ✅ Multi-step mathematical calculations
- ✅ Logical reasoning and planning
- ✅ Financial modeling and risk analysis
- ✅ Anomaly detection with deep reasoning

## Configuration

### Basic Reasoning Model Setup

Edit `src/risk_analytics_agent/config/models.yaml`:

```yaml
agents:
  quantitative_analysis_agent:
    provider: openai
    model_name: o1-preview          # or o1-mini, o1
    reasoning_effort: high           # Options: low, medium, high
    supports_reasoning: true         # Important: flags reasoning model
    max_completion_tokens: 32768     # o1 uses this instead of max_tokens
    api_key: ${OPENAI_API_KEY}
    # Note: Don't set temperature - o1 models don't support it
```

### Per-Agent Reasoning Models

Use different reasoning models for specific tasks:

```yaml
agents:
  # Heavy reasoning for complex quantitative work
  quantitative_analysis_agent:
    provider: openai
    model_name: o1-preview
    reasoning_effort: high
    supports_reasoning: true
    max_completion_tokens: 32768
    
  # Moderate reasoning for variance analysis
  variance_analysis_agent:
    provider: openai
    model_name: o1-mini
    reasoning_effort: medium
    supports_reasoning: true
    max_completion_tokens: 16384
    
  # Deep reasoning for anomaly detection
  anomaly_detection_agent:
    provider: openai
    model_name: o1
    reasoning_effort: high
    supports_reasoning: true
    max_completion_tokens: 32768
```

## Supported Reasoning Models

### 1. OpenAI o1 Series

**o1-preview** (Most capable)
```yaml
provider: openai
model_name: o1-preview
reasoning_effort: high
supports_reasoning: true
max_completion_tokens: 32768
api_key: ${OPENAI_API_KEY}
```

**o1-mini** (Faster, STEM focused)
```yaml
provider: openai
model_name: o1-mini
reasoning_effort: medium
supports_reasoning: true
max_completion_tokens: 65536
api_key: ${OPENAI_API_KEY}
```

**o1** (Latest)
```yaml
provider: openai
model_name: o1
reasoning_effort: high
supports_reasoning: true
max_completion_tokens: 100000
api_key: ${OPENAI_API_KEY}
```

**Pricing** (as of March 2026):
- o1-preview: $15/$60 per 1M tokens (input/output)
- o1-mini: $3/$12 per 1M tokens
- o1: $15/$60 per 1M tokens

### 2. DeepSeek R1

**DeepSeek Reasoner**
```yaml
provider: openai  # Uses OpenAI-compatible API
model_name: deepseek-reasoner
api_base: https://api.deepseek.com/v1
api_key: ${DEEPSEEK_API_KEY}
supports_reasoning: true
max_tokens: 8192
temperature: 0.7  # DeepSeek supports temperature
```

**Benefits**:
- Cost-effective ($0.55/$2.19 per 1M tokens)
- Strong reasoning capabilities
- Supports temperature control

### 3. Self-Hosted Reasoning Models

For on-premise deployment:

```yaml
provider: vllm  # or ollama
model_name: deepseek-r1-distill-llama-70b
api_base: http://your-server:8000/v1
api_key: your-key
supports_reasoning: true
max_tokens: 8192
```

## Key Parameters

### `reasoning_effort` (o1 models only)

Controls how much time the model spends reasoning:

- **`low`**: Faster, less thorough (~10-20 seconds)
- **`medium`**: Balanced (default, ~30-60 seconds)
- **`high`**: Most thorough, slower (~60-120 seconds)

**When to use high reasoning effort**:
- Complex financial calculations (LCR, NSFR)
- Multi-step variance analysis
- Regulatory compliance checks
- Anomaly root cause analysis

**When to use low/medium**:
- Simple data retrieval
- Schema discovery
- Quick calculations
- Formatting/reporting

### `supports_reasoning`

Set to `true` for reasoning models. This flag:
- **Removes `temperature`** (o1 doesn't support it)
- **Removes `top_p`** (o1 doesn't support it)
- Keeps `max_completion_tokens` and `reasoning_effort`
- Optimizes for reasoning model behavior

### `max_completion_tokens` vs `max_tokens`

- **`max_completion_tokens`**: Used by o1 models for output tokens
- **`max_tokens`**: Used by most other models
- The code handles both - just set the appropriate one

## Example Configurations

### Configuration 1: Hybrid Approach
Use reasoning models for complex tasks, standard models for simple ones:

```yaml
default:
  provider: openai
  model_name: gpt-4o
  temperature: 0.7
  max_tokens: 4096
  api_key: ${OPENAI_API_KEY}

agents:
  # Fast models for simple tasks
  schema_discovery_agent:
    model_name: gpt-4o-mini
    
  data_retrieval_agent:
    model_name: gpt-4o-mini
  
  # Reasoning models for complex analysis
  quantitative_analysis_agent:
    model_name: o1-preview
    reasoning_effort: high
    supports_reasoning: true
    max_completion_tokens: 32768
    
  variance_analysis_agent:
    model_name: o1-mini
    reasoning_effort: medium
    supports_reasoning: true
    max_completion_tokens: 16384
    
  anomaly_detection_agent:
    model_name: o1
    reasoning_effort: high
    supports_reasoning: true
    max_completion_tokens: 32768
```

### Configuration 2: All DeepSeek (Cost-Effective)
```yaml
default:
  provider: openai
  model_name: deepseek-chat
  api_base: https://api.deepseek.com/v1
  api_key: ${DEEPSEEK_API_KEY}
  temperature: 0.7
  max_tokens: 4096

agents:
  # Use DeepSeek Reasoner for analytical agents
  quantitative_analysis_agent:
    model_name: deepseek-reasoner
    supports_reasoning: true
    max_tokens: 8192
    
  variance_analysis_agent:
    model_name: deepseek-reasoner
    supports_reasoning: true
    max_tokens: 8192
    
  anomaly_detection_agent:
    model_name: deepseek-reasoner
    supports_reasoning: true
    max_tokens: 8192
```

### Configuration 3: Local Models via LM Studio
```yaml
default:
  provider: openai
  model_name: openai/deepseek-r1-distill-llama-70b
  api_base: http://localhost:1234/v1
  api_key: lm-studio
  supports_reasoning: true
  max_tokens: 8192
  temperature: 0.7
```

## Implementation Details

### What the Code Does

When `supports_reasoning: true` is set:

```python
# In models.py
if supports_reasoning:
    # Remove parameters not supported by reasoning models
    extra_kwargs.pop("temperature", None)
    extra_kwargs.pop("top_p", None)
    # Keep reasoning-specific parameters
    # - reasoning_effort
    # - max_completion_tokens
```

### Parameters Passed to LiteLLM

The following parameters are now supported:

```python
_LITELLM_EXTRA_KEYS = {
    # Standard parameters
    "temperature",
    "max_tokens",
    "timeout",
    "custom_llm_provider",
    
    # Reasoning model parameters  
    "reasoning_effort",          # o1: low/medium/high
    "max_completion_tokens",     # o1: output token limit
    "supports_reasoning",        # Flag for special handling
    
    # Additional parameters
    "top_p",
    "frequency_penalty",
    "presence_penalty",
    "stop",
    "stream",
}
```

## Testing

### Test with a Simple Query

```python
# Test o1 model
python main.py "Calculate the sum of prime numbers between 1 and 100"
```

The reasoning model will:
1. Think through the mathematical problem
2. Show reasoning process (if supported)
3. Provide detailed answer

### Test Complex Analysis

```python
python main.py "Analyze MLO variance between March 1 and March 15, identify patterns, and explain root causes"
```

The reasoning model will:
1. Break down the complex query
2. Plan the analysis steps
3. Execute calculations with reasoning
4. Provide comprehensive explanation

## Performance Comparison

| Task | GPT-4o | o1-mini | o1-preview | Notes |
|------|---------|---------|------------|-------|
| Schema Discovery | ⚡ Fast | 🐌 Slow | 🐌 Very Slow | Overkill for simple tasks |
| SQL Generation | ⚡ Fast | ⚡ Fast | 🐌 Slow | o1-mini good enough |
| Variance Calc | ✅ Good | ✅✅ Better | ✅✅✅ Best | Reasoning helps accuracy |
| Anomaly Detection | ✅ Good | ✅✅ Better | ✅✅✅ Best | Deep reasoning beneficial |
| Report Formatting | ⚡ Fast | 🐌 Slow | 🐌 Slow | Don't use reasoning models |

**Recommendation**: Use reasoning models selectively for complex analytical tasks, not for simple data retrieval or formatting.

## Cost Optimization

### Strategy 1: Tiered Approach
```
Simple tasks (schema, SQL)      → gpt-4o-mini  ($0.15/$0.60/1M)
Medium complexity (variance)    → o1-mini      ($3/$12/1M)
Complex reasoning (anomalies)   → o1-preview   ($15/$60/1M)
```

### Strategy 2: DeepSeek for All
```
All tasks → deepseek-reasoner  ($0.55/$2.19/1M)
```
Trade-off: Slightly lower capability, much lower cost

### Strategy 3: Hybrid
```
Simple → gpt-4o-mini
Complex → deepseek-reasoner
Critical → o1-preview (when accuracy is paramount)
```

## Environment Variables

Add to your `.env` file:

```env
# OpenAI (for o1 models)
OPENAI_API_KEY=sk-...

# DeepSeek (cost-effective alternative)
DEEPSEEK_API_KEY=sk-...

# Your LM Studio (local testing)
# No key needed - uses http://localhost:1234/v1
```

## Troubleshooting

### "Model doesn't support parameter 'temperature'"
✅ **Solution**: Set `supports_reasoning: true` in config

### "Rate limit exceeded"
⚠️ **Cause**: Reasoning models can be rate-limited
✅ **Solution**: 
- Add `timeout: 300` for longer waits
- Use `reasoning_effort: medium` instead of `high`
- Consider o1-mini instead of o1-preview

### "Response too slow"
✅ **Solutions**:
- Use `reasoning_effort: low` or `medium`
- Switch heavy-reasoning agents to o1-mini
- Use reasoning models only for complex tasks

### "Cost too high"
✅ **Solutions**:
- Switch to DeepSeek R1 ($0.55/$2.19 vs $15/$60)
- Use o1-mini instead of o1-preview
- Reserve reasoning models for specific agents only

## Best Practices

1. **Use reasoning models strategically**
   - ✅ Complex calculations (variance, LCR, NSFR)
   - ✅ Multi-step analysis
   - ✅ Anomaly root cause investigation
   - ❌ Simple queries, formatting, schema discovery

2. **Tune reasoning_effort**
   - Start with `medium`
   - Use `high` only for critical calculations
   - Use `low` for faster prototyping

3. **Monitor costs**
   - Track token usage per agent
   - Consider DeepSeek for development
   - Reserve o1-preview for production/critical work

4. **Test thoroughly**
   - Reasoning models behave differently
   - Validate accuracy on your use cases
   - Compare results with standard models

## References

- [OpenAI o1 Documentation](https://platform.openai.com/docs/guides/reasoning)
- [DeepSeek R1 Documentation](https://api-docs.deepseek.com/)
- [LiteLLM Reasoning Support](https://docs.litellm.ai/docs/providers/openai#o1-models)
- [ADK LiteLLM Integration](https://google.github.io/adk-docs/agents/models/litellm/)

## Next Steps

1. **Configure your reasoning model**: Edit `models.yaml`
2. **Set API keys**: Add to `.env`
3. **Test it**: `python main.py "Complex analytical query"`
4. **Monitor performance**: Compare reasoning vs standard models
5. **Optimize costs**: Adjust agent assignments based on results
