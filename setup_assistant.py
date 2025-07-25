#!/usr/bin/env python3
"""
Voice Assistant Setup and Installation Script
Comprehensive setup for the Lepida Voice Assistant
"""

import os
import sys
import subprocess
import shutil
import platform
import importlib
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("🤖 LEPIDA VOICE ASSISTANT SETUP")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"❌ Python {min_version[0]}.{min_version[1]}+ is required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python {current_version[0]}.{current_version[1]} is compatible")
    print(f"   Platform: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    return True

def check_system_requirements():
    """Check system requirements and available resources."""
    print("🖥️  Checking system requirements...")
    
    try:
        import psutil
        
        # Check available memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print(f"   RAM: {memory_gb:.1f} GB total, {memory.percent}% used")
        
        if memory_gb < 2:
            print("   ⚠️  Warning: Less than 2GB RAM available")
        
        # Check disk space
        disk = psutil.disk_usage('.')
        disk_free_gb = disk.free / (1024**3)
        print(f"   Disk: {disk_free_gb:.1f} GB free")
        
        if disk_free_gb < 1:
            print("   ⚠️  Warning: Less than 1GB disk space available")
        
        # Check CPU
        cpu_count = psutil.cpu_count()
        print(f"   CPU: {cpu_count} cores")
        
        return True
        
    except ImportError:
        print("   ⚠️  psutil not installed - skipping detailed system check")
        return True
    except Exception as e:
        print(f"   ⚠️  System check failed: {e}")
        return True

def check_audio_system():
    """Check audio system availability."""
    print("🎵 Checking audio system...")
    
    try:
        import pyaudio
        
        audio = pyaudio.PyAudio()
        
        # Check input devices
        input_devices = []
        output_devices = []
        
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
            if device_info['maxOutputChannels'] > 0:
                output_devices.append(device_info['name'])
        
        print(f"   Input devices: {len(input_devices)} found")
        print(f"   Output devices: {len(output_devices)} found")
        
        if len(input_devices) == 0:
            print("   ⚠️  No audio input devices found")
        if len(output_devices) == 0:
            print("   ⚠️  No audio output devices found")
        
        audio.terminate()
        return True
        
    except ImportError:
        print("   ⚠️  PyAudio not installed - audio system not available")
        return False
    except Exception as e:
        print(f"   ❌ Audio system check failed: {e}")
        return False

def check_optional_dependencies():
    """Check optional dependencies availability."""
    print("🔍 Checking optional dependencies...")
    
    optional_deps = {
        'torch': 'PyTorch (for AI models)',
        'transformers': 'Transformers (for language models)',
        'whisper': 'OpenAI Whisper (for speech recognition)',
        'psutil': 'System monitoring',
        'pygame': 'Alternative audio playback',
        'scipy': 'Scientific computing for audio',
        'librosa': 'Advanced audio analysis'
    }
    
    available = []
    missing = []
    
    for dep, description in optional_deps.items():
        try:
            importlib.import_module(dep)
            available.append(f"{dep} - {description}")
            print(f"   ✅ {dep}")
        except ImportError:
            missing.append(f"{dep} - {description}")
            print(f"   ❌ {dep} (optional)")
    
    print(f"\n   Available: {len(available)}/{len(optional_deps)} optional dependencies")
    
    if missing:
        print("   Missing optional dependencies:")
        for dep in missing:
            print(f"     - {dep}")
        print("   Note: These are optional and can be installed later if needed")
    
    return True

def download_models():
    """Download required models if not present."""
    print("📥 Checking and downloading models...")
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Check for TTS models
    tts_models = {
        "facebook/mms-tts-ind": "Indonesian TTS model"
    }
    
    # Check for STT models
    whisper_model_path = models_dir / "whisper"
    if not whisper_model_path.exists():
        print("   ⚠️  Whisper models not found")
        print("   Models will be downloaded automatically when first used")
    else:
        print("   ✅ Whisper models directory exists")
    
    # Check for wake word models
    porcupine_model_path = models_dir / "porcupine"
    if not porcupine_model_path.exists():
        print("   ⚠️  Porcupine wake word models not found")
        print("   Wake word detection may require additional setup")
    else:
        print("   ✅ Porcupine models directory exists")
    
    return True

def validate_configuration():
    """Validate configuration files."""
    print("⚙️  Validating configuration...")
    
    # Check config.yml
    config_file = Path("config.yml")
    if config_file.exists():
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            required_sections = ['app', 'audio', 'tts', 'stt']
            missing_sections = []
            
            for section in required_sections:
                if section not in config:
                    missing_sections.append(section)
                else:
                    print(f"   ✅ {section} section found")
            
            if missing_sections:
                print(f"   ⚠️  Missing sections: {missing_sections}")
                return False
            else:
                print("   ✅ Configuration file is valid")
                return True
                
        except Exception as e:
            print(f"   ❌ Configuration file error: {e}")
            return False
    else:
        print("   ⚠️  config.yml not found")
        print("   Default configuration will be created")
        return True

def create_directories():
    """Create necessary directories."""
    directories = [
        "logs",
        "outputs",
        "outputs/sound", 
        "models",
        "temp",
        "assets/audio"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"   Created: {directory}")
    
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def setup_frontend():
    """Setup frontend web interface."""
    print("🌐 Setting up frontend web interface...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Check if frontend requirements.txt exists
    frontend_requirements = frontend_dir / "requirements.txt"
    if not frontend_requirements.exists():
        print("❌ Frontend requirements.txt not found")
        return False
    
    try:
        # Install frontend dependencies
        print("   Installing frontend dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(frontend_requirements)
        ], check=True, capture_output=True, text=True)
        print("   ✅ Frontend dependencies installed")
        
        # Create frontend templates directory if not exists
        templates_dir = frontend_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Copy index.html to templates if needed
        main_index = frontend_dir / "index.html"
        template_index = templates_dir / "index.html"
        
        if main_index.exists() and not template_index.exists():
            shutil.copy2(main_index, template_index)
            print("   ✅ HTML template copied to templates directory")
        
        # Create static directories
        static_dirs = ["static", "static/css", "static/js", "temp"]
        for static_dir in static_dirs:
            (frontend_dir / static_dir).mkdir(parents=True, exist_ok=True)
        
        print("   ✅ Frontend directories created")
        
        # Test frontend app import
        frontend_app = frontend_dir / "app.py"
        if frontend_app.exists():
            print("   ✅ Frontend Flask app found")
        else:
            print("   ⚠️  Frontend Flask app not found")
        
        print("✅ Frontend setup completed successfully")
        print("   To start frontend: cd frontend && python app.py")
        print("   Web interface: http://localhost:5000")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        print(f"   Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Frontend setup failed: {e}")
        return False

def setup_environment():
    """Setup environment variables."""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from example")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example file found")
        
    return True

