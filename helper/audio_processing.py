"""
Audio Processing utility module
Handles audio input/output, recording, and playback
"""

import logging
import threading
import queue
import time
import numpy as np
from pathlib import Path

# Optional imports
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    
try:
    import wave
    WAVE_AVAILABLE = True
except ImportError:
    WAVE_AVAILABLE = False

class AudioProcessor:
    """Audio processing utility for microphone input and speaker output."""
    
    def __init__(self, config):
        """Initialize audio processor with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Check dependencies
        if not PYAUDIO_AVAILABLE:
            self.logger.error("PyAudio not available. Audio processing will be limited.")
            self.audio = None
            return
            
        # Audio configuration
        self.input_device = config.get('audio.input.device_index')
        self.output_device = config.get('audio.output.device_index')
        self.sample_rate = config.get('audio.input.sample_rate', 16000)
        self.channels = config.get('audio.input.channels', 1)
        self.chunk_size = config.get('audio.input.chunk_size', 1024)
        self.format = pyaudio.paInt16
        
        # Recording state
        self.recording = False
        self.audio_queue = queue.Queue()
        
        # Initialize PyAudio
        try:
            self.audio = pyaudio.PyAudio()
            
            # Find default devices if not specified
            if self.input_device is None:
                self.input_device = self._get_default_input_device()
            if self.output_device is None:
                self.output_device = self._get_default_output_device()
                
            self.logger.info(f"Audio processor initialized - Input: {self.input_device}, Output: {self.output_device}")
        except Exception as e:
            self.logger.error(f"Failed to initialize PyAudio: {e}")
            self.audio = None
    
    def _get_default_input_device(self):
        """Get default input (microphone) device."""
        if not self.audio:
            return None
            
        try:
            device_info = self.audio.get_default_input_device_info()
            return device_info['index']
        except Exception as e:
            self.logger.warning(f"Could not get default input device: {e}")
            return None
    
    def _get_default_output_device(self):
        """Get default output (speaker) device."""
        if not self.audio:
            return None
            
        try:
            device_info = self.audio.get_default_output_device_info()
            return device_info['index']
        except Exception as e:
            self.logger.warning(f"Could not get default output device: {e}")
            return None
    
    def list_audio_devices(self):
        """List all available audio devices."""
        devices = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            devices.append({
                'index': i,
                'name': device_info['name'],
                'channels': device_info['maxInputChannels'],
                'sample_rate': device_info['defaultSampleRate']
            })
        return devices
    
    def record_audio(self, duration=5, output_file=None):
        """
        Record audio from microphone.
        
        Args:
            duration (int): Recording duration in seconds
            output_file (str): Optional file path to save recording
            
        Returns:
            numpy.ndarray: Audio data or None if failed
        """
        try:
            # Open microphone stream
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.input_device,
                frames_per_buffer=self.chunk_size
            )
            
            self.logger.info(f"Recording for {duration} seconds...")
            
            frames = []
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Convert to numpy array
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            
            # Save to file if requested
            if output_file:
                self.save_audio(audio_data, output_file)
            
            self.logger.info("Recording completed")
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Failed to record audio: {e}")
            return None
    
    def play_audio_file(self, file_path):
        """
        Play audio file through speakers.
        
        Args:
            file_path (str): Path to audio file
        """
        try:
            # Read audio file
            with wave.open(file_path, 'rb') as wf:
                # Open output stream
                stream = self.audio.open(
                    format=self.audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=self.output_device
                )
                
                # Play audio in chunks
                chunk_size = 1024
                data = wf.readframes(chunk_size)
                while data:
                    stream.write(data)
                    data = wf.readframes(chunk_size)
                
                stream.stop_stream()
                stream.close()
                
            self.logger.info(f"Played audio file: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to play audio file {file_path}: {e}")
    
    def play_audio_data(self, audio_data, sample_rate=None):
        """
        Play audio data through speakers.
        
        Args:
            audio_data (numpy.ndarray): Audio data
            sample_rate (int): Sample rate of audio data
        """
        try:
            if sample_rate is None:
                sample_rate = self.sample_rate
            
            # Open output stream
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=sample_rate,
                output=True,
                output_device_index=self.output_device
            )
            
            # Convert numpy array to bytes
            audio_bytes = audio_data.tobytes()
            
            # Play audio
            stream.write(audio_bytes)
            stream.stop_stream()
            stream.close()
            
            self.logger.info("Played audio data")
            
        except Exception as e:
            self.logger.error(f"Failed to play audio data: {e}")
    
    def save_audio(self, audio_data, file_path, sample_rate=None):
        """
        Save audio data to file.
        
        Args:
            audio_data (numpy.ndarray): Audio data
            file_path (str): Output file path
            sample_rate (int): Sample rate of audio data
        """
        try:
            if sample_rate is None:
                sample_rate = self.sample_rate
            
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save as WAV file
            with wave.open(file_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())
            
            self.logger.info(f"Saved audio to: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save audio to {file_path}: {e}")
    
    def close(self):
        """Close audio processor and cleanup resources."""
        self.audio.terminate()
        self.logger.info("Audio processor closed")
