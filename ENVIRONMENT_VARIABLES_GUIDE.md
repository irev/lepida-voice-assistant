# 🔧 Environment Variables Configuration Guide

## ✅ Files Generated

### 1. **`.env.example`** - Template File
- **Purpose**: Template with all available environment variables
- **Usage**: Reference for configuration options
- **Safety**: Safe to commit to version control
- **Contains**: Default values and examples

### 2. **`.env`** - Active Configuration
- **Purpose**: Your actual development configuration
- **Usage**: Used by the application at runtime
- **Safety**: ⚠️ **NEVER commit to version control**
- **Contains**: Your actual API keys and settings

---

## 🚀 Quick Start

### Copy Template to Active Config
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### Edit Your Configuration
```bash
# Open .env file and set your actual values
notepad .env          # Windows
nano .env             # Linux
code .env             # VS Code
```

---

## 📊 Configuration Categories

### 🎯 Application Settings
```env
APP_NAME=Lepida Voice Assistant
APP_DEBUG=True                    # Enable debug mode for development
APP_LOG_LEVEL=DEBUG              # Logging level (DEBUG, INFO, WARNING, ERROR)
RUN_AS_SERVICE=false             # Run as background service
```

### 🔊 Audio Configuration
```env
AUDIO_INPUT_DEVICE=auto          # Microphone (auto-detect or device index)
AUDIO_OUTPUT_DEVICE=auto         # Speaker (auto-detect or device index)
AUDIO_SAMPLE_RATE=16000          # Audio quality (Hz)
AUDIO_CHANNELS=1                 # Mono (1) or Stereo (2)
```

### 🗣️ Text-to-Speech (TTS)
```env
TTS_ENGINE=mms_tts               # Primary TTS engine
TTS_FALLBACK_ENGINES=coqui,piper # Backup engines
TTS_LANGUAGE=id                  # Indonesian language
```

### 🎤 Speech-to-Text (STT)
```env
STT_ENGINE=whisper_cpp           # Primary STT engine
STT_LANGUAGE=id                  # Indonesian language
WHISPER_MODEL_SIZE=base          # Model size (tiny, base, small, medium, large)
```

### 🔊 Wake Word Detection
```env
WAKE_WORD_ENGINE=porcupine       # Wake word detection engine
PORCUPINE_ACCESS_KEY=            # Your Porcupine API key
WAKE_WORDS=lepida,assistant      # Custom wake words
```

### 🔗 API Keys (Optional)
```env
GOOGLE_STT_API_KEY=              # Google Speech-to-Text API
OPENAI_API_KEY=                  # OpenAI API for advanced features
HUGGINGFACE_API_TOKEN=           # Hugging Face model downloads
WEATHER_API_KEY=                 # Weather information
NEWS_API_KEY=                    # News updates
```

### 🌐 Web Interface
```env
FLASK_HOST=0.0.0.0              # Web server host
FLASK_PORT=5000                  # Web server port
FLASK_DEBUG=True                 # Enable Flask debug mode
FLASK_SECRET_KEY=your-secret     # Web security key
```

---

## 🛠️ Environment Variable Priority

The application loads configuration in this order (later values override earlier ones):

1. **Default values** (hardcoded in application)
2. **config.yml** (YAML configuration file)
3. **Environment variables** (.env file or system environment)
4. **Command line arguments** (highest priority)

---

## 🔒 Security Best Practices

### ✅ Safe Practices
- ✅ Keep `.env` in `.gitignore`
- ✅ Use different `.env` for development/production
- ✅ Store API keys securely
- ✅ Use strong secret keys in production
- ✅ Regularly rotate API keys

### ❌ Avoid These
- ❌ Never commit `.env` to version control
- ❌ Don't share API keys in chat/email
- ❌ Don't use default secret keys in production
- ❌ Don't store passwords in plain text

---

## 🎛️ Development vs Production