def generate_audio_assets():
    """Generate audio assets."""
    print("🎵 Generating audio assets...")
    
    try:
        from assets.audio.generate_audio_assets import create_audio_assets
        create_audio_assets()
        print("✅ Audio assets generated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to generate audio assets: {e}")
        print("   You can generate them manually by running:")
        print("   python assets/audio/generate_audio_assets.py")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    print("🧪 Testing basic functionality...")
    
    try:
        # Test configuration loading
        from config.config import get_config
        config = get_config()
        print("   ✅ Configuration loading works")
        
        # Test TTS initialization
        try:
            from utils.text_to_speech import TextToSpeech
            tts = TextToSpeech(config)
            print("   ✅ TTS system initialized")
        except Exception as e:
            print(f"   ⚠️  TTS initialization failed: {e}")
        
        # Test audio processing
        try:
            from helper.audio_processing import AudioProcessor
            audio_processor = AudioProcessor(config)
            print("   ✅ Audio processing initialized")
        except Exception as e:
            print(f"   ⚠️  Audio processing failed: {e}")
        
        # Test wake word detection
        try:
            from utils.wake_word_detection import WakeWordDetector
            wake_detector = WakeWordDetector(config)
            print("   ✅ Wake word detection initialized")
        except Exception as e:
            print(f"   ⚠️  Wake word detection failed: {e}")
        
        # Test command processor
        try:
            from utils.command_processor import VoiceCommandProcessor
            cmd_processor = VoiceCommandProcessor(config, None, None)
            print("   ✅ Command processor initialized")
        except Exception as e:
            print(f"   ⚠️  Command processor failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Basic functionality test failed: {e}")
        return False

def validate_plugins():
    """Validate available plugins."""
    print("🔌 Validating plugins...")
    
    try:
        from utils.plugin_validator import PluginValidator
        from config.config import get_config
        
        config = get_config()
        validator = PluginValidator(config)
        
        # Discover plugins
        plugins = validator.discover_plugins()
        total_plugins = sum(len(plugin_list) for plugin_list in plugins.values())
        
        print(f"   Found {total_plugins} plugins:")
        for plugin_type, plugin_list in plugins.items():
            if plugin_list:
                print(f"     {plugin_type}: {len(plugin_list)} plugins")
        
        # Validate plugins
        if total_plugins > 0:
            results = validator.validate_all_plugins()
            valid_count = 0
            invalid_count = 0
            
            for plugin_type, plugin_results in results.items():
                for plugin_name, result in plugin_results.items():
                    if result.get("valid", False):
                        valid_count += 1
                    else:
                        invalid_count += 1
            
            print(f"   Validation: {valid_count} valid, {invalid_count} invalid")
            
            if invalid_count > 0:
                print("   ⚠️  Some plugins failed validation")
                print("   Run 'python cli.py health' for detailed plugin report")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Plugin validation failed: {e}")
        return True

