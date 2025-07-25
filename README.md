# 🎤 Lepida Voice Assistant

A powerful, modular voice assistant application designed for offline/online operation with advanced AI technologies. Features complete Indonesian language support, plugin-based architecture, and comprehensive system monitoring.

## 🌟 Key Highlights

- **🇮🇩 Indonesian Language Optimized**: Full support for Bahasa Indonesia
- **🔒 Privacy-First**: Works completely offline when needed
- **🧩 Modular Architecture**: Plugin-based system for easy extension
- **📊 Smart Monitoring**: Built-in system health and performance monitoring
- **🌐 Web Interface**: Complete web-based control panel
- **⚡ Real-time Processing**: Fast voice recognition and response

## 🚀 Features

- **🗣️ Text-to-Speech (TTS)**: Facebook MMS TTS for Indonesian language with multiple fallback engines
- **👂 Speech-to-Text (STT)**: Offline speech recognition with Whisper.cpp and Google STT fallback
- **🔊 Audio Processing**: Advanced microphone input and speaker output handling
- **⚡ Wake Word Detection**: Configurable wake word activation with Porcupine
- **🧠 Command Processing**: Intelligent command interpretation and execution
- **🔌 Plugin System**: Modular architecture for TTS, STT, wake word, and sound effects
- **⚙️ Configuration Management**: YAML-based configuration with environment variables
- **📱 CLI Interface**: Comprehensive command-line tools for management
- **🌐 Web Dashboard**: Modern web interface for remote control and monitoring
- **🏥 Health Monitoring**: Comprehensive system health checks and diagnostics
- **📊 System Monitoring**: Real-time CPU, memory, disk, and network monitoring
- **🛠️ Plugin Validation**: Automatic plugin validation and testing system
- **🔧 Auto Setup**: Intelligent setup assistant for easy installation

## �️ Complete System Architecture

### ✅ **Core Modules (All Available)**

1. **app.py** - Main application entry point with voice processing pipeline
2. **command.py** - Intelligent command processing and text interpretation *(Recently Added)*
3. **cli.py** - Comprehensive CLI management tool with commands:
   - `setup` - Complete system setup and health check
   - `health` - Run comprehensive health diagnostics
   - `assets` - Generate audio assets automatically
   - `test-tts` - Test text-to-speech functionality
   - `test-stt` - Test speech-to-text functionality  
   - `devices` - List and configure audio devices
   - `run` - Start voice assistant with options

4. **launcher.py** - Simple launcher script for quick startup
5. **setup_assistant.py** - Automated setup script with dependency management *(Enhanced)*

### ✅ **Utility Modules (All Available)**

1. **utils/text_to_speech.py** - TTS engine wrapper with plugin management
2. **utils/audio_transcription.py** - Audio transcription from various engines
3. **utils/command_processor.py** - Voice command processing and execution
4. **utils/wake_word_detection.py** - Wake word detection and activation management
5. **utils/system_monitor.py** - Real-time system resource monitoring *(Recently Added)*
6. **utils/health_check.py** - Comprehensive health checking system:
   - Dependency validation and version checking
   - Configuration file validation
   - Audio system testing and device detection
   - Model availability checks
   - Asset verification and permissions
   - Plugin validation and testing

7. **utils/performance_monitor.py** - System performance monitoring:
   - CPU/Memory/Disk usage monitoring
   - Audio device monitoring and latency testing
   - Process resource tracking
   - Threshold alerting and notifications

8. **utils/plugin_validator.py** - Plugin validation system:
   - TTS plugin validation and testing
   - STT plugin validation and testing  
   - Wake word plugin validation
   - Sound FX plugin validation
   - Dependency checking and compatibility testing

### ✅ **Frontend & Web Interface (Complete)**

1. **frontend/app.py** - Flask web server with comprehensive API
2. **frontend/templates/index.html** - Modern responsive web dashboard
3. **frontend/static/css/style.css** - Complete styling and responsive design
4. **frontend/static/js/app.js** - Frontend JavaScript with real-time updates

**Web Interface Features:**
- 🎛️ System status dashboard with real-time monitoring
- 🗣️ Text-to-speech testing with voice selection
- 👂 Speech-to-text testing with microphone input
- ⚙️ Configuration management interface
- 📊 System performance monitoring graphs
- 🔌 Plugin management and validation
- 📱 Mobile-responsive design

