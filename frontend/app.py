from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import logging
import threading
import time
import psutil
import yaml
from datetime import datetime, timedelta

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import get_config
from utils.text_to_speech import TextToSpeech
from utils.audio_transcription import AudioTranscription
from utils.system_monitor import SystemMonitor
from utils.wake_word_detection import WakeWordDetection
from helper.audio_processing import AudioProcessor

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceAssistantAPI:
    def __init__(self):
        self.config = get_config()
        self.tts = None
        self.stt = None
        self.wake_word = None
        self.system_monitor = SystemMonitor()
        self.audio_processor = AudioProcessor(self.config)
        self.is_running = True
        self.start_time = datetime.now()
        
        # Initialize components
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize TTS, STT, and Wake Word components"""
        try:
            # Initialize TTS
            self.tts = TextToSpeech(self.config)
            logger.info("TTS component initialized")
            
            # Initialize STT
            self.stt = AudioTranscription(self.config)
            logger.info("STT component initialized")
            
            # Initialize Wake Word Detection
            self.wake_word = WakeWordDetection(self.config)
            logger.info("Wake Word component initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
    
    def get_system_info(self):
        """Get system information"""
        try:
            uptime = datetime.now() - self.start_time
            uptime_str = str(uptime).split('.')[0]  # Remove microseconds
            
            return {
                'cpu_usage': psutil.cpu_percent(interval=1),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent,
                'uptime': uptime_str,
                'version': '1.0.0',
                'python_version': sys.version.split()[0]
            }
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {}
    
    def get_performance_data(self):
        """Get real-time performance data"""
        try:
            return {
                'cpu_usage': psutil.cpu_percent(interval=0.1),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get performance data: {e}")
            return {}

# Initialize API instance
api = VoiceAssistantAPI()

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'tts': api.tts is not None,
            'stt': api.stt is not None,
            'wake_word': api.wake_word is not None
        }
    })

@app.route('/api/config')
def get_config_endpoint():
    """Get current configuration"""
    return jsonify(api.config.config)

@app.route('/api/config/update', methods=['POST'])
def update_config():
    """Update configuration setting"""
    try:
        data = request.get_json()
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({'error': 'Key is required'}), 400
        
        # Update configuration using the Config object's update method
        api.config.update(key, value)
        
        logger.info(f"Updated config: {key} = {value}")
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Failed to update config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/info')
def system_info():
    """Get system information"""
    return jsonify(api.get_system_info())

@app.route('/api/system/performance')
def system_performance():
    """Get system performance data"""
    return jsonify(api.get_performance_data())

@app.route('/api/tts/test', methods=['POST'])
def test_tts():
    """Test text-to-speech"""
    try:
        data = request.get_json()
        text = data.get('text', 'Hello from Lepida Voice Assistant')
        
        if not api.tts:
            return jsonify({'error': 'TTS not initialized'}), 500
        
        # Generate speech
        success = api.tts.speak(text)
        
        if success:
            return jsonify({'success': True, 'message': 'TTS test completed'})
        else:
            return jsonify({'error': 'TTS test failed'}), 500
            
    except Exception as e:
        logger.error(f"TTS test error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stt/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe uploaded audio"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if not api.stt:
            return jsonify({'error': 'STT not initialized'}), 500
        
        # Save temporary audio file
        temp_path = os.path.join('temp', 'upload.wav')
        os.makedirs('temp', exist_ok=True)
        audio_file.save(temp_path)
        
        # Transcribe audio
        text = api.stt.transcribe(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({'text': text, 'success': True})
        
    except Exception as e:
        logger.error(f"STT transcription error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/test', methods=['POST'])
def test_audio():
    """Test audio system"""
    try:
        # Test audio input/output
        success = api.audio_processor.test_audio_system()
        
        if success:
            return jsonify({'success': True, 'message': 'Audio test completed'})
        else:
            return jsonify({'error': 'Audio test failed'}), 500
            
    except Exception as e:
        logger.error(f"Audio test error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/wakeword/start', methods=['POST'])
def start_wake_word():
    """Start wake word detection"""
    try:
        if not api.wake_word:
            return jsonify({'error': 'Wake word detection not initialized'}), 500
        
        success = api.wake_word.start_detection()
        
        if success:
            return jsonify({'success': True, 'message': 'Wake word detection started'})
        else:
            return jsonify({'error': 'Failed to start wake word detection'}), 500
            
    except Exception as e:
        logger.error(f"Wake word start error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/wakeword/stop', methods=['POST'])
def stop_wake_word():
    """Stop wake word detection"""
    try:
        if not api.wake_word:
            return jsonify({'error': 'Wake word detection not initialized'}), 500
        
        success = api.wake_word.stop_detection()
        
        if success:
            return jsonify({'success': True, 'message': 'Wake word detection stopped'})
        else:
            return jsonify({'error': 'Failed to stop wake word detection'}), 500
            
    except Exception as e:
        logger.error(f"Wake word stop error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/reload', methods=['POST'])
def reload_system():
    """Reload the voice assistant system"""
    try:
        # Reinitialize components
        api.initialize_components()
        return jsonify({'success': True, 'message': 'System reloaded'})
        
    except Exception as e:
        logger.error(f"System reload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/shutdown', methods=['POST'])
def shutdown_system():
    """Shutdown the voice assistant"""
    try:
        api.is_running = False
        
        # Stop all components
        if api.wake_word:
            api.wake_word.stop_detection()
        
        logger.info("System shutdown initiated")
        
        # Shutdown Flask server
        threading.Timer(1.0, lambda: os._exit(0)).start()
        
        return jsonify({'success': True, 'message': 'System shutdown initiated'})
        
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/restart', methods=['POST'])
def restart_system():
    """Restart the voice assistant"""
    try:
        api.is_running = False
        
        # Stop all components
        if api.wake_word:
            api.wake_word.stop_detection()
        
        logger.info("System restart initiated")
        
        # Restart the application
        def restart():
            time.sleep(1)
            os.execv(sys.executable, ['python'] + sys.argv)
        
        threading.Timer(1.0, restart).start()
        
        return jsonify({'success': True, 'message': 'System restart initiated'})
        
    except Exception as e:
        logger.error(f"Restart error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Copy index.html to templates if it doesn't exist
    template_path = os.path.join(templates_dir, 'index.html')
    if not os.path.exists(template_path):
        original_path = os.path.join(os.path.dirname(__file__), 'index.html')
        if os.path.exists(original_path):
            import shutil
            shutil.copy2(original_path, template_path)
    
    print("🚀 Starting Lepida Voice Assistant Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🎤 Voice Assistant Frontend is ready!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
