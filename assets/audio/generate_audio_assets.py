#!/usr/bin/env python3
"""
Audio Asset Generator
Creates default audio files for the voice assistant
"""

import numpy as np
import soundfile as sf
import os
from pathlib import Path

def generate_beep(frequency=440, duration=0.5, sample_rate=22050):
    """Generate a simple beep tone."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    # Add fade in/out to prevent clicks
    fade_samples = int(0.01 * sample_rate)
    audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return audio

def generate_chord(frequencies, duration=1.0, sample_rate=22050):
    """Generate a chord from multiple frequencies."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)
    for freq in frequencies:
        audio += 0.2 * np.sin(2 * np.pi * freq * t)
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.7
    return audio

def create_audio_assets():
    """Create all audio assets for the voice assistant."""
    assets_dir = Path(__file__).parent
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎵 Creating audio assets...")
    
    # Basic notification beep
    audio = generate_beep(440, 0.3)
    sf.write(assets_dir / "audio.wav", audio, 22050)
    print("✅ Created audio.wav")
    
    # Start sound - ascending tone
    audio = generate_beep(523, 0.2)  # C note
    sf.write(assets_dir / "start.wav", audio, 22050)
    print("✅ Created start.wav")
    
    # Stop sound - descending tone
    audio = generate_beep(392, 0.2)  # G note
    sf.write(assets_dir / "stop.wav", audio, 22050)
    print("✅ Created stop.wav")
    
    # Error sound - low harsh beep
    audio = generate_beep(220, 0.5)
    sf.write(assets_dir / "error.wav", audio, 22050)
    print("✅ Created error.wav")
    
    # Success sound - pleasant chord
    audio = generate_chord([523, 659, 784], 0.4)  # C major chord
    sf.write(assets_dir / "success.wav", audio, 22050)
    print("✅ Created success.wav")
    
    # Notification sound - gentle beep
    audio = generate_beep(880, 0.2)
    sf.write(assets_dir / "notification.wav", audio, 22050)
    print("✅ Created notification.wav")
    
    # Welcome sound - ascending melody
    frequencies = [523, 587, 659, 698]  # C-D-E-F
    audio = np.concatenate([generate_beep(f, 0.15) for f in frequencies])
    sf.write(assets_dir / "welcome.wav", audio, 22050)
    print("✅ Created welcome.wav")
    
    # Goodbye sound - descending melody
    frequencies = [698, 659, 587, 523]  # F-E-D-C
    audio = np.concatenate([generate_beep(f, 0.15) for f in frequencies])
    sf.write(assets_dir / "goodbye.wav", audio, 22050)
    print("✅ Created goodbye.wav")
    
    print("🎉 All audio assets created successfully!")

if __name__ == "__main__":
    create_audio_assets()
