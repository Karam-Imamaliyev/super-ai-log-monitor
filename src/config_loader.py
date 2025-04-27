# src/config_loader.py

import yaml
import os


def load_config(config_path=os.path.join(os.path.dirname(__file__), "../config/settings.yaml")):
    """
    Loads configuration settings from a YAML file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration settings loaded from YAML.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config
