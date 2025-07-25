"""
Health Check System
Comprehensive health checks for voice assistant components
"""

import logging
import time
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class HealthChecker:
    """System health checker for voice assistant components."""
    
    def __init__(self, config):
        """Initialize health checker."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.checks = {}
        
    def check_dependencies(self):
        """Check if all required dependencies are available."""
        checks = {}
        
        # Core dependencies
        required_modules = [
            'numpy', 'soundfile', 'yaml', 'pathlib'
        ]
        
        # Optional dependencies
        optional_modules = {
            'pyaudio': 'Audio input/output',
            'whisper': 'Speech recognition', 
            'torch': 'AI models',
            'psutil': 'System monitoring',
            'requests': 'Online services'
        }
        
        # Check required modules
        for module in required_modules:
            try:
                __import__(module)
                checks[f"dependency_{module}"] = {"status": "ok", "message": f"{module} available"}
            except ImportError:
                checks[f"dependency_{module}"] = {"status": "error", "message": f"{module} not found"}
        
        # Check optional modules  
        for module, description in optional_modules.items():
            try:
                __import__(module)
                checks[f"optional_{module}"] = {"status": "ok", "message": f"{module} available - {description}"}
            except ImportError:
                checks[f"optional_{module}"] = {"status": "warning", "message": f"{module} not found - {description} disabled"}
                
        return checks
        
    def check_configuration(self):
        """Check configuration files and settings."""
        checks = {}
        
        # Check config.yml
        config_file = Path("config.yml")
        if config_file.exists():
            checks["config_file"] = {"status": "ok", "message": "Configuration file found"}
            
            # Check key configuration sections
            required_sections = ['app', 'audio', 'tts', 'stt']
            for section in required_sections:
                if self.config.get(section):
                    checks[f"config_{section}"] = {"status": "ok", "message": f"{section} section configured"}
                else:
                    checks[f"config_{section}"] = {"status": "warning", "message": f"{section} section missing"}
        else:
            checks["config_file"] = {"status": "error", "message": "Configuration file not found"}
            
        # Check .env file
        env_file = Path(".env")
        if env_file.exists():
            checks["env_file"] = {"status": "ok", "message": "Environment file found"}
        else:
            checks["env_file"] = {"status": "warning", "message": "Environment file not found - using defaults"}
            
        return checks
        
    def check_audio_system(self):
        """Check audio system availability."""
        checks = {}
        
        try:
            # Check if audio processing is available
            from helper.audio_processing import AudioProcessor
            audio_processor = AudioProcessor(self.config)
            
            if hasattr(audio_processor, 'audio') and audio_processor.audio:
                checks["audio_system"] = {"status": "ok", "message": "Audio system initialized"}
                
                # Check for input/output devices
                try:
                    from utils.performance_monitor import AudioDeviceMonitor
                    device_monitor = AudioDeviceMonitor(self.config)
                    devices = device_monitor.get_audio_devices()
                    
                    input_devices = sum(1 for d in devices if d['max_input_channels'] > 0)
                    output_devices = sum(1 for d in devices if d['max_output_channels'] > 0)
                    
                    checks["audio_input"] = {
                        "status": "ok" if input_devices > 0 else "warning",
                        "message": f"{input_devices} input device(s) found"
                    }
                    checks["audio_output"] = {
                        "status": "ok" if output_devices > 0 else "warning", 
                        "message": f"{output_devices} output device(s) found"
                    }
                    
                    device_monitor.cleanup()
                    
                except Exception as e:
                    checks["audio_devices"] = {"status": "warning", "message": f"Could not enumerate devices: {e}"}
                    
            else:
                checks["audio_system"] = {"status": "error", "message": "Audio system not available"}
                
        except Exception as e:
            checks["audio_system"] = {"status": "error", "message": f"Audio system error: {e}"}
            
        return checks
        
    def check_models(self):
        """Check availability of AI models."""
        checks = {}
        
        # Check TTS models
        try:
            from utils.text_to_speech import TextToSpeech
            tts = TextToSpeech(self.config)
            checks["tts_system"] = {"status": "ok", "message": "TTS system available"}
        except Exception as e:
            checks["tts_system"] = {"status": "error", "message": f"TTS system error: {e}"}
            
        # Check STT models
        try:
            from utils.audio_transcription import AudioTranscription
            stt = AudioTranscription(self.config)
            checks["stt_system"] = {"status": "ok", "message": "STT system available"}
        except Exception as e:
            checks["stt_system"] = {"status": "error", "message": f"STT system error: {e}"}
            
        # Check wake word detection
        try:
            from utils.wake_word_detection import WakeWordDetector
            wake_detector = WakeWordDetector(self.config)
            if wake_detector.enabled:
                checks["wakeword_system"] = {"status": "ok", "message": "Wake word detection available"}
            else:
                checks["wakeword_system"] = {"status": "warning", "message": "Wake word detection disabled"}
        except Exception as e:
            checks["wakeword_system"] = {"status": "error", "message": f"Wake word system error: {e}"}
            
        return checks
        
    def check_assets(self):
        """Check availability of audio assets."""
        checks = {}
        
        assets_dir = Path("assets/audio")
        if not assets_dir.exists():
            checks["assets_dir"] = {"status": "warning", "message": "Audio assets directory not found"}
            return checks
            
        checks["assets_dir"] = {"status": "ok", "message": "Audio assets directory found"}
        
        # Check for expected audio files
        expected_files = [
            'audio.wav', 'start.wav', 'stop.wav', 'error.wav',
            'success.wav', 'notification.wav', 'welcome.wav', 'goodbye.wav'
        ]
        
        missing_files = []
        for filename in expected_files:
            file_path = assets_dir / filename
            if file_path.exists():
                checks[f"asset_{filename}"] = {"status": "ok", "message": f"{filename} found"}
            else:
                missing_files.append(filename)
                checks[f"asset_{filename}"] = {"status": "warning", "message": f"{filename} missing"}
                
        if missing_files:
            checks["assets_summary"] = {
                "status": "warning", 
                "message": f"{len(missing_files)} audio assets missing - run generate_audio_assets.py"
            }
        else:
            checks["assets_summary"] = {"status": "ok", "message": "All audio assets available"}
            
        return checks
        
    def check_permissions(self):
        """Check file and directory permissions."""
        checks = {}
        
        # Check write permissions for logs
        logs_dir = Path("logs")
        try:
            logs_dir.mkdir(exist_ok=True)
            test_file = logs_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            checks["logs_permission"] = {"status": "ok", "message": "Logs directory writable"}
        except Exception as e:
            checks["logs_permission"] = {"status": "error", "message": f"Cannot write to logs directory: {e}"}
            
        # Check write permissions for outputs
        outputs_dir = Path("outputs")
        try:
            outputs_dir.mkdir(exist_ok=True) 
            test_file = outputs_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            checks["outputs_permission"] = {"status": "ok", "message": "Outputs directory writable"}
        except Exception as e:
            checks["outputs_permission"] = {"status": "error", "message": f"Cannot write to outputs directory: {e}"}
            
        return checks
        
    def run_all_checks(self):
        """Run all health checks and return comprehensive report."""
        start_time = time.time()
        
        self.logger.info("Running health checks...")
        
        all_checks = {}
        
        # Run all check categories
        check_categories = [
            ("dependencies", self.check_dependencies),
            ("configuration", self.check_configuration), 
            ("audio_system", self.check_audio_system),
            ("models", self.check_models),
            ("assets", self.check_assets),
            ("permissions", self.check_permissions)
        ]
        
        for category, check_func in check_categories:
            try:
                checks = check_func()
                all_checks[category] = checks
            except Exception as e:
                self.logger.error(f"Error running {category} checks: {e}")
                all_checks[category] = {
                    "error": {"status": "error", "message": f"Check failed: {e}"}
                }
                
        # Generate summary
        total_checks = sum(len(checks) for checks in all_checks.values())
        ok_count = sum(
            1 for checks in all_checks.values() 
            for check in checks.values() 
            if check.get("status") == "ok"
        )
        warning_count = sum(
            1 for checks in all_checks.values()
            for check in checks.values()
            if check.get("status") == "warning"
        )
        error_count = sum(
            1 for checks in all_checks.values()
            for check in checks.values()
            if check.get("status") == "error"
        )
        
        duration = time.time() - start_time
        
        summary = {
            "total_checks": total_checks,
            "ok_count": ok_count, 
            "warning_count": warning_count,
            "error_count": error_count,
            "duration": duration,
            "overall_status": "ok" if error_count == 0 else "warning" if warning_count > 0 else "error"
        }
        
        self.logger.info(f"Health check completed in {duration:.2f}s - {ok_count} OK, {warning_count} warnings, {error_count} errors")
        
        return {
            "summary": summary,
            "checks": all_checks,
            "timestamp": time.time()
        }
        
    def format_report(self, report):
        """Format health check report for display."""
        lines = []
        lines.append("=" * 60)
        lines.append("VOICE ASSISTANT HEALTH CHECK REPORT")
        lines.append("=" * 60)
        
        summary = report["summary"]
        lines.append(f"Overall Status: {summary['overall_status'].upper()}")
        lines.append(f"Total Checks: {summary['total_checks']}")
        lines.append(f"✅ OK: {summary['ok_count']}")
        lines.append(f"⚠️  Warnings: {summary['warning_count']}")
        lines.append(f"❌ Errors: {summary['error_count']}")
        lines.append(f"Duration: {summary['duration']:.2f}s")
        lines.append("")
        
        # Details by category
        for category, checks in report["checks"].items():
            lines.append(f"📋 {category.upper().replace('_', ' ')}")
            lines.append("-" * 40)
            
            for check_name, check_result in checks.items():
                status = check_result.get("status", "unknown")
                message = check_result.get("message", "No message")
                
                if status == "ok":
                    icon = "✅"
                elif status == "warning":
                    icon = "⚠️"
                elif status == "error":
                    icon = "❌"
                else:
                    icon = "❓"
                    
                lines.append(f"  {icon} {check_name}: {message}")
            lines.append("")
            
        lines.append("=" * 60)
        return "\n".join(lines)
