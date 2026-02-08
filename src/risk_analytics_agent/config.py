"""YAML configuration loader with environment variable interpolation."""

import os
import re
from pathlib import Path

import yaml

_ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")

CONFIG_DIR = Path(__file__).resolve().parent / "config"


def _interpolate_env(value: str) -> str:
    """Replace ${ENV_VAR} placeholders with environment variable values."""

    def _replace(match: re.Match) -> str:
        var_name = match.group(1)
        env_val = os.environ.get(var_name)
        if env_val is None:
            raise ValueError(
                f"Environment variable '{var_name}' is not set "
                f"(referenced in config)"
            )
        return env_val

    return _ENV_VAR_PATTERN.sub(_replace, value)


def _walk_and_interpolate(obj: object) -> object:
    """Recursively interpolate environment variables in a config structure."""
    if isinstance(obj, str):
        return _interpolate_env(obj)
    if isinstance(obj, dict):
        return {k: _walk_and_interpolate(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_and_interpolate(item) for item in obj]
    return obj


def _load_yaml(default_name: str, local_name: str, path: Path | None = None) -> dict:
    """Load a YAML config file with local-override support."""
    if path is None:
        local_path = CONFIG_DIR / local_name
        default_path = CONFIG_DIR / default_name
        path = local_path if local_path.exists() else default_path

    with open(path) as f:
        raw = yaml.safe_load(f)

    return _walk_and_interpolate(raw)


def load_snowflake_config(path: Path | None = None) -> dict:
    """Load Snowflake configuration from ``config/snowflake.yaml``.

    Checks for ``snowflake.local.yaml`` first, then falls back to the
    default template.
    """
    return _load_yaml("snowflake.yaml", "snowflake.local.yaml", path)["snowflake"]


def load_model_config(path: Path | None = None) -> dict:
    """Load LLM model configuration from ``config/models.yaml``.

    Checks for ``models.local.yaml`` first, then falls back to the
    default template.  Returns the top-level dict containing ``default``
    and ``agents`` keys.
    """
    return _load_yaml("models.yaml", "models.local.yaml", path)
