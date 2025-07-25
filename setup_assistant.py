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
from datetime import datetime
import tempfile
import requests
import zipfile
import logging
import time
import traceback

class SetupError(Exception):
    """Custom exception for setup-related errors."""
    def __init__(self, message, solution=None, error_code=None):
        self.message = message
        self.solution = solution
        self.error_code = error_code
        super().__init__(self.message)

def setup_logging():
    """Setup comprehensive logging for the setup process."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Setup log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"setup_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Create a custom logger for setup
    logger = logging.getLogger('setup')
    logger.info("=" * 80)
    logger.info("LEPIDA VOICE ASSISTANT - SETUP LOG STARTED")
    logger.info("=" * 80)
    logger.info(f"Setup started at: {datetime.now()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Architecture: {platform.machine()}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)
    
    return logger

def log_step_start(step_name):
    """Log the start of a setup step."""
    logger = logging.getLogger('setup')
    logger.info(f"🔄 STARTING: {step_name}")

def log_step_success(step_name):
    """Log successful completion of a setup step."""
    logger = logging.getLogger('setup')
    logger.info(f"✅ SUCCESS: {step_name}")

def log_step_warning(step_name, warning_msg):
    """Log a warning for a setup step."""
    logger = logging.getLogger('setup')
    logger.warning(f"⚠️  WARNING: {step_name} - {warning_msg}")

def log_step_error(step_name, error_msg, traceback_info=None):
    """Log an error for a setup step."""
    logger = logging.getLogger('setup')
    logger.error(f"❌ ERROR: {step_name} - {error_msg}")
    if traceback_info:
        logger.error(f"Traceback:\n{traceback_info}")

def log_system_info(info_dict):
    """Log system information."""
    logger = logging.getLogger('setup')
    logger.info("📊 System Information:")
    for key, value in info_dict.items():
        logger.info(f"   {key}: {value}")

def print_error_with_solution(error_msg, solution=None, error_code=None):
    """Print error message with solution suggestions."""
    logger = logging.getLogger('setup')
    print(f"❌ ERROR: {error_msg}")
    logger.error(f"ERROR: {error_msg}")
    
    if error_code:
        print(f"   Error Code: {error_code}")
        logger.error(f"   Error Code: {error_code}")
    if solution:
        print(f"💡 SOLUTION: {solution}")
        logger.info(f"   SOLUTION: {solution}")
    print()
    logger.error("-" * 40)

def handle_subprocess_error(e, operation="Operation"):
    """Handle subprocess errors with detailed information."""
    error_msg = f"{operation} failed with exit code {e.returncode}"
    
    if hasattr(e, 'stderr') and e.stderr:
        stderr_output = e.stderr.strip()
        print(f"❌ {error_msg}")
        print(f"   Error output: {stderr_output}")
        
        # Provide specific solutions based on error patterns
        if "permission denied" in stderr_output.lower():
            solution = "Try running as administrator/sudo, or check file permissions"
        elif "no module named" in stderr_output.lower():
            solution = "Install missing dependencies: pip install -r requirements.txt"
        elif "externally-managed-environment" in stderr_output.lower():
            solution = "Use virtual environment: python -m venv .venv && activate it"
        elif "network" in stderr_output.lower() or "connection" in stderr_output.lower():
            solution = "Check internet connection and try again"
        elif "disk" in stderr_output.lower() or "space" in stderr_output.lower():
            solution = "Free up disk space and try again"
        else:
            solution = "Check the error details above and ensure all prerequisites are met"
        
        print_error_with_solution("", solution, f"SUBPROCESS_{e.returncode}")
    else:
        print_error_with_solution(error_msg, "Check system requirements and try again", f"SUBPROCESS_{e.returncode}")

def check_prerequisites():
    """Check system prerequisites before starting setup."""
    logger = logging.getLogger('setup')
    log_step_start("System Prerequisites Check")
    print("🔍 Checking system prerequisites...")
    
    issues = []
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    logger.info(f"Python version: {python_version}")
    
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ is required")
        logger.error(f"Python version {python_version} is too old (minimum 3.8)")
    else:
        logger.info(f"Python version {python_version} is compatible")
    
    # Check if running as admin on Windows (for some operations)
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            logger.info(f"Running as administrator: {is_admin}")
        except:
            is_admin = False
            logger.warning("Could not check administrator status")
        
        if not is_admin:
            print("   ⚠️  Not running as administrator - some operations may fail")
            log_step_warning("Prerequisites", "Not running as administrator")
    
    # Check available disk space
    try:
        import shutil
        free_space = shutil.disk_usage('.').free / (1024**3)  # GB
        logger.info(f"Available disk space: {free_space:.2f} GB")
        if free_space < 1:
            issues.append(f"Low disk space: {free_space:.1f}GB available (minimum 1GB required)")
            logger.error(f"Insufficient disk space: {free_space:.2f} GB")
    except Exception as e:
        logger.warning(f"Could not check disk space: {e}")
    
    # Check internet connectivity
    try:
        import urllib.request
        urllib.request.urlopen('https://pypi.org', timeout=5)
        print("   ✅ Internet connection available")
        logger.info("Internet connection: Available")
    except Exception as e:
        print("   ⚠️  No internet connection - offline installation only")
        log_step_warning("Prerequisites", f"No internet connection: {e}")
    
    if issues:
        print("   ❌ Prerequisites check failed:")
        logger.error("Prerequisites check failed:")
        for issue in issues:
            print(f"     - {issue}")
            logger.error(f"   - {issue}")
        log_step_error("System Prerequisites Check", "Prerequisites validation failed")
        return False
    else:
        print("   ✅ Prerequisites check passed")
        log_step_success("System Prerequisites Check")
        return True

def print_banner():
    """Print setup banner."""
    print("=" * 80)
    print("""
    ██╗     ███████╗██████╗ ██╗██████╗  █████╗     ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗
    ██║     ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗    ██║   ██║██╔═══██╗██║██╔════╝██╔════╝
    ██║     █████╗  ██████╔╝██║██║  ██║███████║    ██║   ██║██║   ██║██║██║     █████╗  
    ██║     ██╔══╝  ██╔═══╝ ██║██║  ██║██╔══██║    ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝  
    ███████╗███████╗██║     ██║██████╔╝██║  ██║     ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗
    ╚══════╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝      ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝
                                                                                        
                         █████╗ ███████╗███████╗██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗
                        ██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝
                        ███████║███████╗███████╗██║███████╗   ██║   ███████║██╔██╗ ██║   ██║   
                        ██╔══██║╚════██║╚════██║██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║   
                        ██║  ██║███████║███████║██║███████║   ██║   ██║  ██║██║ ╚████║   ██║   
                        ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   
    """)
    print("🤖 INTELLIGENT VOICE ASSISTANT SETUP & INSTALLATION")
    print("=" * 80)
    print("🎯 Offline/Online Voice Assistant powered by advanced AI technologies")
    print("🚀 Setting up your personal AI assistant...")
    print("=" * 80)
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

def setup_virtual_environment():
    """Create and setup virtual environment."""
    print("🐍 Setting up virtual environment...")
    
    venv_path = Path(".venv")
    
    # Check if virtual environment already exists
    if venv_path.exists():
        print("   ✅ Virtual environment already exists")
        
        # Check if we're currently in the virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("   ✅ Currently running in virtual environment")
            return True
        else:
            print("   ⚠️  Virtual environment exists but not activated")
            print("   To activate: .venv\\Scripts\\activate (Windows) or source .venv/bin/activate (Linux/Mac)")
            return True
    
    try:
        # Create virtual environment
        print("   Creating virtual environment...")
        
        # Determine the correct Python executable
        python_cmd = "python3" if platform.system() != "Windows" else "python"
        
        # Try python3 first, fallback to python
        try:
            result = subprocess.run([python_cmd, "-m", "venv", ".venv"], 
                                  check=True, capture_output=True, text=True, timeout=300)
            print("   ✅ Virtual environment created successfully")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            if python_cmd == "python3":
                python_cmd = "python"
                try:
                    result = subprocess.run([python_cmd, "-m", "venv", ".venv"], 
                                          check=True, capture_output=True, text=True, timeout=300)
                    print("   ✅ Virtual environment created successfully")
                except subprocess.CalledProcessError as e2:
                    handle_subprocess_error(e2, "Virtual environment creation")
                    return False
            else:
                handle_subprocess_error(e, "Virtual environment creation")
                return False
        except subprocess.TimeoutExpired:
            print_error_with_solution(
                "Virtual environment creation timed out",
                "Try again with a faster internet connection or manually create: python -m venv .venv",
                "VENV_TIMEOUT"
            )
            return False
        
        # Provide activation instructions
        if platform.system() == "Windows":
            activation_cmd = ".venv\\Scripts\\activate"
        else:
            activation_cmd = "source .venv/bin/activate"
        
        print(f"   To activate: {activation_cmd}")
        print("   ⚠️  Please activate the virtual environment and run setup again")
        print(f"   Command: {activation_cmd} && python setup_assistant.py")
        
        return True
        
    except PermissionError:
        print_error_with_solution(
            "Permission denied while creating virtual environment",
            "Run as administrator (Windows) or with sudo (Linux/Mac), or choose a different directory",
            "VENV_PERMISSION"
        )
        return False
    except OSError as e:
        if "No space left on device" in str(e):
            print_error_with_solution(
                "Insufficient disk space for virtual environment",
                "Free up at least 500MB of disk space and try again",
                "VENV_DISK_SPACE"
            )
        else:
            print_error_with_solution(
                f"OS error during virtual environment creation: {e}",
                "Check system requirements and available resources",
                "VENV_OS_ERROR"
            )
        return False
    except Exception as e:
        print_error_with_solution(
            f"Unexpected error during virtual environment setup: {e}",
            "Try manually creating virtual environment: python -m venv .venv",
            "VENV_UNKNOWN"
        )
        return False

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
        print_error_with_solution(
            "requirements.txt not found",
            "Ensure you're in the correct project directory or create requirements.txt",
            "REQ_FILE_MISSING"
        )
        return False
    
    try:
        # Check if we're in a virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        if not in_venv and Path(".venv").exists():
            print("   ⚠️  Virtual environment exists but not activated")
            print("   Consider activating it before installing dependencies")
        
        print("   Installing Python packages...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"
        ], check=True, capture_output=True, text=True, timeout=1800)  # 30 minute timeout
        
        print("   ✅ Dependencies installed successfully")
        
        # Check for potential issues in pip output
        if result.stderr and "WARNING" in result.stderr:
            print("   ⚠️  Some warnings occurred during installation:")
            warnings = [line for line in result.stderr.split('\n') if 'WARNING' in line]
            for warning in warnings[:3]:  # Show first 3 warnings
                print(f"     {warning.strip()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e, "Dependencies installation")
        
        # Additional specific error handling
        if hasattr(e, 'stderr') and e.stderr:
            stderr_lower = e.stderr.lower()
            if "externally-managed-environment" in stderr_lower:
                print_error_with_solution(
                    "Python environment is externally managed",
                    "Use virtual environment: python -m venv .venv && activate it, then run setup again",
                    "PIP_EXTERNALLY_MANAGED"
                )
            elif "could not find a version" in stderr_lower:
                print_error_with_solution(
                    "Some packages are not available for your Python version",
                    "Update Python to 3.8+ or check requirements.txt for compatibility",
                    "PIP_VERSION_CONFLICT"
                )
            elif "no space left" in stderr_lower:
                print_error_with_solution(
                    "Insufficient disk space",
                    "Free up disk space and try again",
                    "PIP_DISK_SPACE"
                )
        return False
        
    except subprocess.TimeoutExpired:
        print_error_with_solution(
            "Package installation timed out",
            "Check internet connection and try again",
            "PIP_TIMEOUT"
        )
        return False
        
    except FileNotFoundError:
        print_error_with_solution(
            "pip command not found",
            "Ensure Python is properly installed and added to PATH",
            "PIP_NOT_FOUND"
        )
        return False
        
    except Exception as e:
        print_error_with_solution(
            f"Unexpected error during dependency installation: {e}",
            "Try installing dependencies manually: pip install -r requirements.txt",
            "PIP_UNKNOWN"
        )
        return False

def setup_frontend():
    """Setup frontend web interface."""
    print("🌐 Setting up frontend web interface...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print_error_with_solution(
            "Frontend directory not found",
            "Ensure you're in the correct project directory with frontend/ folder",
            "FRONTEND_DIR_MISSING"
        )
        return False
    
    # Check if frontend requirements.txt exists
    frontend_requirements = frontend_dir / "requirements.txt"
    if not frontend_requirements.exists():
        print_error_with_solution(
            "Frontend requirements.txt not found",
            "Create frontend/requirements.txt or check project structure",
            "FRONTEND_REQ_MISSING"
        )
        return False
    
    try:
        # Install frontend dependencies
        print("   Installing frontend dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(frontend_requirements)
        ], check=True, capture_output=True, text=True, timeout=1800)
        print("   ✅ Frontend dependencies installed")
        
        # Create frontend templates directory if not exists
        try:
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
        except PermissionError:
            print_error_with_solution(
                "Permission denied creating frontend directories",
                "Run as administrator or check directory permissions",
                "FRONTEND_PERMISSION"
            )
            return False
        
        # Test frontend app import
        frontend_app = frontend_dir / "app.py"
        if frontend_app.exists():
            try:
                # Try to validate the frontend app
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                    temp_file.write(f"""
import sys
sys.path.insert(0, '{frontend_dir.absolute()}')
try:
    import app
    print('Frontend app validation: OK')
