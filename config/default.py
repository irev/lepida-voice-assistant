import os
import yaml
from pathlib import Path

def create_default_config(config_path):
    """Create a default config.yml file if it doesn't exist."""
    
    default_config = {
        'app': {
            'name': 'Lepida Voice Assistant',
            'version': '1.0.0',
            'language': 'id'
        },
        'audio': {
            'input': {
                'device_index': None,
                'sample_rate': 16000,
                'channels': 1,
                'chunk_size': 1024,
                'format': 'int16'
            },
            'output': {
                'device_index': None,
                'sample_rate': 22050,
                'channels': 1
            },
            'processing': {
                'ambient_noise_duration': 1.0,
                'phrase_time_limit': 5.0,
                'timeout': 1.0
            }
        },
        'tts': {
            'primary_engine': 'mms_tts',
            'fallback_engines': ['coqui_tts', 'piper_tts'],
            'language': 'id',
            'voice_model': 'facebook/mms-tts-ind'
        },
        'stt': {
            'primary_engine': 'whisper_cpp',
            'fallback_engines': ['google_stt'],
            'language': 'id',
            'model_size': 'base'
        },
        'wakeword': {
            'enabled': True,
            'primary_engine': 'porcupine',
            'keywords': ['hey assistant', 'halo asisten'],
            'sensitivity': 0.5
        },
        'soundfx': {
            'enabled': True,
            'engine': 'beep',
            'volume': 0.7
        },
        'online': {
            'enabled': False,
            'google_stt_api_key': ''
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/voice_assistant.log',
            'console': True
        }
    }
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write default config to file
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(default_config, file, default_flow_style=False, allow_unicode=True)
    
    print(f"Created default configuration at {config_path}")
    return default_config
