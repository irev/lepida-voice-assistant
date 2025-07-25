"""
Audio Effects and Sound Management System
Manages sound effects, audio feedback, and audio assets
"""

import logging
import threading
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class AudioEffectsManager:
    """Manages audio effects and sound feedback."""
    
    def __init__(self, config):
        """
        Initialize audio effects manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.enabled = config.get('soundfx.enabled', True)
        self.engine = config.get('soundfx.engine', 'beep')
        self.volume = config.get('soundfx.volume', 0.7)
        
        # Audio assets directory
        self.assets_dir = Path("assets/audio")
        
        # Load sound effects engine
        self.fx_engine = None
        if self.enabled:
            self._load_engine()
        
        # Create default audio files if they don't exist
        self._ensure_audio_assets()
    
    def _load_engine(self):
        """Load sound effects engine."""
        try:
            if self.engine == 'beep':
                from plugins.soundfx_beep import (
                    play_beep, play_success, play_error, 
                    play_notification, play_start, play_stop
                )
                self.fx_engine = {
                    'beep': play_beep,
                    'success': play_success,
                    'error': play_error,
                    'notification': play_notification,
                    'start': play_start,
                    'stop': play_stop
                }
                self.logger.info("Loaded beep sound effects engine")
            else:
                self.logger.warning(f"Unknown sound effects engine: {self.engine}")
                
        except ImportError as e:
            self.logger.warning(f"Failed to load sound effects engine: {e}")
            self.enabled = False
    
    def play_sound(self, sound_type, **kwargs):
        """
        Play a sound effect.
        
        Args:
            sound_type (str): Type of sound to play
            **kwargs: Additional parameters for the sound
        """
        if not self.enabled or not self.fx_engine:
            return
        
        try:
            if sound_type in self.fx_engine:
                # Play using engine
                self.fx_engine[sound_type](**kwargs)
            else:
                # Try to play from audio assets
                self._play_audio_file(sound_type)
                
        except Exception as e:
            self.logger.error(f"Failed to play sound '{sound_type}': {e}")
    
    def _play_audio_file(self, filename):
        """Play audio file from assets directory."""
        try:
            # Try different extensions
            extensions = ['.wav', '.mp3', '.ogg']
            audio_file = None
            
            for ext in extensions:
                file_path = self.assets_dir / f"{filename}{ext}"
                if file_path.exists():
                    audio_file = file_path
                    break
            
            if not audio_file:
                self.logger.warning(f"Audio file not found: {filename}")
                return
            
            # Play the file
            self._play_file(str(audio_file))
            
        except Exception as e:
            self.logger.error(f"Failed to play audio file '{filename}': {e}")
    
    def _play_file(self, file_path):
        """Play audio file using available method."""
        try:
            # Try pygame first
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            # Wait for playback in a separate thread
            def wait_for_playback():
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            
            threading.Thread(target=wait_for_playback, daemon=True).start()
            
        except ImportError:
            try:
                # Try playsound
                from playsound import playsound
                playsound(file_path, block=False)
            except ImportError:
                try:
                    # Try system command (Windows)
                    import subprocess
                    subprocess.run([
                        'powershell', '-c', 
                        f'(New-Object Media.SoundPlayer "{file_path}").PlaySync()'
                    ], check=True, capture_output=True)
                except:
                    self.logger.warning("No audio playback method available")
    
    def _ensure_audio_assets(self):
        """Create default audio assets if they don't exist."""
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # List of audio files that should exist
        audio_files = [
            'start.wav', 'stop.wav', 'success.wav', 'error.wav',
            'notification.wav', 'welcome.wav', 'goodbye.wav', 'audio.wav'
        ]
        
        for audio_file in audio_files:
            file_path = self.assets_dir / audio_file
            if not file_path.exists():
                self._create_default_audio(file_path)
    
    def _create_default_audio(self, file_path):
        """Create a default audio file."""
        try:
            import numpy as np
            import soundfile as sf
            
            # Generate a simple tone based on filename
            duration = 0.5
            sample_rate = 22050
            
            # Determine frequency based on filename
            frequency_map = {
                'start.wav': 800,
                'stop.wav': 400,
                'success.wav': 1000,
                'error.wav': 300,
                'notification.wav': 600,
                'welcome.wav': 800,
                'goodbye.wav': 500,
                'audio.wav': 750
            }
            
            frequency = frequency_map.get(file_path.name, 600)
            
            # Generate tone
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = np.sin(frequency * 2 * np.pi * t) * 0.3
            
            # Apply fade in/out
            fade_samples = int(sample_rate * 0.05)  # 50ms fade
            if len(wave) > 2 * fade_samples:
                wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
                wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Save the file
            sf.write(str(file_path), wave, sample_rate)
            self.logger.info(f"Created default audio file: {file_path.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to create default audio file {file_path.name}: {e}")
    
    # Convenience methods for common sounds
    def play_start(self):
        """Play start/wake up sound."""
        self.play_sound('start')
    
    def play_stop(self):
        """Play stop/shutdown sound."""
        self.play_sound('stop')
    
    def play_success(self):
        """Play success sound."""
        self.play_sound('success')
    
    def play_error(self):
        """Play error sound."""
        self.play_sound('error')
    
    def play_notification(self):
        """Play notification sound."""
        self.play_sound('notification')
    
    def play_welcome(self):
        """Play welcome sound."""
        self.play_sound('welcome')
    
    def play_goodbye(self):
        """Play goodbye sound."""
        self.play_sound('goodbye')
    
    def play_beep(self, frequency=800, duration=0.3):
        """Play a simple beep."""
        self.play_sound('beep', frequency=frequency, duration=duration, volume=self.volume)
    
    def set_volume(self, volume):
        """Set audio effects volume."""
        self.volume = max(0.0, min(1.0, volume))
        self.logger.info(f"Audio effects volume set to: {self.volume}")
    
    def get_available_sounds(self):
        """Get list of available sound effects."""
        sounds = []
        
        # Add engine sounds
        if self.fx_engine:
            sounds.extend(self.fx_engine.keys())
        
        # Add asset sounds
        if self.assets_dir.exists():
            for audio_file in self.assets_dir.glob('*'):
                if audio_file.suffix.lower() in ['.wav', '.mp3', '.ogg']:
                    sounds.append(audio_file.stem)
        
        return list(set(sounds))
    
    def test_audio_system(self):
        """Test the audio system with various sounds."""
        if not self.enabled:
            self.logger.warning("Audio effects are disabled")
            return
        
        test_sounds = ['start', 'notification', 'success', 'stop']
        
        self.logger.info("Testing audio system...")
        for sound in test_sounds:
            self.logger.info(f"Playing: {sound}")
            self.play_sound(sound)
            time.sleep(1)
        
        self.logger.info("Audio system test completed")
    
    def get_status(self):
        """Get audio effects system status."""
        return {
            'enabled': self.enabled,
            'engine': self.engine,
            'volume': self.volume,
            'available_sounds': self.get_available_sounds(),
            'assets_directory': str(self.assets_dir)
        }