### Development Settings (Current `.env`)
```env
APP_DEBUG=True
LOG_LEVEL=DEBUG
DEBUG_MODE=true
VERBOSE_LOGGING=True
ENABLE_DEV_FEATURES=True
FLASK_DEBUG=True
```

### Production Settings (Recommended)
```env
APP_DEBUG=False
LOG_LEVEL=INFO
DEBUG_MODE=false
VERBOSE_LOGGING=False
ENABLE_DEV_FEATURES=False
FLASK_DEBUG=False
FLASK_SECRET_KEY=generated-secure-key
```

---

## 🧪 Testing Configuration

### Test Environment Variables
```env
TEST_MODE=True                   # Enable test mode
TEST_AUDIO_FILE=test/audio.wav   # Test audio file
MOCK_AUDIO_DEVICES=True          # Mock audio for testing
SKIP_MODEL_VALIDATION=True       # Skip model checks
```

### Testing Commands
```bash
# Test with environment variables
python cli.py test-tts
python cli.py test-stt
python cli.py health

# Test web interface
cd frontend && python app.py
# Visit: http://localhost:5000
```

---

## 🚨 Troubleshooting

### Common Issues

#### 1. **Audio Device Issues**
```env
# Try specific device indices
AUDIO_INPUT_DEVICE_INDEX=0
AUDIO_OUTPUT_DEVICE_INDEX=1

# Or mock for testing
MOCK_AUDIO_DEVICES=True
```

#### 2. **Model Loading Issues**
```env
# Skip validation for testing
SKIP_MODEL_VALIDATION=True

# Use smaller models
WHISPER_MODEL_SIZE=tiny
TTS_ENGINE=mms_tts
```

#### 3. **API Connection Issues**
```env
# Enable offline mode
OFFLINE_MODE=true

# Increase timeouts
HTTP_TIMEOUT=60
CONNECTION_RETRY_COUNT=5
```

#### 4. **Permission Issues**
```env
# Reduce security for development
ALLOW_REMOTE_ACCESS=True
ENABLE_API_RATE_LIMITING=False
```

### Debug Commands
```bash
# Check environment loading
python -c "from config.config import get_config; print(get_config())"

# Validate environment
python cli.py health

# Check audio devices
python cli.py devices
```

---

## 📝 Usage Examples

### Basic Voice Assistant
```env
# Minimal configuration for offline voice assistant
TTS_ENGINE=mms_tts
STT_ENGINE=whisper_cpp
WAKE_WORD_ENGINE=porcupine
OFFLINE_MODE=true
```

### Web Interface Only
```env
# Web-only configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
MOCK_AUDIO_DEVICES=True
TEST_MODE=True
```

### Development with All Features
```env
# Full development setup
APP_DEBUG=True
ENABLE_DEV_FEATURES=True
VERBOSE_LOGGING=True
GOOGLE_STT_API_KEY=your-key
OPENAI_API_KEY=your-key
```

---

## 🔄 Environment Management

### Loading Environment Variables
```python
# In Python code
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
api_key = os.getenv('OPENAI_API_KEY')
```

### Runtime Configuration
```bash
# Override environment variables at runtime
LOG_LEVEL=DEBUG python app.py

# Set multiple variables
export FLASK_DEBUG=True && python frontend/app.py
```

### Environment Validation
```bash
# Check configuration
python setup_assistant.py --help

# Validate environment
python cli.py health

# Test specific components
python cli.py test-tts --engine mms_tts
```

---

## ✅ Setup Complete

Your environment files are now configured:

1. **`.env.example`** - Complete template with all options
2. **`.env`** - Your development configuration
3. **Both files** contain comprehensive settings for all features

### Next Steps:
1. **Add API Keys**: Edit `.env` and add your actual API keys
2. **Test Configuration**: Run `python cli.py health`
3. **Start Application**: Run `python app.py` or `python launcher.py`
4. **Web Interface**: Start with `cd frontend && python app.py`

🎉 **Environment configuration is complete and ready for use!**