### ✅ **Helper & Support Modules**

1. **helper/audio_processing.py** - Audio processing utilities
2. **helper/numberToText.py** - Number to Indonesian text conversion *(Enhanced)*
3. **config/config.py** - Configuration loader and management
4. **config/default.py** - Auto-create default configurations
## 📁 Complete Project Structure

```
Lepida-Voice-Assistant/
├── app.py                      # Main entry: initialization and main control
├── command.py                  # Text processing & command interpretation ⭐ NEW
├── launcher.py                 # Quick launcher script
├── cli.py                      # Comprehensive CLI management tool
├── setup_assistant.py          # Automated setup and installation
├── config.yml                  # Global application configuration
├── .env                        # Environment variables (API Keys, Paths, etc.)
├── .env.example                # Example .env contents  
├── requirements.txt            # Dependency list
├── README.md                   # Main documentation
├── .gitignore                  
├── .pre-commit-config.yaml     
│
├── assets/                     # Audio assets for user interaction
│   └── audio/
│       ├── audio.wav           # General audio file
│       ├── start.wav           # Startup sound
│       ├── stop.wav            # Shutdown sound
│       ├── error.wav           # Error notification
│       ├── success.wav         # Success confirmation
│       ├── notification.wav    # General notification
│       ├── welcome.wav         # Welcome greeting
│       ├── goodbye.wav         # Goodbye message
│       └── generate_audio_assets.py  # Asset generator script
│
├── config/
│   ├── config.py               # Configuration loader
│   └── default.py              # Auto-create config.yml if not available
│
├── frontend/                   # Web Interface ⭐ COMPLETE
│   ├── app.py                  # Flask web server with full API
│   ├── requirements.txt        # Frontend-specific dependencies
│   ├── README.md               # Frontend documentation
│   ├── templates/
│   │   └── index.html          # Modern responsive web dashboard
│   └── static/
│       ├── css/
│       │   └── style.css       # Complete responsive styling
│       └── js/
│           └── app.js          # Frontend JavaScript with real-time features
│
├── helper/                     # Helper modules
│   ├── audio_processing.py     # Audio processing (mic, output, etc.)
│   └── numberToText.py         # Number to text conversion (Indonesian) ⭐ ENHANCED
│
├── models/
│   ├── mms_tts.py              # MMS TTS implementation
│   └── autoload.py             # Plugin/model autoloader
│
├── plugins/                    # Modular plugin system
│   ├── tts_mms_tts.py          # Facebook MMS TTS plugin
│   ├── tts_coqui.py            # Coqui TTS plugin
│   ├── tts_piper.py            # Piper TTS plugin
│   ├── stt_whisper_cpp.py      # Whisper.cpp STT plugin
│   ├── stt_google_stt.py       # Google STT plugin
│   ├── wakeword_porcupine.py   # Porcupine wake word plugin
│   └── soundfx_beep.py         # Simple sound effects
│
├── utils/                      # Utility modules
│   ├── text_to_speech.py       # TTS engine wrapper
│   ├── audio_transcription.py  # Audio transcription from various engines
│   ├── command_processor.py    # Voice command processing
│   ├── wake_word_detection.py  # Wake word detection management
│   ├── system_monitor.py       # Real-time system monitoring ⭐ NEW
│   ├── health_check.py         # Comprehensive health checking
│   ├── performance_monitor.py  # System performance monitoring
│   ├── plugin_validator.py     # Plugin validation system
│   ├── audio_effects.py        # Audio effects and processing
│   └── audio_analysis.py       # Audio analysis utilities
│
├── test/                       # Testing suite
│   ├── test_global.py          # Global system test suite ⭐ COMPLETE
│   ├── test_voice_assistant.py # Voice assistant specific tests
│   └── test_whisper.py         # Whisper integration tests
│
├── outputs/                    # Generated outputs
│   └── sound/
│       └── output.wav          # TTS output files
│
├── logs/                       # Application logs
├── temp/                       # Temporary files
└── .github/
    └── copilot-instructions.md # AI assistant instructions
```

