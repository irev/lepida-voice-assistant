"""
Audio Transcription utility module
Handles speech-to-text conversion with plugin support
"""

import importlib
import logging

class AudioTranscription:
    """Speech-to-Text wrapper with plugin support."""
    
    def __init__(self, config):
        """Initialize STT with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get STT configuration
        self.primary_engine = config.get('stt.primary_engine', 'whisper_cpp')
        self.fallback_engines = config.get('stt.fallback_engines', [])
        self.language = config.get('stt.language', 'id')
        
        # Load primary STT engine
        self.stt_engine = self._load_stt_engine(self.primary_engine)
        
        if not self.stt_engine:
            self.logger.error("Failed to load any STT engine")
            raise Exception("No STT engine could be loaded")
    
    def _load_stt_engine(self, engine_name):
        """Load an STT engine plugin."""
        try:
            # Try to import the plugin
            plugin_module = importlib.import_module(f'plugins.stt_{engine_name}')
            self.logger.info(f"Loaded STT engine: {engine_name}")
            return plugin_module
        except ImportError as e:
            self.logger.warning(f"Failed to load STT engine {engine_name}: {e}")
            
            # Try fallback engines
            for fallback in self.fallback_engines:
                if fallback != engine_name:
                    try:
                        plugin_module = importlib.import_module(f'plugins.stt_{fallback}')
                        self.logger.info(f"Loaded fallback STT engine: {fallback}")
                        return plugin_module
                    except ImportError:
                        self.logger.warning(f"Failed to load fallback STT engine {fallback}")
                        continue
            
            return None
    
    def transcribe_audio(self, audio_file=None):
        """
        Transcribe audio to text.
        
        Args:
            audio_file (str): Path to audio file, or None for live microphone input
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            # Call the STT engine
            if hasattr(self.stt_engine, 'transcribe'):
                return self.stt_engine.transcribe(audio_file, self.language)
            else:
                self.logger.error("STT engine does not have 'transcribe' method")
                return None
                
        except Exception as e:
            self.logger.error(f"STT transcription failed: {e}")
            return None
    
    def transcribe_live(self, duration=5):
        """
        Transcribe live audio from microphone.
        
        Args:
            duration (int): Recording duration in seconds
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            if hasattr(self.stt_engine, 'transcribe_live'):
                return self.stt_engine.transcribe_live(duration, self.language)
            else:
                # Fallback to regular transcription
                return self.transcribe_audio()
                
        except Exception as e:
            self.logger.error(f"Live STT transcription failed: {e}")
            return None
    
    def get_supported_languages(self):
        """Get list of supported languages from the STT engine."""
        if hasattr(self.stt_engine, 'get_languages'):
            return self.stt_engine.get_languages()
        return []
