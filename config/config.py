import os
import yaml
from pathlib import Path

class Config:
    """Configuration loader for the voice assistant application."""
    
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yml"
        
        self.config_path = Path(config_path)
        self._config = None
        self.load_config()
    
    def load_config(self):
        """Load configuration from config.yml file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
        except FileNotFoundError:
            # Create default config if it doesn't exist
            from .default import create_default_config
            create_default_config(self.config_path)
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing config.yml: {e}")
    
    def get(self, key_path, default=None):
        """
        Get configuration value using dot notation.
        Example: config.get('audio.input.sample_rate')
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def update(self, key_path, value):
        """Update configuration value and save to file."""
        keys = key_path.split('.')
        config = self._config
        
        if config is None:
            config = {}
            self._config = config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save to file
        self.save_config()
    
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(self._config, file, default_flow_style=False, allow_unicode=True)
    
    @property
    def config(self):
        """Get the full configuration dictionary."""
        return self._config

# Global configuration instance
_config_instance = None

def get_config():
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

def load_env_variables():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