**Legend:** ⭐ = Recently added/enhanced components
│   ├── tts_mms_tts.py          # MMS TTS plugin
│   ├── stt_whisper_cpp.py      # Whisper.cpp STT plugin
│   └── soundfx_beep.py         # Simple sound effects
│
├── utils/
│   ├── audio_transcription.py  # Audio transcription from various engines
│   └── text_to_speech.py       # TTS engine wrapper
│
├── test/                       # Unit tests
│   └── _test.py
│
└── .github/
    └── copilot-instructions.md
```

## 🛠️ Quick Installation

### 🚀 **Automated Setup (Recommended)**
```bash
# Clone the repository
git clone <repository-url>
cd facebook-seacker

# Run automated setup
python setup_assistant.py

# Or with specific options
python setup_assistant.py --frontend  # Include web interface setup
```

### ✋ **Manual Installation**

#### 1. Clone and Install Dependencies
```bash
git clone <repository-url>
cd facebook-seacker
pip install -r requirements.txt
```

#### 2. Setup Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional for basic usage)
# nano .env
```

#### 3. Install Frontend (Optional)
```bash
cd frontend
pip install -r requirements.txt
cd ..
```

### 🔧 **System Requirements**

- **Python**: 3.8+ (3.10+ recommended)
- **Operating System**: Windows, Linux, macOS
- **Memory**: 2GB RAM minimum (4GB+ recommended)
- **Storage**: 1GB free space for models
- **Audio**: Microphone and speakers/headphones

### 🎯 **Platform-Specific Setup**

#### Windows:
```bash
# Install audio dependencies
pip install pyaudio
# If PyAudio fails, download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
pip install -r requirements.txt
```

#### macOS:
```bash
brew install portaudio
pip install -r requirements.txt
```
## 🚀 Usage Guide

### 🎤 **Voice Assistant Mode (Main)**
```bash
# Start the voice assistant
python app.py

# Start with wake word detection
python app.py --wake-word

# Start with specific config
python app.py --config custom_config.yml
```

### 🌐 **Web Dashboard (Remote Control)**
```bash
# Start web interface (in separate terminal)
cd frontend
python app.py

# Then open browser to: http://localhost:5000
```

### 🖥️ **Command Line Interface**
```bash
# System health check
python cli.py health

# Test text-to-speech
python cli.py test-tts "Halo, ini adalah tes suara"

# Test speech-to-text (requires microphone)
python cli.py test-stt

# List audio devices
python cli.py devices

# Complete system setup
python cli.py setup

# Generate audio assets
python cli.py assets
```

### 💬 **Direct Text-to-Speech**
```bash
# Single text conversion
python app.py "Selamat datang di Lepida Voice Assistant"

# Interactive mode
python app.py --interactive

# Save to file
python app.py "Halo dunia" --output output.wav
```

### 🔧 **Command Processing**
```bash
# Test command processing
python command.py "Jam berapa sekarang?"
python command.py "Saya punya 12 apel dan 5 jeruk"
python command.py "Matikan sistem"
```

### 🧪 **Testing & Diagnostics**
```bash
# Run global system tests
python test/test_global.py

# Run specific tests
python -m pytest test/

# Health monitoring
python -c "from utils.system_monitor import SystemMonitor; m=SystemMonitor(); print(m.get_summary())"
```

## ⚙️ Configuration

### 📋 **Main Configuration (`config.yml`)**
```yaml
# Voice Assistant Configuration
app:
  name: "Lepida Voice Assistant"
  description: "A offline/online voice assistant powered by advanced AI technologies."
  version: "1.0.0"
  language: "id"  # Indonesian

audio:
  input:
    device_index: null  # Auto-detect microphone
    sample_rate: 16000
    channels: 1
    chunk_size: 1024
    format: "int16"
  output:
    device_index: null  # Auto-detect speaker
    sample_rate: 22050
    channels: 1

tts:
  primary_engine: "mms_tts"
  fallback_engines: ["coqui_tts", "piper"]
  language: "id"
  speed: 1.0
  volume: 0.8

stt:
  primary_engine: "whisper_cpp"
  fallback_engines: ["google_stt"]
  language: "id"
  model_size: "base"

wake_word:
  enabled: true
  primary_engine: "porcupine"
  keywords: ["hey assistant", "lepida"]
  sensitivity: 0.5

plugins:
  auto_load: true
  validate_on_load: true
```

