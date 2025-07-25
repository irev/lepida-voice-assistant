#!/usr/bin/env python3
"""
Audio Asset Generator
Creates default audio files for the voice assistant
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import numpy as np
    import soundfile as sf
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("💡 SOLUTION: Install dependencies with:")
    print("   pip install numpy soundfile")
    print("   or run: pip install -r requirements.txt")
    print()
    DEPENDENCIES_AVAILABLE = False
    # Set dummy values to prevent further import errors
    np = None
    sf = None

def check_dependencies():
    """Check if required dependencies are available."""
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Cannot generate audio assets - missing dependencies")
        print("📋 Required packages:")
        print("   - numpy (for audio signal generation)")
        print("   - soundfile (for audio file writing)")
        print()
        print("🔧 Installation options:")
        print("   1. pip install numpy soundfile")
        print("   2. pip install -r requirements.txt")
        print("   3. Activate virtual environment first if using one")
        print()
        return False
    return True

def generate_beep(frequency=440, duration=0.5, sample_rate=22050):
    """Generate a simple beep tone."""
    if not DEPENDENCIES_AVAILABLE:
        return None
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    # Add fade in/out to prevent clicks
    fade_samples = int(0.01 * sample_rate)
    audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return audio

def generate_chord(frequencies, duration=1.0, sample_rate=22050):
    """Generate a chord from multiple frequencies."""
    if not DEPENDENCIES_AVAILABLE:
        return None
        
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)
    for freq in frequencies:
        audio += 0.2 * np.sin(2 * np.pi * freq * t)
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.7
    return audio

def create_audio_assets():
    """Create all audio assets for the voice assistant."""
    if not check_dependencies():
        return False
    
    assets_dir = Path(__file__).parent
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎵 Creating audio assets...")
    
    try:
        # Basic notification beep
        audio = generate_beep(440, 0.3)
        if audio is not None:
            sf.write(assets_dir / "audio.wav", audio, 22050)
            print("✅ Created audio.wav")
        
        # Start sound - ascending tone
        audio = generate_beep(523, 0.2)  # C note
        if audio is not None:
            sf.write(assets_dir / "start.wav", audio, 22050)
            print("✅ Created start.wav")
        
        # Stop sound - descending tone
        audio = generate_beep(392, 0.2)  # G note
        if audio is not None:
            sf.write(assets_dir / "stop.wav", audio, 22050)
            print("✅ Created stop.wav")
        
        # Error sound - low harsh beep
        audio = generate_beep(220, 0.5)
        if audio is not None:
            sf.write(assets_dir / "error.wav", audio, 22050)
            print("✅ Created error.wav")
        
        # Success sound - pleasant chord
        audio = generate_chord([523, 659, 784], 0.4)  # C major chord
        if audio is not None:
            sf.write(assets_dir / "success.wav", audio, 22050)
            print("✅ Created success.wav")
        
        # Notification sound - gentle beep
        audio = generate_beep(880, 0.2)
        if audio is not None:
            sf.write(assets_dir / "notification.wav", audio, 22050)
            print("✅ Created notification.wav")
        
        # Welcome sound - ascending melody
        frequencies = [523, 587, 659, 698]  # C-D-E-F
        beeps = [generate_beep(f, 0.15) for f in frequencies]
        if all(beep is not None for beep in beeps):
            audio = np.concatenate(beeps)
            sf.write(assets_dir / "welcome.wav", audio, 22050)
            print("✅ Created welcome.wav")
        
        # Goodbye sound - descending melody
        frequencies = [698, 659, 587, 523]  # F-E-D-C
        beeps = [generate_beep(f, 0.15) for f in frequencies]
        if all(beep is not None for beep in beeps):
            audio = np.concatenate(beeps)
            sf.write(assets_dir / "goodbye.wav", audio, 22050)
            print("✅ Created goodbye.wav")
        
        print("🎉 All audio assets created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating audio assets: {e}")
        print("💡 SOLUTION: Check file permissions and available disk space")
        return False

def main():
    """Main function to create audio assets."""
    if not check_dependencies():
        print("⚠️  Audio assets generation skipped due to missing dependencies")
        print("🔧 Install missing packages and run again:")
        print("   python assets/audio/generate_audio_assets.py")
        return False
    
    return create_audio_assets()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
