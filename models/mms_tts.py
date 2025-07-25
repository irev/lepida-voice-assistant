"""
Facebook MMS TTS Model Implementation
Core implementation of the MMS (Massively Multilingual Speech) TTS model
"""

import logging
import torch
import soundfile as sf
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class MMSTTSModel:
    """Facebook MMS TTS model wrapper."""
    
    def __init__(self, model_name="facebook/mms-tts-ind", device=None):
        """
        Initialize MMS TTS model.
        
        Args:
            model_name (str): Hugging Face model name
            device (str): Device to use ('cpu', 'cuda', etc.)
        """
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.tokenizer = None
        self.logger = logging.getLogger(__name__)
        
        # Load model
        self._load_model()
    
    def _load_model(self):
        """Load the MMS TTS model and tokenizer."""
        try:
            from transformers import VitsModel, AutoTokenizer
            
            self.logger.info(f"Loading MMS TTS model: {self.model_name}")
            
            # Load model and tokenizer
            self.model = VitsModel.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Move model to device
            self.model = self.model.to(self.device)
            
            self.logger.info(f"MMS TTS model loaded successfully on {self.device}")
            
        except ImportError:
            raise ImportError("transformers library is required. Install with: pip install transformers torch")
        except Exception as e:
            self.logger.error(f"Failed to load MMS TTS model: {e}")
            raise
    
    def synthesize(self, text, output_file=None):
        """
        Synthesize speech from text.
        
        Args:
            text (str): Text to synthesize
            output_file (str): Optional output file path
            
        Returns:
            tuple: (audio_array, sample_rate)
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            self.logger.info(f"Synthesizing text: '{text[:50]}...'")
            
            # Tokenize input text
            inputs = self.tokenizer(text, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate audio
            with torch.no_grad():
                output = self.model(**inputs)
            
            # Extract audio waveform
            audio_array = output.waveform.squeeze().cpu().numpy()
            sample_rate = self.model.config.sampling_rate
            
            # Save to file if specified
            if output_file:
                self.save_audio(audio_array, output_file, sample_rate)
            
            self.logger.info("Speech synthesis completed")
            return audio_array, sample_rate
            
        except Exception as e:
            self.logger.error(f"Speech synthesis failed: {e}")
            raise
    
    def save_audio(self, audio_array, file_path, sample_rate=None):
        """
        Save audio array to file.
        
        Args:
            audio_array (numpy.ndarray): Audio data
            file_path (str): Output file path
            sample_rate (int): Sample rate
        """
        if sample_rate is None:
            sample_rate = self.model.config.sampling_rate
        
        try:
            # Create output directory
            output_path = Path(file_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save audio
            sf.write(file_path, audio_array, sample_rate)
            self.logger.info(f"Audio saved to: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save audio: {e}")
            raise
    
    def get_model_info(self):
        """Get model information."""
        if self.model:
            return {
                "model_name": self.model_name,
                "device": self.device,
                "sample_rate": self.model.config.sampling_rate,
                "vocab_size": self.model.config.vocab_size if hasattr(self.model.config, 'vocab_size') else None
            }
        return None
    
    def cleanup(self):
        """Clean up model resources."""
        if self.model:
            del self.model
            self.model = None
        
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        
        # Clear CUDA cache if using GPU
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.logger.info("Model resources cleaned up")

# Global model instance for reuse
_global_model = None

def get_global_model(model_name="facebook/mms-tts-ind", device=None):
    """Get global model instance (singleton pattern)."""
    global _global_model
    
    if _global_model is None:
        _global_model = MMSTTSModel(model_name, device)
    
    return _global_model

def cleanup_global_model():
    """Clean up global model instance."""
    global _global_model
    
    if _global_model:
        _global_model.cleanup()
        _global_model = None
