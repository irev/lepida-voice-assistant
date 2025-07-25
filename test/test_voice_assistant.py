"""
Test suite for the Voice Assistant application
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_number_to_text():
    """Test number to text conversion."""
    from helper.numberToText import NumberToText
    
    # Test basic numbers
    assert NumberToText.convert(0) == "nol"
    assert NumberToText.convert(1) == "satu"
    assert NumberToText.convert(10) == "sepuluh"
    assert NumberToText.convert(12) == "dua belas"
    assert NumberToText.convert(20) == "dua puluh"
    assert NumberToText.convert(25) == "dua puluh lima"
    assert NumberToText.convert(100) == "seratus"
    assert NumberToText.convert(150) == "seratus lima puluh"
    assert NumberToText.convert(1000) == "seribu"

def test_config_loading():
    """Test configuration loading."""
    from config.config import Config
    
    # Test config creation and loading
    config = Config()
    assert config.config is not None
    
    # Test getting values
    app_name = config.get('app.name')
    assert app_name is not None
    
    # Test default values
    unknown_value = config.get('unknown.key', 'default')
    assert unknown_value == 'default'

def test_autoloader():
    """Test plugin autoloader."""
    from models.autoload import AutoLoader
    
    loader = AutoLoader()
    
    # Test getting available plugins
    available_plugins = loader.get_available_plugins('tts')
    assert isinstance(available_plugins, list)
    
    # Test loading a plugin (should handle missing plugins gracefully)
    plugin = loader.load_plugin('tts', 'nonexistent')
    assert plugin is None

def test_plugin_mms_tts_info():
    """Test MMS TTS plugin info."""
    try:
        from plugins.tts_mms_tts import get_info
        info = get_info()
        assert info['name'] == 'MMS TTS'
        assert 'id' in info['languages']
    except ImportError:
        pytest.skip("MMS TTS plugin dependencies not available")

def test_plugin_whisper_info():
    """Test Whisper STT plugin info."""
    from plugins.stt_whisper_cpp import get_info
    info = get_info()
    assert info['name'] == 'OpenAI Whisper STT'
    assert 'id' in info['languages']

def test_soundfx_plugin():
    """Test sound effects plugin."""
    from plugins.soundfx_beep import get_info
    info = get_info()
    assert info['name'] == 'Beep SoundFX'

def test_text_preprocessing():
    """Test text preprocessing for TTS."""
    import re
    from helper.numberToText import NumberToText
    
    def process_numbers_in_text(text):
        def number_to_words(match):
            try:
                number = int(match.group())
                return NumberToText.convert(number)
            except (ValueError, OverflowError):
                return match.group()
        
        return re.sub(r'\b\d{1,3}(?:[.,]\d{3})*\b|\b\d+\b', number_to_words, text)
    
    # Test number conversion in text
    test_text = "Saya punya 15 apel dan 100 jeruk"
    processed = process_numbers_in_text(test_text)
    expected = "Saya punya lima belas apel dan seratus jeruk"
    assert processed == expected

def test_mms_model_info():
    """Test MMS TTS model info."""
    try:
        from models.mms_tts import MMSTTSModel
        # Just test that the class can be imported
        assert MMSTTSModel is not None
    except ImportError:
        pytest.skip("MMS TTS model dependencies not available")

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
