"""
Whisper.cpp STT Plugin
Offline speech-to-text using whisper.cpp
"""

import logging
import subprocess
import tempfile
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Global configuration
WHISPER_EXECUTABLE = "whisper"  # Assumes whisper.cpp is installed and in PATH
DEFAULT_MODEL = "base"

def transcribe(audio_file=None, language="id"):
    """
    Transcribe audio file to text using whisper.cpp.
    
    Args:
        audio_file (str): Path to audio file, or None for live recording
        language (str): Language code
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        if audio_file is None:
            # Record live audio first
            audio_file = _record_temp_audio()
            if not audio_file:
                return None
        
        # Check if file exists
        if not Path(audio_file).exists():
            logger.error(f"Audio file not found: {audio_file}")
            return None
        
        # Prepare whisper command
        cmd = [
            WHISPER_EXECUTABLE,
            audio_file,
            "--language", language,
            "--model", DEFAULT_MODEL,
            "--output-txt",
            "--no-timestamps"
        ]
        
        logger.info(f"Running whisper transcription: {' '.join(cmd)}")
        
        # Run whisper
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            logger.error(f"Whisper failed: {result.stderr}")
            return None
        
        # Read the output text file
        txt_file = Path(audio_file).with_suffix('.txt')
        if txt_file.exists():
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            # Clean up temp files
            try:
                txt_file.unlink()
                if audio_file.startswith(tempfile.gettempdir()):
                    Path(audio_file).unlink()
            except:
                pass
            
            return text if text else None
        
        return None
        
    except subprocess.TimeoutExpired:
        logger.error("Whisper transcription timed out")
        return None
    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}")
        return None

def transcribe_live(duration=5, language="id"):
    """
    Transcribe live audio from microphone.
    
    Args:
        duration (int): Recording duration in seconds
        language (str): Language code
        
    Returns:
        str: Transcribed text or None if failed
    """
    audio_file = _record_temp_audio(duration)
    if audio_file:
        return transcribe(audio_file, language)
    return None

def _record_temp_audio(duration=5):
    """
    Record temporary audio file for transcription.
    
    Args:
        duration (int): Recording duration in seconds
        
    Returns:
        str: Path to temporary audio file or None if failed
    """
    try:
        # Try to use ffmpeg to record from microphone
        temp_file = tempfile.mktemp(suffix='.wav')
        
        cmd = [
            'ffmpeg',
            '-f', 'pulse',  # Linux
            '-i', 'default',
            '-t', str(duration),
            '-ar', '16000',
            '-ac', '1',
            '-y',
            temp_file
        ]
        
        logger.info(f"Recording audio for {duration} seconds...")
        
        result = subprocess.run(cmd, capture_output=True, timeout=duration + 5)
        
        if result.returncode == 0 and Path(temp_file).exists():
            return temp_file
        else:
            logger.error("Failed to record audio with ffmpeg")
            return None
            
    except subprocess.TimeoutExpired:
        logger.error("Audio recording timed out")
        return None
    except Exception as e:
        logger.error(f"Audio recording failed: {e}")
        return None

def get_languages():
    """Get supported languages."""
    return [
        "id", "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr", "pl",
        "ca", "nl", "ar", "sv", "it", "hi", "cs", "he", "fi", "vi", "uk", "el"
    ]

def check_availability():
    """Check if whisper.cpp is available."""
    try:
        result = subprocess.run([WHISPER_EXECUTABLE, "--help"], 
                              capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def get_info():
    """Get plugin information."""
    return {
        "name": "Whisper.cpp STT",
        "description": "Offline speech-to-text using whisper.cpp",
        "languages": get_languages(),
        "version": "1.0.0",
        "requires": ["whisper.cpp", "ffmpeg"],
        "available": check_availability()
    }
