"""Configuration loader"""
import yaml
from pathlib import Path

_config = None

def load_config(config_path=None):
    """Load generation configuration"""
    global _config
    
    if _config is not None:
        return _config
    
    if config_path is None:
        config_path = Path(__file__).parent / "generation_config.yaml"
    
    with open(config_path, 'r') as f:
        _config = yaml.safe_load(f)
    
    return _config

def get_config(key, default=None):
    """Get a configuration value by key (supports dot notation)"""
    config = load_config()
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
        if value is None:
            return default
    return value