except ImportError as e:
    print(f'Frontend app validation failed: {{e}}')
except Exception as e:
    print(f'Frontend app has issues: {{e}}')
""")
                    temp_file.flush()
                    
                    validation_result = subprocess.run([
                        sys.executable, temp_file.name
                    ], capture_output=True, text=True, timeout=30)
                    
                    if "validation: OK" in validation_result.stdout:
                        print("   ✅ Frontend Flask app validated")
                    else:
                        print("   ⚠️  Frontend app has validation issues")
                        if validation_result.stdout:
                            print(f"     {validation_result.stdout.strip()}")
                
                # Clean up temp file
                try:
                    Path(temp_file.name).unlink()
                except:
                    pass
                    
            except Exception as e:
                print(f"   ⚠️  Could not validate frontend app: {e}")
        else:
            print_error_with_solution(
                "Frontend Flask app (app.py) not found",
                "Ensure frontend/app.py exists or check project structure",
                "FRONTEND_APP_MISSING"
            )
        
        print("✅ Frontend setup completed successfully")
        print("   To start frontend: cd frontend && python app.py")
        print("   Web interface: http://localhost:5000")
        return True
        
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e, "Frontend dependencies installation")
        return False
        
    except subprocess.TimeoutExpired:
        print_error_with_solution(
            "Frontend installation timed out",
            "Check internet connection and try again",
            "FRONTEND_TIMEOUT"
        )
        return False
        
    except Exception as e:
        print_error_with_solution(
            f"Frontend setup failed: {e}",
            "Check frontend directory structure and requirements.txt",
            "FRONTEND_UNKNOWN"
        )
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
    logger = logging.getLogger('setup')
    log_step_start("Audio Assets Generation")
    print("🎵 Generating audio assets...")
    
    try:
        # Try importing the audio generation module
        from assets.audio.generate_audio_assets import create_audio_assets
        
        # Create the audio assets
        success = create_audio_assets()
        if success:
            print("✅ Audio assets generated successfully")
            log_step_success("Audio Assets Generation")
            return True
        else:
            print("❌ Failed to generate audio assets")
            log_step_error("Audio Assets Generation", "Audio generation function returned False")
            return False
            
    except ImportError as e:
        missing_dep = str(e).split("'")[1] if "'" in str(e) else str(e)
        error_msg = f"Missing dependency for audio generation: {missing_dep}"
        print(f"❌ {error_msg}")
        
        if "numpy" in str(e).lower():
            solution = "Install numpy: pip install numpy"
            error_code = "AUDIO_NUMPY_MISSING"
        elif "soundfile" in str(e).lower():
            solution = "Install soundfile: pip install soundfile"
            error_code = "AUDIO_SOUNDFILE_MISSING"
        else:
            solution = "Install audio dependencies: pip install numpy soundfile"
            error_code = "AUDIO_DEPS_MISSING"
        
        print_error_with_solution(error_msg, solution, error_code)
        print("   You can generate them manually by running:")
        print("   python assets/audio/generate_audio_assets.py")
        
        log_step_warning("Audio Assets Generation", f"Skipped due to missing dependencies: {missing_dep}")
        return True  # Don't fail setup for optional audio assets
        
    except FileNotFoundError:
        error_msg = "Audio generation script not found"
        print(f"❌ {error_msg}")
        print_error_with_solution(
            error_msg,
            "Ensure assets/audio/generate_audio_assets.py exists in the project",
            "AUDIO_SCRIPT_MISSING"
        )
        log_step_warning("Audio Assets Generation", "Audio generation script not found")
        return True  # Don't fail setup for missing script
        
    except Exception as e:
        error_msg = f"Unexpected error during audio generation: {e}"
        print(f"❌ {error_msg}")
        print_error_with_solution(
            error_msg,
            "Check file permissions, disk space, and audio system",
            "AUDIO_UNKNOWN_ERROR"
        )
        print("   You can generate them manually by running:")
        print("   python assets/audio/generate_audio_assets.py")
        
        log_step_error("Audio Assets Generation", str(e), traceback.format_exc())
        return True  # Don't fail setup for audio generation issues

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
    print("=" * 80)
    print("🎉 SETUP COMPLETED SUCCESSFULLY! 🎉")
    print("=" * 80)
    print("""
    ░██████╗███████╗████████╗██╗░░░██╗██████╗░  ░█████╗░░█████╗░███╗░░░███╗██████╗░██╗░░░░░███████╗████████╗███████╗██████╗░
    ██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗  ██╔══██╗██╔══██╗████╗░████║██╔══██╗██║░░░░░██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝  ██║░░╚═╝██║░░██║██╔████╔██║██████╔╝██║░░░░░█████╗░░░░░██║░░░█████╗░░██║░░██║
    ░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░  ██║░░██╗██║░░██║██║╚██╔╝██║██╔═══╝░██║░░░░░██╔══╝░░░░░██║░░░██╔══╝░░██║░░██║
    ██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░░░░░███████╗███████╗░░░██║░░░███████╗██████╔╝
    ╚═════╝░╚══════╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚══════╝╚══════╝░░░╚═╝░░░╚══════╝╚═════╝░
    """)
    print()
    
    # Check if we're in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    venv_exists = Path(".venv").exists()
    
    if venv_exists and not in_venv:
        print("⚠️  IMPORTANT: Activate your virtual environment first!")
        if platform.system() == "Windows":
            print("   Command: .venv\\Scripts\\activate")
        else:
            print("   Command: source .venv/bin/activate")
        print()
    
    print("🚀 Next steps:")
    print("1. Run health check: python cli.py health")
    print("2. Test TTS: python cli.py test-tts")
    print("3. Test STT: python cli.py test-stt")
    print("4. List audio devices: python cli.py devices")
    print("5. Start voice assistant: python cli.py run")
    print("6. Start web interface: cd frontend && python app.py")
    print()
    print("🎯 Alternative launch methods:")
    print("- Simple launcher: python launcher.py")
    print("- Direct app: python app.py")
    print("- Web interface: http://localhost:5000 (after starting frontend)")
    print()
    print("⚙️  Configuration files:")
    print("- Edit config.yml for voice assistant settings")
    print("- Edit .env for API keys and environment variables")
    print()
    print("🔧 Troubleshooting:")
    print("- For detailed system report: python cli.py health")
    print("- For plugin validation: python -c \"from utils.plugin_validator import *\"")
    print("- Check logs in: logs/voice_assistant.log")
    print("=" * 80)

def print_setup_summary(failed_steps, error_log):
    """Print a comprehensive setup summary with troubleshooting info."""
    print("\n" + "=" * 80)
    if failed_steps:
        print("⚠️  SETUP COMPLETED WITH ISSUES")
        print("=" * 80)
        print(f"📊 Summary: {len(failed_steps)} step(s) failed")
        print("\n🔴 Failed Steps:")
        for i, step in enumerate(failed_steps, 1):
            print(f"   {i}. {step}")
        
        print("\n🔧 TROUBLESHOOTING GUIDE:")
        print("=" * 40)
        
        # Specific troubleshooting based on failed steps
        if any("virtual environment" in step.lower() for step in failed_steps):
            print("🐍 Virtual Environment Issues:")
            print("   • Try: python -m venv .venv")
            print("   • Or: python3 -m venv .venv")
            print("   • Check Python installation and permissions")
            print()
        
        if any("dependencies" in step.lower() for step in failed_steps):
            print("📦 Dependency Issues:")
            print("   • Activate virtual environment first")
            print("   • Try: pip install --upgrade pip")
            print("   • Check internet connection")
            print("   • Manual install: pip install -r requirements.txt")
            print()
        
        if any("frontend" in step.lower() for step in failed_steps):
            print("🌐 Frontend Issues:")
            print("   • Check frontend/ directory exists")
            print("   • Verify frontend/requirements.txt")
            print("   • Try: cd frontend && pip install -r requirements.txt")
            print()
        
        if any("audio" in step.lower() for step in failed_steps):
            print("🎵 Audio System Issues:")
            print("   • Install audio drivers")
            print("   • Check microphone/speaker connections")
            print("   • May work without audio for text-only mode")
            print()
        
        print("🆘 RECOVERY OPTIONS:")
        print("   1. Run recovery mode: python setup_assistant.py --recovery")
        print("   2. Manual setup: Follow README.md instructions")
        print("   3. Quick setup: python setup_assistant.py --quick")
        print("   4. Check logs in: logs/setup_error.log")
        
    else:
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✅ All components installed and configured correctly")
    
    print("=" * 80)

def log_error_to_file(error_info):
    """Log error information to a file for debugging."""
    logger = logging.getLogger('setup')
    try:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        error_log_file = logs_dir / "setup_error.log"
        
        with open(error_log_file, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Error: {error_info.get('error', 'Unknown')}\n")
            f.write(f"Step: {error_info.get('step', 'Unknown')}\n")
            if 'traceback' in error_info:
                f.write(f"Traceback:\n{error_info['traceback']}\n")
            f.write(f"{'='*50}\n")
            
        print(f"   📝 Error logged to: {error_log_file}")
        logger.info(f"Error details logged to: {error_log_file}")
    except Exception as e:
        print(f"   ⚠️  Could not log error: {e}")
        logger.warning(f"Could not log error to file: {e}")

def safe_step_execution(step_name, step_func):
    """Safely execute a setup step with comprehensive error handling."""
    logger = logging.getLogger('setup')
    
    try:
        log_step_start(step_name)
        print(f"\n🔄 {step_name}...")
        
        start_time = time.time()
        result = step_func()
        end_time = time.time()
        execution_time = end_time - start_time
        
        if result:
            print(f"   ✅ {step_name} completed successfully")
            log_step_success(f"{step_name} (executed in {execution_time:.2f}s)")
        else:
            print(f"   ❌ {step_name} failed")
            log_step_error(step_name, "Step function returned False")
        
        return result
        
    except KeyboardInterrupt:
        print(f"\n   ⏹️  {step_name} interrupted by user")
        print("   Setup cancelled. You can resume by running setup again.")
        log_step_error(step_name, "Interrupted by user")
        return False
        
    except Exception as e:
        error_info = {
            'error': str(e),
            'step': step_name,
            'traceback': traceback.format_exc()
        }
        print(f"   ❌ {step_name} failed with exception: {e}")
        log_step_error(step_name, str(e), traceback.format_exc())
        log_error_to_file(error_info)
        
        # Provide step-specific recovery suggestions
        if "virtual environment" in step_name.lower():
            print("   💡 Try manually: python -m venv .venv")
            logger.info("   Recovery suggestion: python -m venv .venv")
        elif "dependencies" in step_name.lower():
            print("   💡 Try manually: pip install -r requirements.txt")
            logger.info("   Recovery suggestion: pip install -r requirements.txt")
        elif "frontend" in step_name.lower():
            print("   💡 Try: python setup_assistant.py --frontend")
            logger.info("   Recovery suggestion: python setup_assistant.py --frontend")
        
        return False

def recovery_mode():
    """Run setup in recovery mode for fixing issues."""
    print("=" * 80)
    print("""
    ██████╗░███████╗░█████╗░░█████╗░██╗░░░██╗███████╗██████╗░██╗░░░██╗  ███╗░░░███╗░█████╗░██████╗░███████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║░░░██║██╔════╝██╔══██╗╚██╗░██╔╝  ████╗░████║██╔══██╗██╔══██╗██╔════╝
    ██████╔╝█████╗░░██║░░╚═╝██║░░██║╚██╗░██╔╝█████╗░░██████╔╝░╚████╔╝░  ██╔████╔██║██║░░██║██║░░██║█████╗░░
    ██╔══██╗██╔══╝░░██║░░██╗██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗░░╚██╔╝░░  ██║╚██╔╝██║██║░░██║██║░░██║██╔══╝░░
    ██║░░██║███████╗╚█████╔╝╚█████╔╝░░╚██╔╝░░███████╗██║░░██║░░░██║░░░  ██║░╚═╝░██║╚█████╔╝██████╔╝███████╗
    ╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░░░░╚═╝░╚════╝░╚═════╝░╚══════╝
    """)
    print("🔧 RECOVERY MODE - Fixing Common Issues")
    print("=" * 80)
    print("This mode will attempt to fix common issues")
    print()
    
    recovery_steps = [
        ("Checking prerequisites", check_prerequisites),
        ("Recreating directories", create_directories),
        ("Regenerating .env file", setup_environment),
        ("Regenerating audio assets", generate_audio_assets),
        ("Testing configuration", validate_configuration),
    ]
    
    failed_recovery_steps = []
    
    for step_name, step_func in recovery_steps:
        if not safe_step_execution(step_name, step_func):
            failed_recovery_steps.append(step_name)
    
    print("\n" + "=" * 80)
    if failed_recovery_steps:
        print("⚠️  Recovery completed with some issues")
        print(f"Failed recovery steps: {', '.join(failed_recovery_steps)}")
        print("\n💡 Manual recovery suggestions:")
        print("   1. Check file permissions")
        print("   2. Ensure you're in the correct directory")
        print("   3. Try running as administrator")
        print("   4. Check disk space and internet connection")
    else:
        print("✅ Recovery mode completed successfully")
    
    print("\nNext step: Try running the full setup again:")
    print("   python setup_assistant.py")
    print("=" * 80)
    print("=" * 80)
    print("""
    ██████╗░███████╗░█████╗░░█████╗░██╗░░░██╗███████╗██████╗░██╗░░░██╗  ███╗░░░███╗░█████╗░██████╗░███████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║░░░██║██╔════╝██╔══██╗╚██╗░██╔╝  ████╗░████║██╔══██╗██╔══██╗██╔════╝
    ██████╔╝█████╗░░██║░░╚═╝██║░░██║╚██╗░██╔╝█████╗░░██████╔╝░╚████╔╝░  ██╔████╔██║██║░░██║██║░░██║█████╗░░
    ██╔══██╗██╔══╝░░██║░░██╗██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗░░╚██╔╝░░  ██║╚██╔╝██║██║░░██║██║░░██║██╔══╝░░
    ██║░░██║███████╗╚█████╔╝╚█████╔╝░░╚██╔╝░░███████╗██║░░██║░░░██║░░░  ██║░╚═╝░██║╚█████╔╝██████╔╝███████╗
    ╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░░░░╚═╝░╚════╝░╚═════╝░╚══════╝
    """)
    print("🔧 RECOVERY MODE - Fixing Common Issues")
    print("=" * 80)
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

# --- FFMPEG SETUP STEP ---
def setup_ffmpeg():
    """Check and setup ffmpeg for audio processing."""
    print("🔎 Checking ffmpeg installation...")
    import shutil
    ffmpeg_bin_path = os.path.abspath(os.path.join("bin", "ffmpeg", "ffmpeg.exe"))
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path or os.path.isfile(ffmpeg_bin_path):
        found_path = ffmpeg_path if ffmpeg_path else ffmpeg_bin_path
        print(f"   ✅ ffmpeg found: {found_path}")
        return True
    system = platform.system()
    arch = platform.machine().lower()
    # Use n7.1-latest release pattern
    ffmpeg_base_url = "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/"
    ffmpeg_filename = None
    if system == "Windows":
        print("   ❌ ffmpeg not found on PATH. Attempting automatic download...")
        if "arm" in arch or "aarch" in arch:
            ffmpeg_filename = "ffmpeg-n7.1-latest-winarm64-lgpl-shared-7.1.zip"
        elif "64" in arch:
            ffmpeg_filename = "ffmpeg-n7.1-latest-win64-lgpl-shared-7.1.zip"
        else:
            ffmpeg_filename = "ffmpeg-n7.1-latest-win32-lgpl-shared-7.1.zip"
        ffmpeg_url = ffmpeg_base_url + ffmpeg_filename
        try:
            print(f"   Downloading ffmpeg from: {ffmpeg_url}")
            temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            with requests.get(ffmpeg_url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    temp_zip.write(chunk)
            temp_zip.close()
            print("   Extracting ffmpeg to bin/ffmpeg ...")
            extract_dir = os.path.join("bin", "ffmpeg")
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(temp_zip.name, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            # Flatten extracted structure: move all files from versioned subfolder to bin/ffmpeg
            # Find the first subfolder (usually ffmpeg-n7.1-latest-win32-lgpl-shared-7.1)
            subfolders = [f for f in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, f))]
            if subfolders:
                versioned_dir = os.path.join(extract_dir, subfolders[0])
                # Move all files from versioned_dir to extract_dir
                for root, dirs, files in os.walk(versioned_dir):
                    for file in files:
                        src_file = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file, versioned_dir)
                        dest_file = os.path.join(extract_dir, rel_path)
                        dest_folder = os.path.dirname(dest_file)
                        os.makedirs(dest_folder, exist_ok=True)
                        shutil.move(src_file, dest_file)
                # Remove the now-empty versioned_dir
                try:
                    shutil.rmtree(versioned_dir)
                except Exception as rm_err:
                    print(f"   ⚠️  Failed to remove versioned folder: {rm_err}")
            # Find ffmpeg.exe in bin/ffmpeg
            ffmpeg_exe = None
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.lower() == "ffmpeg.exe":
                        ffmpeg_exe = os.path.join(root, file)
                        break
            # Ensure ffmpeg.exe is at bin/ffmpeg/ffmpeg.exe
            ffmpeg_target = os.path.join(extract_dir, "ffmpeg.exe")
            if ffmpeg_exe and os.path.isfile(ffmpeg_exe):
                if ffmpeg_exe != ffmpeg_target:
                    try:
                        shutil.copy2(ffmpeg_exe, ffmpeg_target)
                        print(f"   ffmpeg.exe copied to: {ffmpeg_target}")
                    except Exception as move_err:
                        print(f"   ⚠️  Failed to copy ffmpeg.exe to bin/ffmpeg: {move_err}")
                ffmpeg_exe = ffmpeg_target
            # Check if bin/ffmpeg/ffmpeg.exe exists
            if os.path.isfile(ffmpeg_target):
                print(f"   ✅ ffmpeg extracted: {ffmpeg_target}")
                os.environ["FFMPEG_PATH"] = ffmpeg_target
                print(f"   FFMPEG_PATH set for application: {ffmpeg_target}")
                os.environ["PATH"] = os.path.dirname(ffmpeg_target) + os.pathsep + os.environ.get("PATH", "")
                print(f"   PATH updated for ffmpeg usage.")
                return True
            else:
                print("   ❌ bin/ffmpeg/ffmpeg.exe not found after extraction. Please download manually.")
                print("   Download: https://github.com/BtbN/FFmpeg-Builds/releases")
                return False
        except Exception as e:
            print(f"   ❌ ffmpeg download error: {e}")
            print("   Please download manually from https://github.com/BtbN/FFmpeg-Builds/releases")
            return False
    elif system in ("Linux", "Darwin"):
        print("   ❌ ffmpeg not found. Attempting automatic install...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"], check=True)
            ffmpeg_path = shutil.which("ffmpeg")
            if ffmpeg_path:
                print(f"   ✅ ffmpeg installed: {ffmpeg_path}")
                return True
            else:
                print("   ❌ ffmpeg install failed. Please install manually.")
                print("   Try: sudo apt-get install ffmpeg")
                return False
        except Exception as e:
            print(f"   ❌ ffmpeg install error: {e}")
            print("   Please install ffmpeg manually and rerun setup.")
            print("   Download: https://github.com/BtbN/FFmpeg-Builds/releases")
            return False
    else:
        print(f"   ❌ ffmpeg not found. Please install ffmpeg for {system}.")
        print("   Download: https://github.com/BtbN/FFmpeg-Builds/releases")
        return False

# main() and rest of the code
def main():
    """Main setup function."""
    
    # Setup logging first
    logger = setup_logging()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        logger.info(f"Setup mode: {sys.argv[1]}")
        
        if sys.argv[1] == "--recovery":
            logger.info("Starting recovery mode")
            recovery_mode()
            return
        elif sys.argv[1] == "--quick":
            logger.info("Starting quick setup mode")
            print("=" * 80)
            print("""
    ░██████╗░██╗░░░██╗██╗░█████╗░██╗░░██╗  ░██████╗███████╗████████╗██╗░░░██╗██████╗░
    ██╔═══██╗██║░░░██║██║██╔══██╗██║░██╔╝  ██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗
    ██║██╗██║██║░░░██║██║██║░░╚═╝█████═╝░  ╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝
    ╚██████╔╝██║░░░██║██║██║░░██╗██╔═██╗░  ░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░
    ░╚═██╔═╝░╚██████╔╝██║╚█████╔╝██║░╚██╗  ██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░
    ░░░╚═╝░░░░╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝  ╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░
            """)
            print("🚀 QUICK SETUP MODE - Essential Components Only")
            print("=" * 80)
            quick_steps = [
                ("Checking Python version", check_python_version),
                ("Setting up virtual environment", setup_virtual_environment),
                ("Creating directories", create_directories),
                ("Setting up environment", setup_environment),
                ("Generating audio assets", generate_audio_assets),
            ]
            
            failed_steps = []
            for step_name, step_func in quick_steps:
                if not safe_step_execution(step_name, step_func):
                    failed_steps.append(step_name)
            
            logger.info(f"Quick setup completed. Failed steps: {len(failed_steps)}")
            print_setup_summary(failed_steps, {})
            return
            
        elif sys.argv[1] == "--frontend":
            logger.info("Starting frontend setup mode")
            print("=" * 80)
            print("""
    ███████╗██████╗░░█████╗░███╗░░██╗████████╗███████╗███╗░░██╗██████╗░  ░██████╗███████╗████████╗██╗░░░██╗██████╗░
    ██╔════╝██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔════╝████╗░██║██╔══██╗  ██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗
    █████╗░░██████╔╝██║░░██║██╔██╗██║░░░██║░░░█████╗░░██╔██╗██║██║░░██║  ╚█████╗░█████╗░░░░██║░░░██║░░░██║██████╔╝
    ██╔══╝░░██╔══██╗██║░░██║██║╚████║░░░██║░░░██╔══╝░░██║╚████║██║░░██║  ░╚═══██╗██╔══╝░░░░██║░░░██║░░░██║██╔═══╝░
    ██║░░░░░██║░░██║╚█████╔╝██║░╚███║░░░██║░░░███████╗██║░╚███║██████╔╝  ██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░
    ╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═════╝░  ╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═════╝░
            """)
            print("🌐 FRONTEND SETUP MODE - Web Interface Configuration")
            print("=" * 80)
            frontend_steps = [
                ("Checking Python version", check_python_version),
                ("Setting up virtual environment", setup_virtual_environment),
                ("Setting up frontend", setup_frontend),
            ]
            
            failed_steps = []
            for step_name, step_func in frontend_steps:
                if not safe_step_execution(step_name, step_func):
                    failed_steps.append(step_name)
                    break  # Stop on first failure for frontend mode
            
            if not failed_steps:
                print("✅ Frontend setup completed")
                print("🌐 Start frontend: cd frontend && python app.py")
                print("🌐 Web interface: http://localhost:5000")
                logger.info("Frontend setup completed successfully")
            else:
                logger.error(f"Frontend setup failed. Failed steps: {failed_steps}")
                print_setup_summary(failed_steps, {})
            return
            
        elif sys.argv[1] == "--help":
            logger.info("Displaying help information")
            print("Voice Assistant Setup Options:")
            print("  python setup_assistant.py          # Full setup (includes virtual environment)")
            print("  python setup_assistant.py --quick  # Quick setup (no dependencies, includes venv)")
            print("  python setup_assistant.py --frontend # Setup frontend only (includes venv)")
            print("  python setup_assistant.py --recovery # Fix common issues")
            print("  python setup_assistant.py --help   # Show this help")
            print()
            print("Virtual Environment:")
            print("  The setup will create a .venv folder with isolated Python packages.")
            print("  After setup, activate it with:")
            if platform.system() == "Windows":
                print("    .venv\\Scripts\\activate")
            else:
                print("    source .venv/bin/activate")
            print()
            print("Error Handling:")
            print("  • All errors are logged to logs/setup_error.log")
            print("  • Use --recovery mode to fix common issues")
            print("  • Check troubleshooting guide after failed setup")
            return
    
    # Main setup with prerequisites check
    try:
        logger.info("Starting full setup mode")
        print_banner()
        
        # Check prerequisites first
        if not check_prerequisites():
            logger.error("Prerequisites check failed - aborting setup")
            print("\n❌ Prerequisites check failed. Please fix the issues above and try again.")
            print("💡 Try recovery mode: python setup_assistant.py --recovery")
            return
        
        # Setup steps
        steps = [
            ("Checking Python version", check_python_version),
            ("Setting up virtual environment", setup_virtual_environment),
            ("Checking system requirements", check_system_requirements),
            ("Checking audio system", check_audio_system),
            ("Checking ffmpeg installation", setup_ffmpeg),
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
        
        logger.info(f"Starting {len(steps)} setup steps")
        failed_steps = []
        error_log = {}
        
        for step_name, step_func in steps:
            if not safe_step_execution(step_name, step_func):
                failed_steps.append(step_name)
        
        logger.info(f"Setup completed. Failed steps: {len(failed_steps)}/{len(steps)}")
        if failed_steps:
            logger.error(f"Failed steps: {', '.join(failed_steps)}")
        
        print_setup_summary(failed_steps, error_log)
        
        if not failed_steps:
            logger.info("Setup completed successfully - all steps passed")
            setup_complete()
        else:
            logger.warning(f"Setup completed with {len(failed_steps)} failed steps")
            print(f"\n🔧 To fix issues, try:")
            print(f"   python setup_assistant.py --recovery")
            
    except KeyboardInterrupt:
        logger.warning("Setup interrupted by user")
        print("\n\n⏹️  Setup interrupted by user")
        print("You can resume setup by running the command again.")
    except Exception as e:
        logger.critical(f"Critical setup error: {e}")
        logger.critical(f"Traceback:\n{traceback.format_exc()}")
        print(f"\n❌ Critical setup error: {e}")
        print("💡 Try recovery mode: python setup_assistant.py --recovery")
        log_error_to_file({
            'error': str(e),
            'step': 'Main setup',
            'traceback': traceback.format_exc()
        })
    finally:
        logger.info("Setup session ended")
        logger.info("=" * 80)

if __name__ == "__main__":
    main()