### 🔐 **Environment Variables (`.env`)**
```bash
# Optional API Keys
GOOGLE_STT_API_KEY=your_google_api_key_here
PORCUPINE_ACCESS_KEY=your_porcupine_access_key_here

# Audio Device Configuration
AUDIO_INPUT_DEVICE=auto
AUDIO_OUTPUT_DEVICE=auto

# Model Paths (optional - will use defaults if not set)
WHISPER_MODEL_PATH=models/whisper
TTS_MODEL_PATH=models/tts
PORCUPINE_MODEL_PATH=models/porcupine

# Application Settings
RUN_AS_SERVICE=false
DEBUG_MODE=false
OFFLINE_MODE=true
LOG_LEVEL=INFO

# Web Interface Settings
WEB_HOST=localhost
WEB_PORT=5000
WEB_DEBUG=false
```

### 🎛️ **Plugin Configuration**

Each plugin can be configured individually:

```yaml
plugins:
  tts:
    mms_tts:
      enabled: true
      model_path: "models/mms_tts"
      language: "id"
    coqui:
      enabled: false
      model_path: "models/coqui"
  
  stt:
    whisper_cpp:
      enabled: true
      model_path: "models/whisper"
      model_size: "base"
    google_stt:
      enabled: false
      api_key: "${GOOGLE_STT_API_KEY}"
```
## 🔌 Plugin System

The application uses a powerful modular plugin system for TTS, STT, wake word detection, and sound effects:

### 🗣️ **TTS Plugin Example**
```python
def run(text: str, lang: str = "id", output_file: str = None):
    """
    Convert text to speech.
    
    Args:
        text: Text to convert
        lang: Language code (default: "id" for Indonesian)
        output_file: Optional output file path
    
    Returns:
        Path to generated audio file or audio data
    """
    # Convert text to speech implementation
    pass

def get_voices():
    """Get available voices for this engine."""
    return ["id", "id-male", "id-female"]

def get_info():
    """Get plugin information."""
    return {
        "name": "MMS TTS Plugin",
        "description": "Facebook MMS TTS for Indonesian",
        "languages": ["id"],
        "version": "1.0.0",
        "author": "Lepida Team"
    }

def validate():
    """Validate plugin dependencies and configuration."""
    return {"valid": True, "message": "Plugin ready"}
```

### 👂 **STT Plugin Example**
```python
def transcribe(audio_file: str, language: str = "id"):
    """
    Transcribe audio file to text.
    
    Args:
        audio_file: Path to audio file
        language: Target language
    
    Returns:
        Transcribed text
    """
    # Speech recognition implementation
    pass

def transcribe_realtime(audio_stream, callback):
    """Real-time transcription from audio stream."""
    pass
```

### ⚡ **Available Plugins**

| Plugin Type | Plugin Name | Description | Status |
|-------------|-------------|-------------|---------|
| **TTS** | `mms_tts` | Facebook MMS TTS (Primary) | ✅ Ready |
| **TTS** | `coqui` | Coqui TTS Engine | ✅ Ready |
| **TTS** | `piper` | Piper TTS Engine | ✅ Ready |
| **STT** | `whisper_cpp` | Whisper.cpp (Primary) | ✅ Ready |
| **STT** | `google_stt` | Google Speech-to-Text | ✅ Ready |
| **Wake Word** | `porcupine` | Picovoice Porcupine | ✅ Ready |
| **Sound FX** | `beep` | Simple audio feedback | ✅ Ready |

### 🛠️ **Plugin Development**

#### 1. Create Plugin File
```bash
# Create new TTS plugin
touch plugins/tts_my_engine.py

# Create new STT plugin  
touch plugins/stt_my_engine.py
```

#### 2. Implement Required Functions
Follow the interface shown in examples above.

#### 3. Register Plugin
Add to `config.yml`:
```yaml
plugins:
  tts:
    my_engine:
      enabled: true
      # plugin-specific configuration
```

#### 4. Test Plugin
```bash
# Validate plugin
python cli.py validate-plugins

# Test specific plugin
python -c "from plugins.tts_my_engine import run; run('test')"
```

## 🧪 Testing & Quality Assurance

### 🔍 **Global System Testing**
```bash
# Run comprehensive system test
python test/test_global.py

# Quick health check
python cli.py health

# Validate all plugins
python cli.py validate-plugins
```

