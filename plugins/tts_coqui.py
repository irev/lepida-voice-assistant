"""
Coqui TTS Plugin
Advanced Text-to-Speech using Coqui TTS
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Global variables
_tts_model = None
_model_name = None

def _load_model(model_name="tts_models/multilingual/multi-dataset/xtts_v2"):
    """Load Coqui TTS model."""
    global _tts_model, _model_name
    
    try:
        from TTS.api import TTS
        
        if _tts_model is None or _model_name != model_name:
            logger.info(f"Loading Coqui TTS model: {model_name}")
            _tts_model = TTS(model_name)
            _model_name = model_name
            logger.info("Coqui TTS model loaded successfully")
        
        return _tts_model
        
    except ImportError:
        raise ImportError("TTS library not available. Install with: pip install TTS")
    except Exception as e:
        logger.error(f"Failed to load Coqui TTS model: {e}")
        raise

def run(text: str, lang: str = "id", output_file: str = None):
    """
    Convert text to speech using Coqui TTS.
    
    Args:
        text (str): Text to convert to speech
        lang (str): Language code
        output_file (str): Optional file path to save audio
    """
    try:
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return
        
        # Load model
        tts_model = _load_model()
        
        # Determine output file
        if output_file is None:
            output_file = "outputs/sound/coqui_output.wav"
        
        # Create output directory
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Converting text with Coqui TTS: '{text[:50]}...'")
        
        # Generate speech
        tts_model.tts_to_file(
            text=text,
            file_path=output_file,
            language=lang
        )
        
        logger.info(f"Audio saved to {output_file}")
        
        # Try to play the audio
        _play_audio(output_file)
        
    except Exception as e:
        logger.error(f"Coqui TTS conversion failed: {e}")
        raise

def _play_audio(file_path):
    """Play audio file."""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
            
    except ImportError:
        logger.info("pygame not available for audio playback")
    except Exception as e:
        logger.warning(f"Could not play audio: {e}")

def get_voices():
    """Get available voices."""
    try:
        tts_model = _load_model()
        if hasattr(tts_model, 'speakers'):
            return tts_model.speakers
        return []
    except:
        return []

def set_voice(voice_id):
    """Set voice (speaker)."""
    # Voice setting would be handled in the run function
    return True

def get_languages():
    """Get supported languages."""
    return [
        "id", "en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", 
        "nl", "cs", "ar", "zh", "ja", "hu", "ko"
    ]

def check_availability():
    """Check if Coqui TTS is available."""
    try:
        from TTS.api import TTS
        return True
    except ImportError:
        return False

def get_info():
    """Get plugin information."""
    return {
        "name": "Coqui TTS",
        "description": "Advanced multilingual text-to-speech using Coqui TTS",
        "languages": get_languages(),
        "version": "1.0.0",
        "requires": ["TTS"],
        "available": check_availability()
    }
