#!/usr/bin/env python3
"""
Main Voice Assistant Application
Entry point for the Lepida Voice Assistant
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.config import get_config, load_env_variables
from utils.text_to_speech import TextToSpeech
from utils.audio_transcription import AudioTranscription
from utils.command_processor import VoiceCommandProcessor
from utils.wake_word_detection import WakeWordDetector
from utils.audio_effects import AudioEffectsManager
from utils.performance_monitor import PerformanceMonitor
from helper.audio_processing import AudioProcessor
from models.autoload import AutoLoader

class VoiceAssistant:
    """Main Voice Assistant class."""
    
    def __init__(self):
        """Initialize the voice assistant."""
        # Load environment variables
        load_env_variables()
        
        # Load configuration
        self.config = get_config()
        
        # Setup logging
        self.setup_logging()
        
        # Initialize components
        self.tts = None
        self.stt = None
        self.audio_processor = None
        self.command_processor = None
        self.wake_word_detector = None
        self.audio_effects = None
        self.performance_monitor = None
        self.autoloader = AutoLoader()
        
        self.logger.info("Voice Assistant initialized")
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_level = str(self.config.get('logging.level', 'INFO'))
        log_file = str(self.config.get('logging.file', 'logs/voice_assistant.log'))
        console_log = bool(self.config.get('logging.console', True))
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler() if console_log else logging.NullHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def initialize_components(self):
        """Initialize TTS, STT, and audio processing components."""
        try:
            # Initialize Audio Effects first
            self.audio_effects = AudioEffectsManager(self.config)
            self.logger.info("Audio effects initialized successfully")
            
            # Initialize Text-to-Speech
            self.tts = TextToSpeech(self.config)
            self.logger.info("TTS initialized successfully")
            
            # Initialize Speech-to-Text
            self.stt = AudioTranscription(self.config)
            self.logger.info("STT initialized successfully")
            
            # Initialize Audio Processor
            self.audio_processor = AudioProcessor(self.config)
            self.logger.info("Audio processor initialized successfully")
            
            # Initialize Command Processor
            self.command_processor = VoiceCommandProcessor(self.config, self.tts, self.stt)
            self.logger.info("Command processor initialized successfully")
            
            # Initialize Wake Word Detector
            self.wake_word_detector = WakeWordDetector(self.config)
            self.logger.info("Wake word detector initialized successfully")
            
            # Initialize Performance Monitor
            self.performance_monitor = PerformanceMonitor(self.config)
            self.performance_monitor.start_monitoring()
            self.logger.info("Performance monitor initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def speak(self, text, lang=None):
        """Convert text to speech and play it."""
        if self.tts:
            try:
                if lang is None:
                    lang = self.config.get('app.language', 'id')
                self.tts.speak(text, lang)
            except Exception as e:
                self.logger.error(f"Failed to speak text: {e}")
    
    def listen(self):
        """Listen for audio input and convert to text."""
        if self.stt:
            try:
                return self.stt.transcribe_audio()
            except Exception as e:
                self.logger.error(f"Failed to listen for audio: {e}")
                return None
        return None
    
    def run_interactive_mode(self):
        """Run the assistant in interactive mode."""
        self.logger.info("Starting interactive mode")
        
        # Play welcome sound
        if self.audio_effects:
            self.audio_effects.play_welcome()
        
        self.speak("Halo! Asisten suara siap membantu Anda.")
        
        try:
            while True:
                print("\nPilihan:")
                print("1. Berbicara dengan mikrofon")
                print("2. Ketik teks untuk diubah menjadi suara")
                print("3. Mode wake word (deteksi kata kunci)")
                print("4. Test sistem audio")
                print("5. Lihat status sistem")
                print("6. Keluar")
                
                choice = input("Pilih opsi (1-6): ").strip()
                
                if choice == "1":
                    print("Mendengarkan... (tekan Ctrl+C untuk berhenti)")
                    if self.audio_effects:
                        self.audio_effects.play_start()
                    
                    text = self.listen()
                    if text:
                        print(f"Anda berkata: {text}")
                        
                        # Process command
                        if self.command_processor:
                            response = self.command_processor.process_command(text)
                            print(f"Respon: {response}")
                            self.speak(response)
                        else:
                            self.speak(f"Anda mengatakan: {text}")
                            
                        if self.audio_effects:
                            self.audio_effects.play_success()
                    else:
                        print("Tidak ada suara yang terdeteksi.")
                        if self.audio_effects:
                            self.audio_effects.play_error()
                
                elif choice == "2":
                    text = input("Masukkan teks untuk diubah menjadi suara: ")
                    if text.strip():
                        # Process as command if command processor is available
                        if self.command_processor:
                            response = self.command_processor.process_command(text)
                            print(f"Respon: {response}")
                            self.speak(response)
                        else:
                            self.speak(text)
                        
                        if self.audio_effects:
                            self.audio_effects.play_success()
                    else:
                        print("Teks kosong!")
                        if self.audio_effects:
                            self.audio_effects.play_error()
                
                elif choice == "3":
                    self._run_wake_word_mode()
                
                elif choice == "4":
                    self._test_audio_system()
                
                elif choice == "5":
                    self._show_system_status()
                
                elif choice == "6":
                    if self.audio_effects:
                        self.audio_effects.play_goodbye()
                    self.speak("Sampai jumpa!")
                    break
                
                else:
                    print("Pilihan tidak valid!")
                    if self.audio_effects:
                        self.audio_effects.play_error()
                    
        except KeyboardInterrupt:
            print("\nKeluar dari aplikasi...")
            if self.audio_effects:
                self.audio_effects.play_goodbye()
            self.speak("Sampai jumpa!")
        except Exception as e:
            self.logger.error(f"Error in interactive mode: {e}")
            if self.audio_effects:
                self.audio_effects.play_error()
    
    def _run_wake_word_mode(self):
        """Run wake word detection mode."""
        if not self.wake_word_detector or not self.wake_word_detector.enabled:
            print("Wake word detection tidak tersedia.")
            if self.audio_effects:
                self.audio_effects.play_error()
            return
        
        print("Mode wake word aktif. Katakan kata kunci untuk mengaktifkan asisten.")
        print("Tekan Enter untuk keluar dari mode wake word.")
        
        def on_wake_word(keyword, index):
            print(f"\nWake word terdeteksi: {keyword}")
            if self.audio_effects:
                self.audio_effects.play_notification()
            
            # Listen for command after wake word
            print("Mendengarkan perintah...")
            text = self.listen()
            if text:
                print(f"Perintah: {text}")
                if self.command_processor:
                    response = self.command_processor.process_command(text)
                    print(f"Respon: {response}")
                    self.speak(response)
                    if self.audio_effects:
                        self.audio_effects.play_success()
                else:
                    self.speak(f"Anda mengatakan: {text}")
            
            print("Menunggu wake word lagi...")
        
        # Start wake word detection
        if self.wake_word_detector.start_detection(on_wake_word):
            if self.audio_effects:
                self.audio_effects.play_start()
            
            try:
                input()  # Wait for Enter key
            except KeyboardInterrupt:
                pass
            
            self.wake_word_detector.stop_detection()
            print("Mode wake word dihentikan.")
            if self.audio_effects:
                self.audio_effects.play_stop()
        else:
            print("Gagal memulai wake word detection.")
            if self.audio_effects:
                self.audio_effects.play_error()
    
    def _test_audio_system(self):
        """Test audio system components."""
        print("Testing sistem audio...")
        
        if self.audio_effects:
            print("Testing audio effects...")
            self.audio_effects.test_audio_system()
        
        if self.tts:
            print("Testing text-to-speech...")
            self.speak("Ini adalah tes sistem text-to-speech.")
        
        if self.stt:
            print("Testing speech-to-text...")
            print("Silakan bicara selama 3 detik...")
            text = self.listen()
            if text:
                print(f"STT result: {text}")
            else:
                print("STT test failed atau tidak ada suara.")
        
        print("Audio system test selesai.")
    
    def _show_system_status(self):
        """Show system component status."""
        print("\n=== STATUS SISTEM ===")
        
        # TTS Status
        if self.tts:
            print("✅ Text-to-Speech: Aktif")
        else:
            print("❌ Text-to-Speech: Tidak aktif")
        
        # STT Status
        if self.stt:
            print("✅ Speech-to-Text: Aktif")
        else:
            print("❌ Speech-to-Text: Tidak aktif")
        
        # Audio Processor Status
        if self.audio_processor:
            print("✅ Audio Processor: Aktif")
        else:
            print("❌ Audio Processor: Tidak aktif")
        
        # Command Processor Status
        if self.command_processor:
            print("✅ Command Processor: Aktif")
            commands = self.command_processor.get_command_types()
            print(f"   Perintah tersedia: {', '.join(commands)}")
        else:
            print("❌ Command Processor: Tidak aktif")
        
        # Wake Word Detector Status
        if self.wake_word_detector:
            status = self.wake_word_detector.get_status()
            if status['enabled']:
                print(f"✅ Wake Word Detector: Aktif ({status['engine']})")
                print(f"   Keywords: {', '.join(status['keywords'])}")
                print(f"   Sensitivity: {status['sensitivity']}")
            else:
                print("⚠️  Wake Word Detector: Tersedia tapi tidak aktif")
        else:
            print("❌ Wake Word Detector: Tidak tersedia")
        
        # Audio Effects Status
        if self.audio_effects:
            status = self.audio_effects.get_status()
            if status['enabled']:
                print(f"✅ Audio Effects: Aktif ({status['engine']})")
                print(f"   Volume: {status['volume']}")
                print(f"   Sounds: {len(status['available_sounds'])} tersedia")
            else:
                print("⚠️  Audio Effects: Tersedia tapi tidak aktif")
        else:
            print("❌ Audio Effects: Tidak tersedia")
        
        # Configuration
        print(f"\n📝 Konfigurasi:")
        print(f"   Bahasa: {self.config.get('app.language', 'tidak diset')}")
        print(f"   TTS Engine: {self.config.get('tts.primary_engine', 'tidak diset')}")
        print(f"   STT Engine: {self.config.get('stt.primary_engine', 'tidak diset')}")
        
        print("==================\n")

def main():
    """Main entry point."""
    try:
        # Create voice assistant instance
        assistant = VoiceAssistant()
        
        # Initialize components
        assistant.initialize_components()
        
        # Check if running with command line arguments
        if len(sys.argv) > 1:
            # Command line mode
            text = " ".join(sys.argv[1:])
            assistant.speak(text)
        else:
            # Interactive mode
            assistant.run_interactive_mode()
            
    except Exception as e:
        print(f"Failed to start voice assistant: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()