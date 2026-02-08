"""Centralized LiteLLM model factory for on-prem hosted models.

All agents call ``get_model(agent_name)`` which returns a ``LiteLlm``
instance configured from YAML.  Each agent gets the **default** model
config merged with any per-agent overrides defined under
``model.agents.<agent_name>``.

Usage in an agent file::

    from risk_analytics_agent.models import get_model

    my_agent = LlmAgent(
        name="my_agent",
        model=get_model("my_agent"),
        ...
    )

Configuration example (config/snowflake.yaml)::

    model:
      default:
        provider: openai
        model_name: claude-sonnet-4-5-20250929
        api_base: ${LLM_API_BASE}
        api_key: ${LLM_API_KEY}
      agents:
        orchestrator_agent:
          model_name: claude-opus-4-6
        schema_discovery_agent:
          provider: vllm
          model_name: mistral-7b
          api_base: https://vllm.internal.corp/v1
"""

from __future__ import annotations

import threading

from google.adk.models.lite_llm import LiteLlm

from risk_analytics_agent.config import load_model_config

_cache: dict[str, LiteLlm] = {}
_lock = threading.Lock()

_LITELLM_EXTRA_KEYS = frozenset({
    "temperature",
    "max_tokens",
    "timeout",
    "custom_llm_provider",
})


def _build_model(agent_name: str | None) -> LiteLlm:
    """Build a ``LiteLlm`` from the merged default + agent config."""
    full_cfg = load_model_config()
    default_cfg: dict = full_cfg.get("default", {})
    agent_overrides: dict = {}

    if agent_name:
        agents_section = full_cfg.get("agents") or {}
        agent_overrides = agents_section.get(agent_name) or {}

    # Merge: agent values override defaults
    merged = {**default_cfg, **agent_overrides}

    provider = merged["provider"]
    model_name = merged["model_name"]
    api_base = merged.get("api_base")
    api_key = merged.get("api_key")

    model_string = f"{provider}/{model_name}"

    extra_kwargs = {
        k: v for k, v in merged.items()
        if k in _LITELLM_EXTRA_KEYS and v is not None
    }

    return LiteLlm(
        model=model_string,
        api_base=api_base,
        api_key=api_key,
        **extra_kwargs,
    )


def get_model(agent_name: str | None = None) -> LiteLlm:
    """Return a ``LiteLlm`` instance for the given agent.

    Results are cached per *agent_name* so the same ``LiteLlm`` object
    is reused across repeated calls.

    Args:
        agent_name: The agent's ``name`` (e.g. ``"orchestrator_agent"``).
            If *None*, returns the default model with no agent overrides.
    """
    cache_key = agent_name or "__default__"

    if cache_key in _cache:
        return _cache[cache_key]

    with _lock:
        if cache_key in _cache:
            return _cache[cache_key]

        model = _build_model(agent_name)
        _cache[cache_key] = model
        return model


def reset_models() -> None:
    """Clear the model cache (useful for testing)."""
    with _lock:
        _cache.clear()
