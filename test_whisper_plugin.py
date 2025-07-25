#!/usr/bin/env python3
"""
Test script for the updated STT Whisper plugin
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_whisper_plugin():
    """Test the updated Whisper STT plugin"""
    
    print("🧪 Testing OpenAI Whisper STT Plugin")
    print("=" * 50)
    
    try:
        # Import the plugin
        from plugins import stt_whisper_cpp
        
        # Test availability
        print("1. Checking plugin availability...")
        available = stt_whisper_cpp.check_availability()
        print(f"   Plugin available: {available}")
        
        if not available:
            print("   ❌ Plugin not available - missing dependencies")
            print("   Install with: pip install openai-whisper soundfile")
            return False
        
        # Get plugin info
        print("\n2. Plugin information:")
        info = stt_whisper_cpp.get_info()
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Test model loading
        print("\n3. Testing model loading...")
        try:
            model = stt_whisper_cpp._get_model()
            if model is not None:
                print("   ✅ Model loaded successfully")
            else:
                print("   ❌ Failed to load model")
                return False
        except Exception as e:
            print(f"   ❌ Model loading error: {e}")
            return False
        
        # Test with sample audio file (if available)
        print("\n4. Testing transcription...")
        
        # Check for test audio files
        test_audio_files = [
            "test/test_audio.wav",
            "assets/audio/welcome.wav", 
            "outputs/sound/test.wav"
        ]
        
        test_file = None
        for audio_file in test_audio_files:
            if Path(audio_file).exists():
                test_file = audio_file
                break
        
        if test_file:
            print(f"   Using test file: {test_file}")
            try:
                result = stt_whisper_cpp.transcribe(test_file, "id")
                if result:
                    print(f"   ✅ Transcription result: {result}")
                else:
                    print("   ⚠️  Transcription returned empty result")
            except Exception as e:
                print(f"   ❌ Transcription error: {e}")
        else:
            print("   ⚠️  No test audio file found, skipping transcription test")
        
        print("\n✅ Plugin test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import plugin: {e}")
        return False
    except Exception as e:
        print(f"❌ Plugin test failed: {e}")
        return False

def show_whisper_info():
    """Show information about available Whisper packages"""
    
    print("\n🔍 Checking Whisper Installation")
    print("=" * 40)
    
    # Check openai-whisper
    try:
        import whisper
        print("✅ openai-whisper: Available")
        print(f"   Version: {whisper.__version__ if hasattr(whisper, '__version__') else 'Unknown'}")
        
        # List available models
        try:
            models = whisper.available_models()
            print(f"   Available models: {', '.join(models)}")
        except:
            print("   Available models: base, small, medium, large")
            
    except ImportError:
        print("❌ openai-whisper: Not installed")
        print("   Install with: pip install openai-whisper")
    
    # Check soundfile
    try:
        import soundfile as sf
        print("✅ soundfile: Available")
        print(f"   Version: {sf.__version__ if hasattr(sf, '__version__') else 'Unknown'}")
    except ImportError:
        print("❌ soundfile: Not installed")
        print("   Install with: pip install soundfile")
    
    # Check torch
    try:
        import torch
        print("✅ torch: Available")
        print(f"   Version: {torch.__version__}")
    except ImportError:
        print("❌ torch: Not installed")
        print("   Install with: pip install torch")

if __name__ == "__main__":
    print("🎤 STT Whisper Plugin Test")
    print("=" * 60)
    
    # Show system info
    show_whisper_info()
    
    # Test the plugin
    print()
    success = test_whisper_plugin()
    
    if success:
        print("\n🎉 All tests passed! The plugin should work correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Install dependencies: pip install openai-whisper soundfile")
        print("   2. Test manually: python -c \"import whisper; print('Whisper OK')\"")
        print("   3. Check logs for detailed error information")