def run_health_check():
    """Run comprehensive health check."""
    print("🏥 Running health check...")
    
    try:
        from config.config import get_config
        from utils.health_check import HealthChecker
        
        config = get_config()
        checker = HealthChecker(config)
        report = checker.run_all_checks()
        
        summary = report["summary"]
        if summary["error_count"] == 0:
            print("✅ Health check passed")
            return True
        else:
            print(f"⚠️  Health check found {summary['error_count']} errors and {summary['warning_count']} warnings")
            print("   Run 'python cli.py health' for detailed report")
            return True
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def setup_complete():
    """Display setup completion message."""
    print()
    print("=" * 60)
    print("🎉 SETUP COMPLETED!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run health check: python cli.py health")
    print("2. Test TTS: python cli.py test-tts")
    print("3. Test STT: python cli.py test-stt")
    print("4. List audio devices: python cli.py devices")
    print("5. Start voice assistant: python cli.py run")
    print("6. Start web interface: cd frontend && python app.py")
    print()
    print("Alternative launch methods:")
    print("- Simple launcher: python launcher.py")
    print("- Direct app: python app.py")
    print("- Web interface: http://localhost:5000 (after starting frontend)")
    print()
    print("Configuration files:")
    print("- Edit config.yml for voice assistant settings")
    print("- Edit .env for API keys and environment variables")
    print()
    print("Troubleshooting:")
    print("- For detailed system report: python cli.py health")
    print("- For plugin validation: python -c \"from utils.plugin_validator import *\"")
    print("- Check logs in: logs/voice_assistant.log")
    print()

def recovery_mode():
    """Run setup in recovery mode for fixing issues."""
    print("🔧 RECOVERY MODE")
    print("=" * 60)
    print("This mode will attempt to fix common issues")
    print()
    
    recovery_steps = [
        ("Recreating directories", create_directories),
        ("Regenerating .env file", setup_environment),
        ("Regenerating audio assets", generate_audio_assets),
        ("Testing configuration", validate_configuration),
    ]
    
    for step_name, step_func in recovery_steps:
        print(f"🔄 {step_name}...")
        try:
            step_func()
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
    
    print("\n✅ Recovery mode completed")
    print("Try running the full setup again: python setup_assistant.py")

def main():
    """Main setup function."""
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--recovery":
            recovery_mode()
            return
        elif sys.argv[1] == "--quick":
            print("🚀 QUICK SETUP MODE")
            print("=" * 60)
            quick_steps = [
                ("Checking Python version", check_python_version),
                ("Creating directories", create_directories),
                ("Setting up environment", setup_environment),
                ("Generating audio assets", generate_audio_assets),
            ]
            for step_name, step_func in quick_steps:
                print(f"🔄 {step_name}...")
                step_func()
            print("✅ Quick setup completed")
            return
        elif sys.argv[1] == "--frontend":
            print("🌐 FRONTEND SETUP MODE")
            print("=" * 60)
            frontend_steps = [
                ("Checking Python version", check_python_version),
                ("Setting up frontend", setup_frontend),
            ]
            for step_name, step_func in frontend_steps:
                print(f"🔄 {step_name}...")
                if not step_func():
                    print(f"❌ {step_name} failed")
                    return
            print("✅ Frontend setup completed")
            print("🌐 Start frontend: cd frontend && python app.py")
            print("🌐 Web interface: http://localhost:5000")
            return
        elif sys.argv[1] == "--help":
            print("Voice Assistant Setup Options:")
            print("  python setup_assistant.py          # Full setup")
            print("  python setup_assistant.py --quick  # Quick setup (no dependencies)")
            print("  python setup_assistant.py --frontend # Setup frontend only")
            print("  python setup_assistant.py --recovery # Fix common issues")
            print("  python setup_assistant.py --help   # Show this help")
            return
    
    print_banner()
    
    # Setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Checking system requirements", check_system_requirements),
        ("Checking audio system", check_audio_system),
        ("Creating directories", create_directories),
        ("Installing dependencies", install_dependencies),
        ("Setting up frontend", setup_frontend),
        ("Checking optional dependencies", check_optional_dependencies),
        ("Setting up environment", setup_environment),
        ("Validating configuration", validate_configuration),
        ("Downloading/checking models", download_models),
        ("Generating audio assets", generate_audio_assets),
        ("Testing basic functionality", test_basic_functionality),
        ("Validating plugins", validate_plugins),
        ("Running health check", run_health_check)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
            failed_steps.append(step_name)
    
    print()
    if failed_steps:
        print(f"⚠️  Setup completed with {len(failed_steps)} issue(s):")
        for step in failed_steps:
            print(f"   - {step}")
        print()
        print("You may need to fix these issues manually.")
    else:
        print("✅ All setup steps completed successfully!")
    
    setup_complete()

if __name__ == "__main__":
    main()
