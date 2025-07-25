"""
Plugin Validation System
Validates and tests voice assistant plugins
"""

import logging
import importlib
import inspect
from pathlib import Path

logger = logging.getLogger(__name__)

class PluginValidator:
    """Validates plugin implementations and interfaces."""
    
    def __init__(self, config):
        """Initialize plugin validator."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.plugins_dir = Path("plugins")
        
    def validate_tts_plugin(self, plugin_name):
        """Validate a TTS plugin."""
        try:
            plugin_module = importlib.import_module(f"plugins.tts_{plugin_name}")
            
            # Check required function
            if not hasattr(plugin_module, 'run'):
                return {"valid": False, "error": "Missing 'run' function"}
                
            run_func = getattr(plugin_module, 'run')
            
            # Check function signature
            sig = inspect.signature(run_func)
            params = list(sig.parameters.keys())
            
            if 'text' not in params:
                return {"valid": False, "error": "Missing 'text' parameter in run function"}
                
            # Test basic functionality
            try:
                # Try a dry run (if supported)
                if hasattr(plugin_module, 'set_test_mode'):
                    plugin_module.set_test_mode(True)
                    
                result = run_func("test", lang="id")
                
                return {
                    "valid": True,
                    "message": "Plugin validated successfully",
                    "parameters": params,
                    "test_result": str(result) if result else "No return value"
                }
                
            except Exception as e:
                return {
                    "valid": False, 
                    "error": f"Plugin test failed: {e}",
                    "parameters": params
                }
                
        except ImportError as e:
            return {"valid": False, "error": f"Cannot import plugin: {e}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {e}"}
            
    def validate_stt_plugin(self, plugin_name):
        """Validate an STT plugin."""
        try:
            plugin_module = importlib.import_module(f"plugins.stt_{plugin_name}")
            
            # Check required functions
            required_functions = ['transcribe', 'transcribe_file']
            missing_functions = []
            
            for func_name in required_functions:
                if not hasattr(plugin_module, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                return {
                    "valid": False, 
                    "error": f"Missing functions: {missing_functions}"
                }
                
            # Check function signatures
            transcribe_func = getattr(plugin_module, 'transcribe')
            sig = inspect.signature(transcribe_func)
            params = list(sig.parameters.keys())
            
            if 'audio_data' not in params and 'audio_file' not in params:
                return {
                    "valid": False,
                    "error": "Missing audio parameter in transcribe function"
                }
                
            return {
                "valid": True,
                "message": "Plugin validated successfully", 
                "parameters": params,
                "functions": required_functions
            }
            
        except ImportError as e:
            return {"valid": False, "error": f"Cannot import plugin: {e}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {e}"}
            
    def validate_wakeword_plugin(self, plugin_name):
        """Validate a wake word detection plugin."""
        try:
            plugin_module = importlib.import_module(f"plugins.wakeword_{plugin_name}")
            
            # Check required functions
            required_functions = ['initialize', 'start_listening', 'stop_listening']
            missing_functions = []
            
            for func_name in required_functions:
                if not hasattr(plugin_module, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                return {
                    "valid": False,
                    "error": f"Missing functions: {missing_functions}"
                }
                
            # Check initialization function
            init_func = getattr(plugin_module, 'initialize')
            sig = inspect.signature(init_func)
            params = list(sig.parameters.keys())
            
            return {
                "valid": True,
                "message": "Plugin validated successfully",
                "parameters": params,
                "functions": required_functions
            }
            
        except ImportError as e:
            return {"valid": False, "error": f"Cannot import plugin: {e}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {e}"}
            
    def validate_soundfx_plugin(self, plugin_name):
        """Validate a sound effects plugin."""
        try:
            plugin_module = importlib.import_module(f"plugins.soundfx_{plugin_name}")
            
            # Check for common sound effect functions
            common_functions = [
                'play_beep', 'play_start', 'play_stop', 
                'play_success', 'play_error', 'play_notification'
            ]
            
            available_functions = []
            for func_name in common_functions:
                if hasattr(plugin_module, func_name):
                    available_functions.append(func_name)
                    
            if not available_functions:
                return {
                    "valid": False,
                    "error": "No sound effect functions found"
                }
                
            return {
                "valid": True,
                "message": "Plugin validated successfully",
                "available_functions": available_functions
            }
            
        except ImportError as e:
            return {"valid": False, "error": f"Cannot import plugin: {e}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {e}"}
            
    def discover_plugins(self):
        """Discover all available plugins."""
        plugins = {
            "tts": [],
            "stt": [],
            "wakeword": [],
            "soundfx": []
        }
        
        if not self.plugins_dir.exists():
            return plugins
            
        for plugin_file in self.plugins_dir.glob("*.py"):
            filename = plugin_file.stem
            
            if filename.startswith("tts_"):
                plugin_name = filename[4:]  # Remove "tts_" prefix
                plugins["tts"].append(plugin_name)
            elif filename.startswith("stt_"):
                plugin_name = filename[4:]  # Remove "stt_" prefix
                plugins["stt"].append(plugin_name)
            elif filename.startswith("wakeword_"):
                plugin_name = filename[9:]  # Remove "wakeword_" prefix
                plugins["wakeword"].append(plugin_name)
            elif filename.startswith("soundfx_"):
                plugin_name = filename[8:]  # Remove "soundfx_" prefix
                plugins["soundfx"].append(plugin_name)
                
        return plugins
        
    def validate_all_plugins(self):
        """Validate all discovered plugins."""
        plugins = self.discover_plugins()
        results = {}
        
        # Validate TTS plugins
        results["tts"] = {}
        for plugin_name in plugins["tts"]:
            results["tts"][plugin_name] = self.validate_tts_plugin(plugin_name)
            
        # Validate STT plugins
        results["stt"] = {}
        for plugin_name in plugins["stt"]:
            results["stt"][plugin_name] = self.validate_stt_plugin(plugin_name)
            
        # Validate wake word plugins
        results["wakeword"] = {}
        for plugin_name in plugins["wakeword"]:
            results["wakeword"][plugin_name] = self.validate_wakeword_plugin(plugin_name)
            
        # Validate sound FX plugins
        results["soundfx"] = {}
        for plugin_name in plugins["soundfx"]:
            results["soundfx"][plugin_name] = self.validate_soundfx_plugin(plugin_name)
            
        return results
        
    def format_validation_report(self, results):
        """Format plugin validation results for display."""
        lines = []
        lines.append("=" * 60)
        lines.append("PLUGIN VALIDATION REPORT")
        lines.append("=" * 60)
        
        for plugin_type, plugins in results.items():
            if not plugins:
                continue
                
            lines.append(f"\n📦 {plugin_type.upper()} PLUGINS")
            lines.append("-" * 40)
            
            for plugin_name, result in plugins.items():
                if result["valid"]:
                    lines.append(f"  ✅ {plugin_name}: {result['message']}")
                    if "parameters" in result:
                        lines.append(f"     Parameters: {', '.join(result['parameters'])}")
                    if "functions" in result:
                        lines.append(f"     Functions: {', '.join(result['functions'])}")
                    if "available_functions" in result:
                        lines.append(f"     Available: {', '.join(result['available_functions'])}")
                else:
                    lines.append(f"  ❌ {plugin_name}: {result['error']}")
                    
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
        
    def check_plugin_dependencies(self, plugin_name, plugin_type):
        """Check if plugin dependencies are available."""
        try:
            plugin_module = importlib.import_module(f"plugins.{plugin_type}_{plugin_name}")
            
            # Check if plugin has a dependencies function or list
            dependencies = []
            if hasattr(plugin_module, 'get_dependencies'):
                dependencies = plugin_module.get_dependencies()
            elif hasattr(plugin_module, 'DEPENDENCIES'):
                dependencies = plugin_module.DEPENDENCIES
                
            missing_deps = []
            for dep in dependencies:
                try:
                    importlib.import_module(dep)
                except ImportError:
                    missing_deps.append(dep)
                    
            return {
                "dependencies": dependencies,
                "missing": missing_deps,
                "satisfied": len(missing_deps) == 0
            }
            
        except Exception as e:
            return {
                "error": f"Cannot check dependencies: {e}",
                "satisfied": False
            }