### 🎯 **Component Testing**
```bash
# Test individual components
pytest test/test_voice_assistant.py -v
pytest test/test_whisper.py -v

# Test specific functionality
python -c "from helper.numberToText import convert; print(convert('123'))"
python -c "from utils.system_monitor import SystemMonitor; print('Monitor OK')"
```

### 📊 **System Monitoring**
```bash
# Real-time system monitoring
python -c "
from utils.system_monitor import SystemMonitor
import time
monitor = SystemMonitor()
monitor.start_monitoring()
time.sleep(10)
print(monitor.get_summary())
monitor.stop_monitoring()
"

# Performance testing
python utils/performance_monitor.py
```

### ✅ **Test Examples**
```python
def test_number_to_text():
    from helper.numberToText import convert
    assert convert("12") == "dua belas"
    assert convert("100") == "seratus"

def test_command_processing():
    from command import CommandProcessor
    processor = CommandProcessor()
    result = processor.process_text("Jam berapa sekarang?")
    assert result['command_type'] == 'time'

def test_tts_plugin():
    from plugins.tts_mms_tts import run
    result = run("Halo dunia")
    assert result is not None
```

## 📈 **Performance & Monitoring**

### 🖥️ **System Requirements**
- **CPU Usage**: < 50% during normal operation
- **Memory Usage**: 500MB - 2GB depending on models loaded
- **Disk Space**: 1-5GB for models and cache
- **Network**: Optional (for online features)

### 📊 **Built-in Monitoring**
- ✅ Real-time CPU, memory, disk monitoring
- ✅ Audio device latency monitoring
- ✅ Plugin performance tracking
- ✅ Error rate monitoring
- ✅ Health score calculation

### 🚨 **Alert Thresholds**
- **CPU**: > 80% usage
- **Memory**: > 85% usage
- **Disk**: > 90% usage
- **Audio Latency**: > 100ms

## �️ Development & Contribution

### 🚀 **Getting Started with Development**
```bash
# Clone and setup development environment
git clone <repository-url>
cd facebook-seacker
python setup_assistant.py --dev

# Install development dependencies
pip install -r requirements.txt
pip install pytest pre-commit black isort

# Setup pre-commit hooks
pre-commit install
```

### 🔧 **Development Tools**

#### **CLI Development Helper**
```bash
# Quick development commands
python cli.py health          # System health
python cli.py test-tts        # Test TTS
python cli.py test-stt        # Test STT  
python cli.py devices         # Audio devices
python cli.py validate-plugins # Validate plugins
```

#### **Code Quality Tools**
```bash
# Format code
black .
isort .

# Run linting
flake8 .

# Type checking (if mypy installed)
mypy app.py
```

### 📝 **Adding New Features**

#### **1. New TTS Engine**
```bash
# Create plugin file
touch plugins/tts_my_engine.py

# Implement required interface:
# - run(text, lang, output_file)
# - get_voices()
# - get_info()
# - validate()
```

#### **2. New Command Type**
```python
# In command.py, add to command_patterns:
'my_command': [
    r'my pattern',
    r'another pattern'
]

# Add handler method:
def _handle_my_command(self, text: str) -> Dict[str, Any]:
    return {
        'success': True,
        'response': 'My response',
        'command_type': 'my_command'
    }
```

#### **3. New Utility Module**
```bash
# Create in utils/
touch utils/my_utility.py

# Follow existing patterns for logging and configuration
```

### 📋 **Code Style Guidelines**
- **Python**: Follow PEP 8
- **Docstrings**: Use Google style docstrings
- **Type Hints**: Add type hints for all functions
- **Error Handling**: Use try-except with proper logging
- **Configuration**: Use config.yml for settings
- **Testing**: Write tests for new functionality

### 🔍 **Debugging Tips**
```bash
# Enable debug mode
export DEBUG_MODE=true
python app.py

# Check logs
tail -f logs/voice_assistant.log

# Test individual components
python -c "from utils.health_check import HealthChecker; h=HealthChecker(); print(h.run_all_checks())"
```

## 🤝 Contributing

### 📋 **Contribution Process**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes following code style guidelines
4. **Add** tests for new functionality
5. **Run** the test suite (`python test/test_global.py`)
6. **Commit** your changes (`git commit -m 'Add amazing feature'`)
7. **Push** to the branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request

