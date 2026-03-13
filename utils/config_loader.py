"""
Configuration Loader for Intelli-Credit
Loads and validates YAML configuration
"""

import yaml
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to config.yaml file

    Returns:
        Dictionary containing configuration
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        raise


def get_config_value(config: Dict[str, Any], key_path: str, default=None):
    """
    Get nested configuration value using dot notation

    Args:
        config: Configuration dictionary
        key_path: Dot-separated key path (e.g., "scoring.base_score")
        default: Default value if key not found

    Returns:
        Configuration value or default
    """
    keys = key_path.split('.')
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value
