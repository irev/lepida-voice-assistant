"""
Model and Plugin Auto-loader
Handles dynamic loading of TTS, STT, and other plugins
"""

import importlib
import logging
from pathlib import Path

class AutoLoader:
    """Dynamic plugin loader for the voice assistant."""
    
    def __init__(self):
        """Initialize the auto-loader."""
        self.logger = logging.getLogger(__name__)
        self.loaded_plugins = {}
        self.plugin_info = {}
    
    def load_plugin(self, plugin_type, plugin_name):
        """
        Load a plugin dynamically.
        
        Args:
            plugin_type (str): Type of plugin (tts, stt, wakeword, soundfx)
            plugin_name (str): Name of the plugin
            
        Returns:
            module: Loaded plugin module or None if failed
        """
        plugin_key = f"{plugin_type}_{plugin_name}"
        
        # Return cached plugin if already loaded
        if plugin_key in self.loaded_plugins:
            return self.loaded_plugins[plugin_key]
        
        try:
            # Try to import the plugin
            module_name = f"plugins.{plugin_key}"
            plugin_module = importlib.import_module(module_name)
            
            # Cache the plugin
            self.loaded_plugins[plugin_key] = plugin_module
            
            # Get plugin info if available
            if hasattr(plugin_module, 'get_info'):
                self.plugin_info[plugin_key] = plugin_module.get_info()
            
            self.logger.info(f"Loaded plugin: {plugin_key}")
            return plugin_module
            
        except ImportError as e:
            self.logger.warning(f"Failed to load plugin {plugin_key}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading plugin {plugin_key}: {e}")
            return None
    
    def get_available_plugins(self, plugin_type=None):
        """
        Get list of available plugins.
        
        Args:
            plugin_type (str): Filter by plugin type (optional)
            
        Returns:
            list: List of available plugin names
        """
        plugins_dir = Path(__file__).parent.parent / "plugins"
        available_plugins = []
        
        if not plugins_dir.exists():
            return available_plugins
        
        # Scan for plugin files
        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
            
            plugin_name = plugin_file.stem
            
            # Filter by type if specified
            if plugin_type:
                if not plugin_name.startswith(f"{plugin_type}_"):
                    continue
                # Remove type prefix
                display_name = plugin_name[len(plugin_type) + 1:]
            else:
                display_name = plugin_name
            
            available_plugins.append(display_name)
        
        return available_plugins
    
    def get_plugin_info(self, plugin_type, plugin_name):
        """
        Get information about a plugin.
        
        Args:
            plugin_type (str): Type of plugin
            plugin_name (str): Name of the plugin
            
        Returns:
            dict: Plugin information or None if not available
        """
        plugin_key = f"{plugin_type}_{plugin_name}"
        
        # Load plugin if not already loaded
        if plugin_key not in self.loaded_plugins:
            self.load_plugin(plugin_type, plugin_name)
        
        return self.plugin_info.get(plugin_key)
    
    def check_plugin_requirements(self, plugin_type, plugin_name):
        """
        Check if plugin requirements are met.
        
        Args:
            plugin_type (str): Type of plugin
            plugin_name (str): Name of the plugin
            
        Returns:
            bool: True if requirements are met
        """
        plugin_info = self.get_plugin_info(plugin_type, plugin_name)
        
        if not plugin_info:
            return False
        
        # Check if requirements are specified
        requirements = plugin_info.get('requires', [])
        
        for requirement in requirements:
            try:
                importlib.import_module(requirement)
            except ImportError:
                self.logger.warning(f"Missing requirement for {plugin_type}_{plugin_name}: {requirement}")
                return False
        
        # Check availability function if it exists
        plugin_module = self.loaded_plugins.get(f"{plugin_type}_{plugin_name}")
        if plugin_module and hasattr(plugin_module, 'check_availability'):
            return plugin_module.check_availability()
        
        return True
    
    def reload_plugin(self, plugin_type, plugin_name):
        """
        Reload a plugin (useful for development).
        
        Args:
            plugin_type (str): Type of plugin
            plugin_name (str): Name of the plugin
            
        Returns:
            module: Reloaded plugin module or None if failed
        """
        plugin_key = f"{plugin_type}_{plugin_name}"
        
        try:
            # Remove from cache
            if plugin_key in self.loaded_plugins:
                del self.loaded_plugins[plugin_key]
            if plugin_key in self.plugin_info:
                del self.plugin_info[plugin_key]
            
            # Reload the module
            module_name = f"plugins.{plugin_key}"
            import sys
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            
            # Load again
            return self.load_plugin(plugin_type, plugin_name)
            
        except Exception as e:
            self.logger.error(f"Failed to reload plugin {plugin_key}: {e}")
            return None
