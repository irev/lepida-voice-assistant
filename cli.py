#!/usr/bin/env python3
"""
Voice Assistant CLI Management Tool
Command line interface for managing the voice assistant
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_assistant():
    """Setup the voice assistant environment."""
    print("🔧 Setting up Voice Assistant...")
    
    try:
        from config.config import get_config
        from utils.health_check import HealthChecker
        
        # Run health check
        config = get_config()
        checker = HealthChecker(config)
        report = checker.run_all_checks()
        
        print(checker.format_report(report))
        
        if report["summary"]["error_count"] > 0:
            print("\n❌ Setup incomplete - please fix errors above")
            return False
        else:
            print("\n✅ Voice Assistant setup completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def check_health():
    """Run health check on the voice assistant."""
    print("🏥 Running Voice Assistant Health Check...")
    
    try:
        from config.config import get_config
        from utils.health_check import HealthChecker
        
        config = get_config()
        checker = HealthChecker(config)
        report = checker.run_all_checks()
        
        print(checker.format_report(report))
        
        return report["summary"]["overall_status"] == "ok"
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def generate_assets():
    """Generate audio assets."""
    print("🎵 Generating audio assets...")
    
    try:
        from assets.audio.generate_audio_assets import generate_all_assets
        generate_all_assets()
        return True
    except Exception as e:
        print(f"❌ Failed to generate assets: {e}")
        return False

def test_tts(text="Halo, ini adalah tes suara"):
    """Test text-to-speech functionality."""
    print(f"🗣️  Testing TTS with text: '{text}'")
    
    try:
        from config.config import get_config
        from utils.text_to_speech import TextToSpeech
        
        config = get_config()
        tts = TextToSpeech(config)
        tts.speak(text)
        print("✅ TTS test completed")
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_stt():
    """Test speech-to-text functionality."""
    print("🎤 Testing STT - please speak when prompted...")
    
    try:
        from config.config import get_config
        from utils.audio_transcription import AudioTranscription
        from helper.audio_processing import AudioProcessor
        
        config = get_config()
        stt = AudioTranscription(config)
        audio_processor = AudioProcessor(config)
        
        print("Listening for 5 seconds...")
        audio_data = audio_processor.record_audio(duration=5)
        
        if audio_data:
            text = stt.transcribe_audio_data(audio_data)
            print(f"✅ Recognized: '{text}'")
            return True
        else:
            print("❌ No audio recorded")
            return False
            
    except Exception as e:
        print(f"❌ STT test failed: {e}")
        return False

def list_audio_devices():
    """List available audio devices."""
    print("🎧 Available Audio Devices:")
    
    try:
        from config.config import get_config
        from utils.performance_monitor import AudioDeviceMonitor
        
        config = get_config()
        monitor = AudioDeviceMonitor(config)
        devices = monitor.get_audio_devices()
        default_devices = monitor.get_default_devices()
        
        print(f"\n📥 Input Devices:")
        for device in devices:
            if device['max_input_channels'] > 0:
                default_mark = " (DEFAULT)" if default_devices['input'] and device['index'] == default_devices['input']['index'] else ""
                print(f"  [{device['index']}] {device['name']}{default_mark}")
                
        print(f"\n📤 Output Devices:")
        for device in devices:
            if device['max_output_channels'] > 0:
                default_mark = " (DEFAULT)" if default_devices['output'] and device['index'] == default_devices['output']['index'] else ""
                print(f"  [{device['index']}] {device['name']}{default_mark}")
                
        monitor.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Failed to list devices: {e}")
        return False

def run_assistant():
    """Run the voice assistant application."""
    print("🤖 Starting Voice Assistant...")
    
    try:
        from app import main as app_main
        app_main()
        return True
    except KeyboardInterrupt:
        print("\n👋 Voice Assistant stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to start voice assistant: {e}")
        return False

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Voice Assistant Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py setup          # Setup and check the voice assistant
  python cli.py health         # Run health check
  python cli.py assets         # Generate audio assets
  python cli.py test-tts       # Test text-to-speech
  python cli.py test-stt       # Test speech-to-text
  python cli.py devices        # List audio devices
  python cli.py run            # Run the voice assistant
        """
    )
    
    parser.add_argument(
        'command',
        choices=['setup', 'health', 'assets', 'test-tts', 'test-stt', 'devices', 'run'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--text',
        default="Halo, ini adalah tes suara",
        help='Text to use for TTS test (default: "Halo, ini adalah tes suara")'
    )
    
    args = parser.parse_args()
    
    # Execute command
    success = False
    
    if args.command == 'setup':
        success = setup_assistant()
    elif args.command == 'health':
        success = check_health()
    elif args.command == 'assets':
        success = generate_assets()
    elif args.command == 'test-tts':
        success = test_tts(args.text)
    elif args.command == 'test-stt':
        success = test_stt()
    elif args.command == 'devices':
        success = list_audio_devices()
    elif args.command == 'run':
        success = run_assistant()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
