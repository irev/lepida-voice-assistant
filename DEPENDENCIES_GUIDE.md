# 📦 Dependencies Installation Guide

## ✅ Current Status - Working Dependencies

Based on the successful dependency checks, these packages are confirmed working:

### ✅ **Core Dependencies (Verified)**
- ✅ `numpy` - Numerical computing and audio processing
- ✅ `soundfile` - Audio file reading/writing  
- ✅ `yaml` - Configuration file parsing
- ✅ `pathlib` - Enhanced path handling

### ✅ **Optional Features (Verified)**
- ✅ `pyaudio` - Audio input/output
- ✅ `whisper` - Speech recognition  
- ✅ `torch` - AI models
- ✅ `psutil` - System monitoring
- ✅ `requests` - Online services

---

## 🚀 Installation Options

### 1. **Quick Install (Recommended)**
```bash
# Install verified working dependencies
pip install -r requirements-minimal.txt
```

### 2. **Full Install (All Features)**
```bash  
# Install all dependencies
pip install -r requirements.txt
```

### 3. **Development Install**
```bash
# Install with development tools
pip install -r requirements-dev.txt
```

### 4. **Production Install**
```bash
# Install optimized for production
pip install -r requirements-prod.txt
```

---

## 📋 Requirements Files

### **requirements.txt** (Main)
- **Purpose**: Complete installation with all features
- **Contains**: Core + optional + commented alternatives
- **Usage**: Full development setup

### **requirements-minimal.txt** (Recommended)
- **Purpose**: Only verified working dependencies
- **Contains**: Core features that are confirmed working
- **Usage**: Quick setup, guaranteed to work

### **requirements-dev.txt** (Development)
- **Purpose**: Development tools and testing
- **Contains**: All dependencies + dev tools
- **Usage**: Development environment

### **requirements-prod.txt** (Production)
- **Purpose**: Production deployment
- **Contains**: Optimized for server deployment
- **Usage**: Production environments

---

## 🔧 Platform-Specific Installation

### **Windows**
```bash
# Use conda for audio packages (recommended)
conda install pyaudio
pip install -r requirements-minimal.txt

# Or use pre-compiled wheels
pip install pipwin
pipwin install pyaudio
pip install -r requirements-minimal.txt
```

### **Linux (Ubuntu/Debian)**
```bash
# Install system audio dependencies
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev

# Install Python packages
pip install -r requirements-minimal.txt
```

### **macOS**
```bash
# Install audio system dependencies
brew install portaudio

# Install Python packages
pip install -r requirements-minimal.txt
```

---

## 🎯 Component-Specific Installation

### **Basic Voice Assistant (Offline)**
```bash
pip install numpy soundfile PyYAML python-dotenv torch transformers whisper pyaudio flask psutil requests
```

### **Web Interface Only**
```bash
pip install flask requests PyYAML python-dotenv psutil
```

### **Audio Processing Only**  
```bash
pip install numpy soundfile pyaudio wave pygame
```

### **AI Models Only**
```bash
pip install torch transformers whisper numpy
```

---

## 🆘 Troubleshooting Installation

### **Common Issues & Solutions**

#### 1. **PyAudio Installation Fails**
```bash
# Windows - Use conda
conda install pyaudio

# Windows - Use pipwin  
pip install pipwin && pipwin install pyaudio

# Linux - Install system packages
sudo apt-get install python3-pyaudio portaudio19-dev

# macOS - Install portaudio
brew install portaudio
```

#### 2. **Torch Installation Issues**
```bash
# Use CPU-only version (smaller, faster install)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Or use conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

#### 3. **Whisper Installation Issues**
```bash
# Install specific version
pip install openai-whisper==20231117

# Or use minimal whisper
pip install whisper-cpp-python
```

#### 4. **Permission Issues**
```bash
# Use user install
pip install --user -r requirements-minimal.txt

# Or use virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements-minimal.txt
```

#### 5. **Network/Proxy Issues**
```bash
# Install with trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements-minimal.txt

# Use alternative index
pip install -i https://pypi.python.org/simple/ -r requirements-minimal.txt
```

---

## 📊 Installation Verification

### **Test Core Dependencies**
```bash
python -c "import numpy, soundfile, yaml; print('Core dependencies OK')"
```

### **Test Audio System**
```bash
python -c "import pyaudio; print('Audio system OK')"
```

### **Test AI Models**
```bash
python -c "import torch, transformers, whisper; print('AI models OK')"
```

### **Test Web Interface**
```bash
python -c "import flask, requests; print('Web interface OK')"
```

### **Complete System Test**
```bash
# Run health check
python cli.py health

# Or test setup
python setup_assistant.py --quick
```

---

## 🎛️ Optional Dependencies Guide

### **When to Install Optional Dependencies**

#### **TTS Engines**
```bash
# For better voice quality
pip install TTS>=0.22.0              # Coqui TTS (large)
pip install piper-tts>=1.2.0         # Piper TTS (fast)
pip install gtts>=2.3.0              # Google TTS (online)
```

#### **STT Engines**  
```bash
# For better accuracy
pip install faster-whisper>=0.9.0    # Faster whisper
pip install vosk>=0.3.45             # Offline STT
pip install speechrecognition>=3.10.0 # Multiple backends
```

#### **Wake Word Detection**
```bash
# For wake word detection
pip install pvporcupine>=3.0.0       # Porcupine (recommended)
pip install snowboy>=1.3.0           # Snowboy (alternative)
```

#### **Cloud Services**
```bash
# For online features
pip install google-cloud-speech>=2.16.0      # Google STT
pip install google-cloud-texttospeech>=2.12.0 # Google TTS
pip install openai>=1.0.0                    # OpenAI API
```

---

## ✅ Final Installation Command

For the best experience with verified working dependencies:

```bash
# Recommended installation
pip install -r requirements-minimal.txt

# Verify installation
python cli.py health
```

This will install only the dependencies that have been **verified to work** in your system! 🎉
