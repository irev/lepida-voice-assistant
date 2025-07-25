#!/bin/bash
# ====================================================================
# 🍓 Raspberry Pi Audio Setup Script for Lepida Voice Assistant
# ====================================================================

echo "🍓 Raspberry Pi Audio Setup for Lepida Voice Assistant"
echo "======================================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Warning: This script is designed for Raspberry Pi"
    echo "   Continuing anyway..."
fi

echo "📋 Step 1: Updating system packages..."
sudo apt update

echo ""
echo "🔊 Step 2: Installing audio system packages..."

# Install ALSA (Advanced Linux Sound Architecture)
sudo apt install -y alsa-utils alsa-base

# Install PulseAudio (alternative audio system)
sudo apt install -y pulseaudio pulseaudio-utils

# Install additional audio tools
sudo apt install -y sox libsox-fmt-all

# Install Python audio dependencies
echo ""
echo "🐍 Step 3: Installing Python audio packages..."

# Install PyAudio dependencies
sudo apt install -y python3-pyaudio portaudio19-dev

# Install additional audio libraries
sudo apt install -y python3-pygame
sudo apt install -y python3-numpy python3-scipy

# Install pip packages
pip3 install soundfile
pip3 install playsound
pip3 install pygame

echo ""
echo "⚙️  Step 4: Configuring audio settings..."

# Enable audio
sudo modprobe snd_bcm2835

# Set audio output to headphone jack (not HDMI)
sudo amixer cset numid=3 1

# Set volume to reasonable level
sudo amixer set PCM -- 80%

echo ""
echo "🎤 Step 5: Testing audio setup..."

# Test speaker output
echo "Testing speaker output..."
speaker-test -t wav -c 2 -l 1 2>/dev/null || echo "Speaker test failed (normal if no speakers connected)"

# Test ALSA
echo "Testing ALSA..."
aplay --version >/dev/null 2>&1 && echo "✅ ALSA working" || echo "❌ ALSA not working"

# Test PulseAudio
echo "Testing PulseAudio..."
pactl info >/dev/null 2>&1 && echo "✅ PulseAudio working" || echo "❌ PulseAudio not working"

# Test Python audio
echo "Testing Python audio imports..."
python3 -c "import pyaudio; print('✅ PyAudio available')" 2>/dev/null || echo "❌ PyAudio not available"
python3 -c "import pygame; print('✅ Pygame available')" 2>/dev/null || echo "❌ Pygame not available"
python3 -c "import soundfile; print('✅ Soundfile available')" 2>/dev/null || echo "❌ Soundfile not available"

echo ""
echo "🔍 Step 6: Audio device information..."

echo "Available audio devices:"
aplay -l 2>/dev/null || echo "No playback devices found"

echo ""
echo "Audio mixer controls:"
amixer scontrols 2>/dev/null || echo "No mixer controls found"

echo ""
echo "📝 Step 7: Creating Raspberry Pi audio configuration..."

# Create audio configuration file
cat > raspberry_pi_audio_config.txt << 'EOF'
# Raspberry Pi Audio Configuration for Lepida Voice Assistant

## Audio Output Commands:
# Set output to headphone jack: sudo amixer cset numid=3 1
# Set output to HDMI: sudo amixer cset numid=3 2
# Set volume: sudo amixer set PCM -- 80%

## Test Commands:
# Test speaker: speaker-test -t wav -c 2 -l 1
# Test aplay: aplay /usr/share/sounds/alsa/Front_Left.wav
# Test paplay: paplay /usr/share/sounds/alsa/Front_Left.wav

## Troubleshooting:
# Check audio devices: aplay -l
# Check mixer: amixer scontrols
# Check PulseAudio: pactl info

## Environment Variables for .env:
AUDIO_OUTPUT_DEVICE=auto
AUDIO_INPUT_DEVICE=auto
MOCK_AUDIO_DEVICES=False
EOF

echo ""
echo "🎉 Raspberry Pi audio setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. Test voice assistant: python app.py"
echo "3. Check configuration: cat raspberry_pi_audio_config.txt"
echo ""
echo "🔧 If audio still doesn't work:"
echo "1. Check connections (speakers/headphones)"
echo "2. Try different audio output: sudo amixer cset numid=3 1"
echo "3. Adjust volume: sudo amixer set PCM -- 90%"
echo "4. Check device permissions: sudo usermod -a -G audio $USER"
echo ""