### ✅ **Before Submitting**
- [ ] All tests pass (`python test/test_global.py`)
- [ ] Code follows style guidelines (`black .` and `isort .`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No breaking changes (or clearly documented)

### 🎯 **Areas for Contribution**
- 🗣️ New TTS engines (Bark, VALL-E, etc.)
- 👂 New STT engines (Vosk, Azure Speech, etc.)
- 🌍 Additional language support
- 📱 Mobile app interface
- 🤖 AI assistant integration (GPT, Claude, etc.)
- 🔊 Advanced audio processing
- 📊 Enhanced monitoring and analytics
- 🔐 Security improvements

## � Documentation & Resources

### 🔗 **External Resources**
- [Facebook MMS TTS](https://huggingface.co/facebook/mms-tts-ind) - Main TTS engine
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) - STT engine
- [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) - Wake word detection
- [PyAudio Documentation](https://pypi.org/project/PyAudio/) - Audio processing
- [Flask Documentation](https://flask.palletsprojects.com/) - Web interface framework

### � **Internal Documentation**
- `frontend/README.md` - Web interface documentation
- `.github/copilot-instructions.md` - AI assistant guidelines
- `config/` - Configuration management docs
- `plugins/` - Plugin development examples

### 🆘 **Troubleshooting**

#### **Common Issues**

**Audio Issues:**
```bash
# No microphone detected
python cli.py devices

# Audio quality issues
# Check sample rates in config.yml
# Ensure microphone permissions are granted
```

**Plugin Issues:**
```bash
# Plugin validation failed
python cli.py validate-plugins

# Missing dependencies
pip install -r requirements.txt
```

**Performance Issues:**
```bash
# High CPU/Memory usage
python -c "from utils.system_monitor import SystemMonitor; print(SystemMonitor().get_summary())"

# Enable monitoring
python utils/system_monitor.py
```

#### **FAQ**

**Q: Can I run this completely offline?**
A: Yes! Set `OFFLINE_MODE=true` in `.env`. Only MMS TTS and Whisper.cpp will be used.

**Q: How do I add my own TTS voice?**
A: Create a new plugin in `plugins/tts_*.py` following the existing examples.

**Q: Can I use this on Raspberry Pi?**
A: Yes! This was designed for Raspberry Pi. Ensure you have enough RAM (2GB+).

**Q: How do I change the wake word?**
A: Edit `wake_word.keywords` in `config.yml` or use the web interface.

## 🔒 Privacy & Security

### 🛡️ **Privacy Features**
- ✅ **Offline Operation**: Complete functionality without internet
- ✅ **Local Processing**: All voice data processed locally
- ✅ **No Data Collection**: No telemetry or usage tracking
- ✅ **Configurable Privacy**: Choose which services to use

### 🔐 **Security Considerations**
- 🔑 API keys stored in `.env` (not in version control)
- 🌐 Web interface can be secured with authentication
- 📁 File permissions properly configured
- 🚫 No external data transmission in offline mode

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 📋 **License Summary**
- ✅ Commercial use allowed
- ✅ Modification allowed  
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability assumed

## 📞 Support & Community

### 🆘 **Getting Help**
1. **Documentation**: Check this README and internal docs
2. **Issues**: Open a GitHub issue for bugs or feature requests
3. **Discussions**: Use GitHub Discussions for questions
4. **Health Check**: Run `python cli.py health` for diagnostics

### 🎯 **Report Issues**
When reporting issues, please include:
- Operating system and Python version
- Full error message and traceback
- Steps to reproduce the issue
- Output of `python cli.py health`

### 🌟 **Show Your Support**
- ⭐ Star this repository
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🤝 Contribute code or documentation
- 📢 Share with others who might find it useful

---

## 🎉 **Quick Start Summary**

```bash
# 1. Clone and setup
git clone <repository-url>
cd facebook-seacker
python setup_assistant.py

# 2. Test the system
python test/test_global.py

# 3. Start voice assistant
python app.py

# 4. Open web interface (optional)
cd frontend && python app.py
# Browse to: http://localhost:5000
```

**🎤 Ready to use Lepida Voice Assistant! 🇮🇩**

---

*Made with ❤️ for the Indonesian AI community*
