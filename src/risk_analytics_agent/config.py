"""YAML configuration loader with environment variable interpolation."""

import os
import re
from pathlib import Path

import yaml

_ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")

CONFIG_DIR = Path(__file__).resolve().parent / "config"


def _interpolate_env(value: str, allow_missing: bool = False) -> str:
    """Replace ${ENV_VAR} placeholders with environment variable values.
    
    Args:
        value: String potentially containing ${VAR} placeholders
        allow_missing: If True, missing variables return empty string instead of raising
    """

    def _replace(match: re.Match) -> str:
        var_name = match.group(1)
        env_val = os.environ.get(var_name)
        if env_val is None:
            if allow_missing:
                return ""
            raise ValueError(
                f"Environment variable '{var_name}' is not set "
                f"(referenced in config)"
            )
        return env_val

    return _ENV_VAR_PATTERN.sub(_replace, value)


def _walk_and_interpolate(obj: object, allow_missing: bool = False) -> object:
    """Recursively interpolate environment variables in a config structure.
    
    Args:
        obj: Config object (dict, list, str, etc.)
        allow_missing: If True, missing env vars return empty string
    """
    if isinstance(obj, str):
        return _interpolate_env(obj, allow_missing=allow_missing)
    if isinstance(obj, dict):
        return {k: _walk_and_interpolate(v, allow_missing=allow_missing) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_and_interpolate(item, allow_missing=allow_missing) for item in obj]
    return obj


def _load_yaml(default_name: str, local_name: str, path: Path | None = None, allow_missing_env: bool = False) -> dict:
    """Load a YAML config file with local-override support.
    
    Args:
        default_name: Default config filename
        local_name: Local override filename
        path: Optional explicit path
        allow_missing_env: If True, missing env vars become empty strings
    """
    if path is None:
        local_path = CONFIG_DIR / local_name
        default_path = CONFIG_DIR / default_name
        path = local_path if local_path.exists() else default_path

    with open(path) as f:
        raw = yaml.safe_load(f)

    return _walk_and_interpolate(raw, allow_missing=allow_missing_env)


def load_snowflake_config(path: Path | None = None) -> dict:
    """Load Snowflake configuration from ``config/snowflake.yaml``.

    Checks for ``snowflake.local.yaml`` first, then falls back to the
    default template.
    
    Allows missing environment variables (returns empty strings)
    to support demo/mock mode.
    """
    return _load_yaml("snowflake.yaml", "snowflake.local.yaml", path, allow_missing_env=True)["snowflake"]


def load_model_config(path: Path | None = None) -> dict:
    """Load LLM model configuration from ``config/models.yaml``.

    Checks for ``models.local.yaml`` first, then falls back to the
    default template.  Returns the top-level dict containing ``default``
    and ``agents`` keys.
    """
    return _load_yaml("models.yaml", "models.local.yaml", path)
