# Lepida Voice Assistant - Error Handling Guide

## 🚨 Common Setup Errors and Solutions

### Virtual Environment Issues

#### VENV_PERMISSION
**Error**: Permission denied while creating virtual environment
**Solution**: 
- Run as administrator (Windows) or with sudo (Linux/Mac)
- Choose a different directory with write permissions
- Check if antivirus is blocking the operation

#### VENV_TIMEOUT
**Error**: Virtual environment creation timed out
**Solution**:
- Check internet connection
- Try manual creation: `python -m venv .venv`
- Disable antivirus temporarily

#### VENV_DISK_SPACE
**Error**: Insufficient disk space for virtual environment
**Solution**:
- Free up at least 500MB of disk space
- Use `disk cleanup` tool on Windows
- Remove temporary files and downloads

### Dependencies Installation Issues

#### PIP_EXTERNALLY_MANAGED
**Error**: Python environment is externally managed
**Solution**:
- Use virtual environment: `python -m venv .venv`
- Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
- Run setup again

#### PIP_VERSION_CONFLICT
**Error**: Some packages are not available for your Python version
**Solution**:
- Update Python to 3.8+
- Check requirements.txt for compatibility
- Try installing packages individually

#### PIP_DISK_SPACE
**Error**: Insufficient disk space
**Solution**:
- Free up disk space (at least 1GB recommended)
- Clear pip cache: `pip cache purge`
- Use `--no-cache-dir` flag

#### PIP_TIMEOUT
**Error**: Package installation timed out
**Solution**:
- Check internet connection
- Try again later
- Use alternative package index: `pip install -i https://pypi.org/simple/`

### Frontend Setup Issues

#### FRONTEND_DIR_MISSING
**Error**: Frontend directory not found
**Solution**:
- Ensure you're in the correct project directory
- Check if frontend/ folder exists
- Re-download/clone the project

#### FRONTEND_REQ_MISSING
**Error**: Frontend requirements.txt not found
**Solution**:
- Check project structure
- Create frontend/requirements.txt if missing
- Verify file permissions

#### FRONTEND_APP_MISSING
**Error**: Frontend Flask app (app.py) not found
**Solution**:
- Ensure frontend/app.py exists
- Check project structure
- Re-download missing files

### Audio System Issues

#### AUDIO_DEVICE_NOT_FOUND
**Error**: No audio devices found
**Solution**:
- Install audio drivers
- Check microphone/speaker connections
- Test with other audio applications
- Voice assistant may work in text-only mode

#### PYAUDIO_INSTALL_FAILED
**Error**: PyAudio installation failed
**Solution**:
- Install system audio libraries first
- Windows: Install Microsoft Visual C++ Build Tools
- Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`
- Mac: `brew install portaudio`

### Configuration Issues

#### CONFIG_FILE_CORRUPT
**Error**: Configuration file error
**Solution**:
- Delete config.yml (will be recreated)
- Check YAML syntax
- Restore from backup

#### ENV_FILE_MISSING
**Error**: Environment file issues
**Solution**:
- Copy .env.example to .env
- Set required environment variables
- Check file permissions

## 🔧 Recovery Commands

### Quick Recovery
```bash
python setup_assistant.py --recovery
```

### Manual Recovery Steps
1. **Clean slate**: Delete .venv, logs, temp folders
2. **Fresh start**: `python setup_assistant.py`
3. **Virtual environment**: `python -m venv .venv`
4. **Activation**: `.venv\Scripts\activate`
5. **Dependencies**: `pip install -r requirements.txt`

### Platform-Specific Issues

#### Windows
- Run PowerShell as Administrator
- Enable execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Install Visual C++ Build Tools for native packages

#### Linux
- Install development packages: `sudo apt-get install python3-dev python3-venv build-essential`
- Check permissions: `chmod +x setup_assistant.py`
- Use sudo only if necessary

#### macOS
- Install Xcode Command Line Tools: `xcode-select --install`
- Use Homebrew for dependencies: `brew install python`
- Check PATH environment variable

## 📊 Error Codes Reference

| Code | Category | Description |
|------|----------|-------------|
| VENV_* | Virtual Environment | Issues with venv creation/activation |
| PIP_* | Package Installation | pip and dependency issues |
| FRONTEND_* | Web Interface | Frontend setup problems |
| AUDIO_* | Audio System | Microphone/speaker issues |
| CONFIG_* | Configuration | Settings and config file issues |

## 🆘 Getting Help

1. **Check logs**: `logs/setup_error.log`
2. **Run diagnostics**: `python cli.py health`
3. **Recovery mode**: `python setup_assistant.py --recovery`
4. **GitHub Issues**: Report bugs with error codes
5. **Documentation**: Check README.md for requirements

## 📝 Reporting Bugs

When reporting errors, include:
- Error code (e.g., VENV_PERMISSION)
- Full error message
- Operating system and Python version
- Steps to reproduce
- Contents of logs/setup_error.log
