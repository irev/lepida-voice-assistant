"""
Google Speech-to-Text Plugin
Cloud-based speech recognition using Google Cloud Speech API
"""

import logging
import tempfile
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def transcribe(audio_file=None, language="id"):
    """
    Transcribe audio using Google Speech-to-Text API.
    
    Args:
        audio_file (str): Path to audio file, or None for live recording
        language (str): Language code
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        from google.cloud import speech
        
        # Initialize client
        client = speech.SpeechClient()
        
        # Handle live recording
        if audio_file is None:
            audio_file = _record_temp_audio()
            if not audio_file:
                return None
        
        # Check if file exists
        if not Path(audio_file).exists():
            logger.error(f"Audio file not found: {audio_file}")
            return None
        
        logger.info(f"Transcribing audio with Google STT: {audio_file}")
        
        # Load audio file
        with open(audio_file, 'rb') as audio_data:
            content = audio_data.read()
        
        # Configure recognition
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=_get_google_language_code(language),
            enable_automatic_punctuation=True,
        )
        
        # Perform transcription
        response = client.recognize(config=config, audio=audio)
        
        # Extract text from response
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            logger.info(f"Transcription result: {transcript}")
            
            # Clean up temp file
            if audio_file.startswith(tempfile.gettempdir()):
                try:
                    Path(audio_file).unlink()
                except:
                    pass
            
            return transcript.strip() if transcript else None
        
        return None
        
    except ImportError:
        raise ImportError("google-cloud-speech library not available. Install with: pip install google-cloud-speech")
    except Exception as e:
        logger.error(f"Google STT transcription failed: {e}")
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

def transcribe_streaming(language="id", callback=None):
    """
    Real-time streaming transcription.
    
    Args:
        language (str): Language code
        callback (function): Function to call with transcription results
    """
    try:
        from google.cloud import speech
        import pyaudio
        import queue
        import threading
        
        # Audio recording parameters
        RATE = 16000
        CHUNK = int(RATE / 10)  # 100ms
        
        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=_get_google_language_code(language),
        )
        
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )
        
        # Audio queue
        audio_queue = queue.Queue()
        
        def audio_callback(in_data, frame_count, time_info, status):
            audio_queue.put(in_data)
            return (None, pyaudio.paContinue)
        
        # Start audio stream
        audio_interface = pyaudio.PyAudio()
        stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=audio_callback,
        )
        
        def request_generator():
            while True:
                chunk = audio_queue.get()
                if chunk is None:
                    return
                yield speech.StreamingRecognizeRequest(audio_content=chunk)
        
        requests = request_generator()
        responses = client.streaming_recognize(streaming_config, requests)
        
        for response in responses:
            for result in response.results:
                if result.is_final:
                    transcript = result.alternatives[0].transcript
                    if callback:
                        callback(transcript)
                    else:
                        logger.info(f"Final transcript: {transcript}")
        
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()
        
    except Exception as e:
        logger.error(f"Streaming transcription failed: {e}")

def _record_temp_audio(duration=5):
    """Record temporary audio file."""
    try:
        import pyaudio
        import wave
        
        # Audio parameters
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        audio = pyaudio.PyAudio()
        
        # Open stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        logger.info(f"Recording audio for {duration} seconds...")
        
        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save to temporary file
        temp_file = tempfile.mktemp(suffix='.wav')
        with wave.open(temp_file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        return temp_file
        
    except Exception as e:
        logger.error(f"Audio recording failed: {e}")
        return None

def _get_google_language_code(lang_code):
    """Convert language code to Google format."""
    mapping = {
        "id": "id-ID",
        "en": "en-US",
        "es": "es-ES",
        "fr": "fr-FR",
        "de": "de-DE",
        "it": "it-IT",
        "pt": "pt-BR",
        "ru": "ru-RU",
        "ja": "ja-JP",
        "ko": "ko-KR",
        "zh": "zh-CN"
    }
    return mapping.get(lang_code, "en-US")

def get_languages():
    """Get supported languages."""
    return [
        "id", "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
        "ar", "hi", "th", "vi", "tr", "pl", "nl", "sv", "da", "no", "fi"
    ]

def check_availability():
    """Check if Google Speech API is available."""
    try:
        from google.cloud import speech
        # Check if credentials are available
        api_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        return api_key is not None
    except ImportError:
        return False

def get_info():
    """Get plugin information."""
    return {
        "name": "Google Speech-to-Text",
        "description": "Cloud-based speech recognition using Google Cloud Speech API",
        "languages": get_languages(),
        "version": "1.0.0",
        "requires": ["google-cloud-speech", "pyaudio"],
        "available": check_availability()
    }
