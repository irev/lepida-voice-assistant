"""
MMS TTS Plugin
Facebook MMS Text-to-Speech implementation
"""

import logging
import torch
import soundfile as sf
import numpy as np
from pathlib import Path

# Try to import required libraries
try:
    from transformers import VitsModel, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Global variables for model caching
_model = None
_tokenizer = None
_model_name = "facebook/mms-tts-ind"

def _load_model():
    """Load the MMS TTS model and tokenizer."""
    global _model, _tokenizer
    
    if not TRANSFORMERS_AVAILABLE:
        raise ImportError("transformers library is not available. Install with: pip install transformers torch")
    
    if _model is None or _tokenizer is None:
        logger.info(f"Loading MMS TTS model: {_model_name}")
        _model = VitsModel.from_pretrained(_model_name)
        _tokenizer = AutoTokenizer.from_pretrained(_model_name)
        logger.info("MMS TTS model loaded successfully")

def run(text: str, lang: str = "id", output_file: str = None):
    """
    Convert text to speech using MMS TTS.
    
    Args:
        text (str): Text to convert to speech
        lang (str): Language code (currently only 'id' supported)
        output_file (str): Optional file path to save audio
    """
    try:
        # Load model if not already loaded
        _load_model()
        
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return
        
        logger.info(f"Converting text to speech: '{text[:50]}...'")
        
        # Tokenize the input text
        inputs = _tokenizer(text, return_tensors="pt")
        
        # Generate audio
        with torch.no_grad():
            output = _model(inputs["input_ids"])
        
        # Extract the audio waveform
        audio_array = output.waveform.squeeze().cpu().numpy()
        
        # Determine output file
        if output_file is None:
            output_file = "outputs/sound/output.wav"
        
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the audio to a file
        sf.write(output_file, audio_array, _model.config.sampling_rate)
        logger.info(f"Audio saved to {output_file}")
        
        # Try to play the audio if possible
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
        except ImportError:
            logger.info("pygame not available for audio playback")
        except Exception as e:
            logger.warning(f"Could not play audio: {e}")
        
        return audio_array
        
    except Exception as e:
        logger.error(f"MMS TTS conversion failed: {e}")
        raise

def get_voices():
    """Get available voices (MMS only supports Indonesian currently)."""
    return ["id"]

def set_voice(voice_id):
    """Set voice (not supported in MMS)."""
    if voice_id == "id":
        return True
    return False

def get_info():
    """Get plugin information."""
    return {
        "name": "MMS TTS",
        "description": "Facebook MMS Text-to-Speech for Indonesian",
        "languages": ["id"],
        "version": "1.0.0",
        "requires": ["transformers", "torch", "soundfile"]
    }
