"""
Piper TTS Plugin
Lightweight and fast neural text-to-speech
"""

import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

# Configuration
PIPER_EXECUTABLE = "piper"  # Assumes piper is installed and in PATH
DEFAULT_MODEL = "id_ID-fgl-medium"  # Indonesian model

def run(text: str, lang: str = "id", output_file: str = None):
    """
    Convert text to speech using Piper TTS.
    
    Args:
        text (str): Text to convert to speech
        lang (str): Language code
        output_file (str): Optional file path to save audio
    """
    try:
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return
        
        # Determine output file
        if output_file is None:
            output_file = "outputs/sound/piper_output.wav"
        
        # Create output directory
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Converting text with Piper TTS: '{text[:50]}...'")
        
        # Get model for language
        model_path = _get_model_for_language(lang)
        if not model_path:
            raise Exception(f"No Piper model available for language: {lang}")
        
        # Prepare piper command
        cmd = [
            PIPER_EXECUTABLE,
            "--model", model_path,
            "--output_file", output_file
        ]
        
        # Run piper with text input
        result = subprocess.run(
            cmd,
            input=text,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise Exception(f"Piper TTS failed: {result.stderr}")
        
        logger.info(f"Audio saved to {output_file}")
        
        # Try to play the audio
        _play_audio(output_file)
        
    except subprocess.TimeoutExpired:
        logger.error("Piper TTS timed out")
        raise
    except Exception as e:
        logger.error(f"Piper TTS conversion failed: {e}")
        raise

def _get_model_for_language(lang):
    """Get Piper model path for language."""
    models_dir = Path("models/piper")
    
    # Model mapping
    language_models = {
        "id": "id_ID-fgl-medium.onnx",
        "en": "en_US-lessac-medium.onnx",
        "es": "es_ES-mls_10246-low.onnx",
        "fr": "fr_FR-mls_1840-low.onnx",
        "de": "de_DE-thorsten_emotional-medium.onnx",
        "it": "it_IT-riccardo_fasol-x_low.onnx",
        "nl": "nl_NL-mls_5809-low.onnx"
    }
    
    model_file = language_models.get(lang, language_models.get("en"))
    model_path = models_dir / model_file
    
    if model_path.exists():
        return str(model_path)
    
    # Try to use system-wide models
    try:
        result = subprocess.run([PIPER_EXECUTABLE, "--list-models"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and model_file in result.stdout:
            return model_file
    except:
        pass
    
    return None

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
    return ["default"]

def set_voice(voice_id):
    """Set voice."""
    return voice_id == "default"

def get_languages():
    """Get supported languages."""
    return ["id", "en", "es", "fr", "de", "it", "nl"]

def check_availability():
    """Check if Piper is available."""
    try:
        result = subprocess.run([PIPER_EXECUTABLE, "--version"], 
                              capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def download_model(language="id"):
    """Download Piper model for language."""
    models_dir = Path("models/piper")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # This would implement model downloading
    # For now, just provide instructions
    logger.info(f"To download Piper models for {language}:")
    logger.info("Visit: https://github.com/rhasspy/piper/releases")
    logger.info(f"Download model to: {models_dir}")

def get_info():
    """Get plugin information."""
    return {
        "name": "Piper TTS",
        "description": "Fast and lightweight neural text-to-speech",
        "languages": get_languages(),
        "version": "1.0.0",
        "requires": ["piper"],
        "available": check_availability()
    }
