# 🍓 Raspberry Pi Audio Setup - Complete Guide

## Overview

This guide provides a complete solution for audio playback issues on Raspberry Pi with the Lepida Voice Assistant.

## Files Created/Updated

### 1. Updated Audio Plugin
- **File**: `plugins/soundfx_beep.py`
- **Changes**: Added multi-backend audio support for Raspberry Pi
- **Backends**: pygame, playsound, ALSA, PulseAudio, SoX, OMXPlayer

### 2. Setup Script
- **File**: `setup_raspberry_pi_audio.sh`
- **Purpose**: Automated Raspberry Pi audio configuration
- **Features**: Installs packages, configures audio, tests setup

### 3. Troubleshooting Guide
- **File**: `RASPBERRY_PI_AUDIO_TROUBLESHOOTING.md`
- **Purpose**: Comprehensive troubleshooting for audio issues
- **Includes**: Common problems, solutions, diagnostics

### 4. Test Script
- **File**: `test/test_audio_pi.py`
- **Purpose**: Verify audio setup and test all backends
- **Features**: System info, dependency check, audio testing

## Quick Setup (Raspberry Pi)

1. **Run setup script:**
   ```bash
   chmod +x setup_raspberry_pi_audio.sh
   ./setup_raspberry_pi_audio.sh
   ```

2. **Reboot:**
   ```bash
   sudo reboot
   ```

3. **Test audio:**
   ```bash
   python test/test_audio_pi.py
   ```

4. **Run voice assistant:**
   ```bash
   python app.py
   ```

## Audio Backend Priority

The system tries these audio methods in order:

1. **pygame** (recommended for Pi) - Python audio library with good Pi support
2. **playsound** - Cross-platform Python audio
3. **aplay** - ALSA command-line player
4. **paplay** - PulseAudio command-line player
5. **sox play** - SoX audio processing
6. **omxplayer** - Raspberry Pi specific media player

## Environment Configuration

Add these settings to your `.env` file for optimal Pi performance:

```bash
# Audio settings
AUDIO_OUTPUT_DEVICE=auto
AUDIO_INPUT_DEVICE=auto
MOCK_AUDIO_DEVICES=False

# TTS optimization for Pi
TTS_ENGINE=mms_tts
TTS_SAMPLE_RATE=22050
TTS_VOLUME=0.8

# STT optimization for Pi
STT_ENGINE=whisper_cpp
STT_MODEL_SIZE=base
STT_DEVICE=cpu
```

## Common Issues Fixed

### Issue: "No audio playback method available"
- **Solution**: Multi-backend support with automatic fallback
- **Backends**: 6 different audio methods ensure compatibility

### Issue: Permission denied
- **Solution**: Setup script adds user to audio group
- **Command**: `sudo usermod -a -G audio $USER`

### Issue: No sound from headphone jack
- **Solution**: Force audio to headphone jack
- **Command**: `sudo amixer cset numid=3 1`

### Issue: Import errors in development
- **Solution**: Audio imports wrapped in try/except blocks
- **Note**: Lint errors are expected in dev environment

## Manual Troubleshooting

If automatic setup fails, try these commands:

```bash
# Install audio packages
sudo apt install -y alsa-utils pulseaudio python3-pygame sox

# Configure audio output
sudo amixer cset numid=3 1  # Headphone jack
sudo amixer set PCM -- 80%  # Set volume

# Test audio
aplay /usr/share/sounds/alsa/Front_Left.wav
```

## Verification

After setup, verify everything works:

1. **System test:**
   ```bash
   python test/test_audio_pi.py
   ```

2. **Plugin test:**
   ```python
   from plugins.soundfx_beep import run
   run('start')  # Should play start sound
   ```

3. **Voice assistant test:**
   ```bash
   python app.py  # Should work without audio warnings
   ```

## Support

For additional help:
- Check `RASPBERRY_PI_AUDIO_TROUBLESHOOTING.md`
- Run diagnostic: `python test/test_audio_pi.py`
- Review logs for specific error messages

## Success Indicators

✅ No "No audio playback method available" warnings  
✅ Audio plays during TTS and sound effects  
✅ Multiple audio backends available as fallbacks  
✅ Compatible with all Raspberry Pi models  
✅ Works with both ALSA and PulseAudio  

The Raspberry Pi audio issues should now be resolved with comprehensive multi-backend support and automatic fallback mechanisms.
