"""
OpenAI Whisper STT Plugin
Offline speech-to-text using OpenAI Whisper Python package
"""

import logging
import tempfile
import os
from pathlib import Path
import numpy as np

try:
    import whisper
    import soundfile as sf
    WHISPER_AVAILABLE = True
except ImportError as e:
    WHISPER_AVAILABLE = False
    whisper = None
    sf = None
    logger = logging.getLogger(__name__)
    logger.warning(f"Whisper dependencies not available: {e}")

logger = logging.getLogger(__name__)

# Global configuration
DEFAULT_MODEL = "base"
_loaded_model = None

def _get_model():
    """Get or load the Whisper model."""
    global _loaded_model
    
    if not WHISPER_AVAILABLE:
        logger.error("Whisper package not available")
        return None
    
    if _loaded_model is None:
        try:
            logger.info(f"Loading Whisper model: {DEFAULT_MODEL}")
            _loaded_model = whisper.load_model(DEFAULT_MODEL)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            return None
    
    return _loaded_model

def transcribe(audio_file=None, language="id"):
    """
    Transcribe audio file to text using OpenAI Whisper.
    
    Args:
        audio_file (str): Path to audio file, or None for live recording
        language (str): Language code
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        if not WHISPER_AVAILABLE:
            logger.error("Whisper package not available")
            return None
            
        if audio_file is None:
            logger.error("Audio file path required for transcription")
            return None
        
        # Check if file exists
        if not Path(audio_file).exists():
            logger.error(f"Audio file not found: {audio_file}")
            return None
        
        # Get the model
        model = _get_model()
        if model is None:
            return None
        
        logger.info(f"Transcribing audio file: {audio_file}")
        
        # Transcribe with Whisper
        result = model.transcribe(
            audio_file, 
            language=language if language != "id" else "indonesian",
            task="transcribe"
        )
        
        text = result["text"].strip()
        logger.info(f"Transcription completed: {text[:50]}...")
        
        return text if text else None
        
    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}")
        return None

def transcribe_live(duration=5, language="id"):
    """
    Transcribe live audio from microphone.
    Note: This function requires audio recording capabilities
    
    Args:
        duration (int): Recording duration in seconds
        language (str): Language code
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        # Import audio processing if available
        from helper.audio_processing import AudioProcessor
        from config.config import get_config
        
        # Create temporary file
        temp_file = tempfile.mktemp(suffix='.wav')
        
        # Try to record audio
        config = get_config()
        audio_processor = AudioProcessor(config)
        success = audio_processor.record_audio(duration, temp_file)
        
        if success and Path(temp_file).exists():
            result = transcribe(temp_file, language)
            
            # Clean up temp file
            try:
                Path(temp_file).unlink()
            except:
                pass
            
            return result
        else:
            logger.error("Failed to record audio")
            return None
            
    except ImportError as e:
        logger.error(f"Audio recording not available: {e}")
        return None
    except Exception as e:
        logger.error(f"Live transcription failed: {e}")
        return None

def _record_temp_audio(duration=5):
    """
    Record temporary audio file for transcription.
    Note: This is a fallback method, prefer using transcribe_live()
    
    Args:
        duration (int): Recording duration in seconds
        
    Returns:
        str: Path to temporary audio file or None if failed
    """
    logger.warning("Direct audio recording not implemented, use transcribe_live() instead")
    return None

def get_languages():
    """Get supported languages."""
    return [
        "id", "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr", "pl",
        "ca", "nl", "ar", "sv", "it", "hi", "cs", "he", "fi", "vi", "uk", "el"
    ]

def check_availability():
    """Check if OpenAI Whisper is available."""
    return WHISPER_AVAILABLE

def get_info():
    """Get plugin information."""
    return {
        "name": "OpenAI Whisper STT",
        "description": "Offline speech-to-text using OpenAI Whisper",
        "languages": get_languages(),
        "version": "1.0.0",
        "requires": ["openai-whisper", "soundfile"],
        "available": check_availability()
    }
