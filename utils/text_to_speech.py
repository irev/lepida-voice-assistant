"""
Text-to-Speech utility module
Handles text-to-speech conversion with plugin support
"""

import importlib
import logging
from pathlib import Path
from helper.numberToText import NumberToText
import re

class TextToSpeech:
    """Text-to-Speech wrapper with plugin support."""
    
    def __init__(self, config):
        """Initialize TTS with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get TTS configuration
        self.primary_engine = config.get('tts.primary_engine', 'mms_tts')
        self.fallback_engines = config.get('tts.fallback_engines', [])
        self.language = config.get('tts.language', 'id')
        
        # Load primary TTS engine
        self.tts_engine = self._load_tts_engine(self.primary_engine)
        
        if not self.tts_engine:
            self.logger.error("Failed to load any TTS engine")
            raise Exception("No TTS engine could be loaded")
    
    def _load_tts_engine(self, engine_name):
        """Load a TTS engine plugin."""
        try:
            # Try to import the plugin
            plugin_module = importlib.import_module(f'plugins.tts_{engine_name}')
            self.logger.info(f"Loaded TTS engine: {engine_name}")
            return plugin_module
        except ImportError as e:
            self.logger.warning(f"Failed to load TTS engine {engine_name}: {e}")
            
            # Try fallback engines
            for fallback in self.fallback_engines:
                if fallback != engine_name:
                    try:
                        plugin_module = importlib.import_module(f'plugins.tts_{fallback}')
                        self.logger.info(f"Loaded fallback TTS engine: {fallback}")
                        return plugin_module
                    except ImportError:
                        self.logger.warning(f"Failed to load fallback TTS engine {fallback}")
                        continue
            
            return None
    
    def _preprocess_text(self, text):
        """Preprocess text for better TTS pronunciation."""
        # Convert numbers to words for better pronunciation
        def number_to_words(match):
            try:
                number = int(match.group())
                return NumberToText.convert(number)
            except (ValueError, OverflowError):
                return match.group()
        
        # Find all numbers and replace with words
        processed_text = re.sub(r'\b\d{1,3}(?:[.,]\d{3})*\b|\b\d+\b', number_to_words, text)
        
        # Additional text processing can be added here
        # - Remove special characters
        # - Normalize text
        # - Handle abbreviations
        
        return processed_text
    
    def speak(self, text, lang=None, output_file=None):
        """
        Convert text to speech and play or save it.
        
        Args:
            text (str): Text to convert to speech
            lang (str): Language code (default: from config)
            output_file (str): Optional file path to save audio
        """
        if not text or not text.strip():
            self.logger.warning("Empty text provided for TTS")
            return
        
        if lang is None:
            lang = self.language
        
        # Preprocess text
        original_text = text
        processed_text = self._preprocess_text(text)
        
        if original_text != processed_text:
            self.logger.debug(f"Text preprocessing: '{original_text}' -> '{processed_text}'")
        
        try:
            # Call the TTS engine
            if hasattr(self.tts_engine, 'run'):
                self.tts_engine.run(processed_text, lang, output_file)
            else:
                self.logger.error("TTS engine does not have 'run' method")
                
        except Exception as e:
            self.logger.error(f"TTS conversion failed: {e}")
            raise
    
    def get_available_voices(self):
        """Get list of available voices from the TTS engine."""
        if hasattr(self.tts_engine, 'get_voices'):
            return self.tts_engine.get_voices()
        return []
    
    def set_voice(self, voice_id):
        """Set the voice for TTS output."""
        if hasattr(self.tts_engine, 'set_voice'):
            return self.tts_engine.set_voice(voice_id)
        return False
