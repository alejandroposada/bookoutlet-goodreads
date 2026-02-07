"""Configuration loader with YAML support and CLI overrides."""

import os
from pathlib import Path
from typing import Optional, Dict, Any

import yaml

from .schema import Config


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries, with override taking precedence.

    Args:
        base: Base dictionary
        override: Override dictionary

    Returns:
        Merged dictionary
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to YAML file

    Returns:
        Configuration dictionary
    """
    if not config_path.exists():
        return {}

    with open(config_path, 'r') as f:
        return yaml.safe_load(f) or {}


def load_config(
    config_path: Optional[str] = None,
    cli_overrides: Optional[Dict[str, Any]] = None
) -> Config:
    """
    Load configuration with priority: CLI args > config.local.yaml > config.yaml > defaults.

    Args:
        config_path: Optional explicit config file path
        cli_overrides: Optional dictionary of CLI argument overrides

    Returns:
        Validated Config object

    Example:
        >>> config = load_config(cli_overrides={'matching': {'threshold': 95}})
        >>> config.matching.threshold
        95
    """
    # Start with empty config
    config_data = {}

    # Priority 1: Default config.yaml (if exists)
    default_config_path = Path('config.yaml')
    if default_config_path.exists():
        config_data = load_yaml_config(default_config_path)

    # Priority 2: Local config override (config.local.yaml)
    local_config_path = Path('config.local.yaml')
    if local_config_path.exists():
        local_config = load_yaml_config(local_config_path)
        config_data = deep_merge(config_data, local_config)

    # Priority 3: Explicit config file path
    if config_path:
        explicit_config = load_yaml_config(Path(config_path))
        config_data = deep_merge(config_data, explicit_config)

    # Priority 4: CLI overrides
    if cli_overrides:
        config_data = deep_merge(config_data, cli_overrides)

    # Validate and return
    return Config(**config_data)


def save_config(config: Config, path: str = "config.yaml"):
    """
    Save configuration to YAML file.

    Args:
        config: Config object to save
        path: Path to save to
    """
    config_dict = config.model_dump()

    with open(path, 'w') as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
