"""
Porcupine Wake Word Detection Plugin
Wake word detection using Picovoice Porcupine
"""

import logging
import threading
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# Global variables
_porcupine = None
_audio_stream = None
_is_listening = False
_wake_word_callback = None

def initialize(access_key=None, keywords=None, sensitivity=0.5):
    """
    Initialize Porcupine wake word detection.
    
    Args:
        access_key (str): Picovoice access key
        keywords (list): List of wake words
        sensitivity (float): Detection sensitivity (0.0 to 1.0)
    """
    global _porcupine
    
    try:
        import pvporcupine
        
        if access_key is None:
            access_key = os.getenv('PORCUPINE_ACCESS_KEY')
            if not access_key:
                raise ValueError("Porcupine access key not provided")
        
        if keywords is None:
            keywords = ['hey google', 'alexa']  # Built-in keywords
        
        logger.info(f"Initializing Porcupine with keywords: {keywords}")
        
        _porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=keywords,
            sensitivities=[sensitivity] * len(keywords)
        )
        
        logger.info("Porcupine initialized successfully")
        return True
        
    except ImportError:
        raise ImportError("pvporcupine library not available. Install with: pip install pvporcupine")
    except Exception as e:
        logger.error(f"Failed to initialize Porcupine: {e}")
        raise

def start_listening(callback=None):
    """
    Start listening for wake words.
    
    Args:
        callback (function): Function to call when wake word is detected
    """
    global _is_listening, _wake_word_callback
    
    if _porcupine is None:
        raise RuntimeError("Porcupine not initialized. Call initialize() first.")
    
    _wake_word_callback = callback
    _is_listening = True
    
    # Start listening thread
    listen_thread = threading.Thread(target=_listen_loop, daemon=True)
    listen_thread.start()
    
    logger.info("Started listening for wake words")

def stop_listening():
    """Stop listening for wake words."""
    global _is_listening
    
    _is_listening = False
    logger.info("Stopped listening for wake words")

def _listen_loop():
    """Main listening loop."""
    try:
        import pyaudio
        
        # Initialize audio stream
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=_porcupine.sample_rate,
            input=True,
            frames_per_buffer=_porcupine.frame_length
        )
        
        logger.info("Audio stream started for wake word detection")
        
        while _is_listening:
            try:
                # Read audio frame
                pcm = stream.read(_porcupine.frame_length, exception_on_overflow=False)
                pcm = [int.from_bytes(pcm[i:i+2], byteorder='little', signed=True) 
                       for i in range(0, len(pcm), 2)]
                
                # Process frame
                keyword_index = _porcupine.process(pcm)
                
                if keyword_index >= 0:
                    logger.info(f"Wake word detected: index {keyword_index}")
                    
                    if _wake_word_callback:
                        try:
                            _wake_word_callback(keyword_index)
                        except Exception as e:
                            logger.error(f"Error in wake word callback: {e}")
                
            except Exception as e:
                logger.error(f"Error in listen loop: {e}")
                time.sleep(0.1)
        
        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
    except ImportError:
        logger.error("pyaudio not available for wake word detection")
    except Exception as e:
        logger.error(f"Listen loop failed: {e}")

def cleanup():
    """Cleanup Porcupine resources."""
    global _porcupine, _is_listening
    
    _is_listening = False
    
    if _porcupine:
        _porcupine.delete()
        _porcupine = None
    
    logger.info("Porcupine cleaned up")

def get_builtin_keywords():
    """Get list of built-in keywords."""
    try:
        import pvporcupine
        return list(pvporcupine.KEYWORDS.keys())
    except ImportError:
        return []

def check_availability():
    """Check if Porcupine is available."""
    try:
        import pvporcupine
        return True
    except ImportError:
        return False

def get_info():
    """Get plugin information."""
    return {
        "name": "Porcupine Wake Word",
        "description": "Wake word detection using Picovoice Porcupine",
        "keywords": get_builtin_keywords(),
        "version": "1.0.0",
        "requires": ["pvporcupine", "pyaudio"],
        "available": check_availability()
    }
