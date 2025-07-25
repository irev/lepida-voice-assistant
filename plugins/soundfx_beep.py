"""
Simple Beep Sound Effects Plugin
Provides basic audio feedback sounds
"""

import logging
import time
import math
import numpy as np
import soundfile as sf
from pathlib import Path

logger = logging.getLogger(__name__)

def play_beep(frequency=800, duration=0.3, volume=0.7):
    """
    Play a simple beep sound.
    
    Args:
        frequency (int): Beep frequency in Hz
        duration (float): Duration in seconds
        volume (float): Volume (0.0 to 1.0)
    """
    try:
        # Generate beep tone
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(frequency * 2 * np.pi * t) * volume
        
        # Apply fade in/out to avoid clicks
        fade_samples = int(sample_rate * 0.01)  # 10ms fade
        if len(wave) > 2 * fade_samples:
            wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
            wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        # Save to temporary file and play
        temp_file = "temp/beep.wav"
        Path(temp_file).parent.mkdir(parents=True, exist_ok=True)
        sf.write(temp_file, wave, sample_rate)
        
        # Try to play the sound
        _play_audio_file(temp_file)
        
    except Exception as e:
        logger.error(f"Failed to play beep: {e}")

def play_success():
    """Play success sound (ascending beeps)."""
    try:
        frequencies = [600, 800, 1000]
        for freq in frequencies:
            play_beep(freq, 0.15, 0.5)
            time.sleep(0.05)
    except Exception as e:
        logger.error(f"Failed to play success sound: {e}")

def play_error():
    """Play error sound (descending beeps)."""
    try:
        frequencies = [1000, 800, 600]
        for freq in frequencies:
            play_beep(freq, 0.2, 0.6)
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Failed to play error sound: {e}")

def play_notification():
    """Play notification sound (double beep)."""
    try:
        play_beep(800, 0.2, 0.5)
        time.sleep(0.1)
        play_beep(800, 0.2, 0.5)
    except Exception as e:
        logger.error(f"Failed to play notification sound: {e}")

def play_start():
    """Play start/wake sound."""
    try:
        play_beep(600, 0.3, 0.4)
    except Exception as e:
        logger.error(f"Failed to play start sound: {e}")

def play_stop():
    """Play stop/sleep sound."""
    try:
        play_beep(400, 0.5, 0.4)
    except Exception as e:
        logger.error(f"Failed to play stop sound: {e}")

def _play_audio_file(file_path):
    """Play audio file using available method."""
    try:
        # Try pygame first
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
    except ImportError:
        try:
            # Try playsound
            from playsound import playsound
            playsound(file_path)
        except ImportError:
            try:
                # Try system command (Windows)
                import subprocess
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{file_path}").PlaySync()'],
                             check=True, capture_output=True)
            except:
                logger.warning("No audio playback method available")

def get_info():
    """Get plugin information."""
    return {
        "name": "Beep SoundFX",
        "description": "Simple beep sound effects for audio feedback",
        "version": "1.0.0",
        "requires": ["numpy", "soundfile"]
    }
