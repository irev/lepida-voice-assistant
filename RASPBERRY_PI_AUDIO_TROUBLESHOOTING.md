# 🍓 Raspberry Pi Audio Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: "No audio playback method available"

**Symptoms:**
- Warning messages in voice assistant logs
- No sound output during TTS or audio feedback

**Solutions:**

1. **Install missing audio packages:**
   ```bash
   sudo apt update
   sudo apt install -y alsa-utils pulseaudio python3-pygame sox
   ```

2. **Enable audio output:**
   ```bash
   # Enable audio module
   sudo modprobe snd_bcm2835
   
   # Set audio to headphone jack
   sudo amixer cset numid=3 1
   
   # Set volume
   sudo amixer set PCM -- 80%
   ```

3. **Test audio systems:**
   ```bash
   # Test ALSA
   aplay /usr/share/sounds/alsa/Front_Left.wav
   
   # Test PulseAudio
   paplay /usr/share/sounds/alsa/Front_Left.wav
   
   # Test speaker
   speaker-test -t wav -c 2 -l 1
   ```

### Issue 2: "Permission denied" audio errors

**Solution:**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Reboot to apply changes
sudo reboot
```

### Issue 3: No sound from headphone jack

**Solutions:**

1. **Force audio to headphone jack:**
   ```bash
   sudo amixer cset numid=3 1
   ```

2. **Check audio routing:**
   ```bash
   # List available devices
   aplay -l
   
   # Check mixer settings
   amixer scontrols
   ```

3. **Edit boot config:**
   ```bash
   sudo nano /boot/config.txt
   # Add line: dtparam=audio=on
   sudo reboot
   ```

### Issue 4: Audio choppy or distorted

**Solutions:**

1. **Increase audio buffer:**
   ```bash
   # Edit PulseAudio config
   sudo nano /etc/pulse/daemon.conf
   # Uncomment and set: default-sample-rate = 44100
   ```

2. **Adjust GPU memory split:**
   ```bash
   sudo raspi-config
   # Advanced Options → Memory Split → Set to 64
   ```

### Issue 5: PyAudio import errors

**Solution:**
```bash
# Install PyAudio dependencies
sudo apt install -y python3-pyaudio portaudio19-dev

# Reinstall PyAudio
pip3 uninstall pyaudio
pip3 install pyaudio
```

## Audio Backend Priority

The voice assistant tries audio backends in this order:

1. **pygame** (recommended for Pi)
2. **playsound** (cross-platform)
3. **aplay** (ALSA command-line)
4. **paplay** (PulseAudio command-line)
5. **sox play** (SoX command-line)
6. **omxplayer** (Pi-specific media player)

## Environment Configuration

Add to your `.env` file:

```bash
# Raspberry Pi specific settings
AUDIO_OUTPUT_DEVICE=auto
AUDIO_INPUT_DEVICE=auto
MOCK_AUDIO_DEVICES=False

# TTS settings for Pi
TTS_ENGINE=mms_tts
TTS_SAMPLE_RATE=22050
TTS_VOLUME=0.8

# STT settings for Pi
STT_ENGINE=whisper_cpp
STT_MODEL_SIZE=base
STT_DEVICE=cpu
```

## Quick Diagnostic Commands

```bash
# Check Raspberry Pi model
cat /proc/cpuinfo | grep Model

# Check audio devices
aplay -l

# Check audio modules
lsmod | grep snd

# Check PulseAudio status
systemctl --user status pulseaudio

# Test Python audio
python3 -c "
import subprocess
import sys

try:
    import pygame
    print('✅ pygame available')
except ImportError:
    print('❌ pygame not available')

try:
    import pyaudio
    print('✅ pyaudio available')
except ImportError:
    print('❌ pyaudio not available')

# Test command line tools
for cmd in ['aplay', 'paplay', 'sox']:
    result = subprocess.run(['which', cmd], capture_output=True)
    if result.returncode == 0:
        print(f'✅ {cmd} available')
    else:
        print(f'❌ {cmd} not available')
"
```

## Performance Optimization

For better performance on Raspberry Pi:

1. **Use smaller TTS models:**
   ```yaml
   # In config.yml
   tts:
     engine: "mms_tts"
     model_size: "small"
   ```

2. **Reduce audio quality:**
   ```yaml
   # In config.yml
   audio:
     sample_rate: 16000
     channels: 1
   ```

3. **Enable GPU acceleration:**
   ```bash
   sudo raspi-config
   # Advanced Options → GL Driver → GL (Fake KMS)
   ```

## Getting Help

If issues persist:

1. Check system logs: `journalctl -u your-service-name`
2. Test with minimal script: `python test/test_audio_pi.py`
3. Join community forum: [Raspberry Pi Audio Community]
4. Submit issue with diagnostic output

## Automatic Setup

Run the setup script for automatic configuration:

```bash
chmod +x setup_raspberry_pi_audio.sh
./setup_raspberry_pi_audio.sh
```
