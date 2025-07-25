"""
Wake Word Detection System
Manages wake word detection and activation
"""

import logging
import threading
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class WakeWordDetector:
    """Wake word detection manager."""
    
    def __init__(self, config):
        """
        Initialize wake word detector.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.enabled = config.get('wakeword.enabled', True)
        self.primary_engine = config.get('wakeword.primary_engine', 'porcupine')
        self.keywords = config.get('wakeword.keywords', ['hey assistant'])
        self.sensitivity = config.get('wakeword.sensitivity', 0.5)
        
        # State
        self.is_listening = False
        self.detection_callback = None
        self.engine = None
        
        # Load detection engine
        if self.enabled:
            self._load_engine()
    
    def _load_engine(self):
        """Load wake word detection engine."""
        try:
            if self.primary_engine == 'porcupine':
                from plugins.wakeword_porcupine import initialize, start_listening, stop_listening
                self.engine = {
                    'initialize': initialize,
                    'start_listening': start_listening,
                    'stop_listening': stop_listening
                }
                self.logger.info("Loaded Porcupine wake word engine")
            else:
                self.logger.warning(f"Unknown wake word engine: {self.primary_engine}")
                
        except ImportError as e:
            self.logger.warning(f"Failed to load wake word engine: {e}")
            self.enabled = False
    
    def start_detection(self, callback=None):
        """
        Start wake word detection.
        
        Args:
            callback (function): Function to call when wake word is detected
        """
        if not self.enabled or not self.engine:
            self.logger.warning("Wake word detection not available")
            return False
        
        try:
            self.detection_callback = callback
            
            # Initialize engine
            if 'initialize' in self.engine:
                self.engine['initialize'](
                    keywords=self.keywords,
                    sensitivity=self.sensitivity
                )
            
            # Start listening
            if 'start_listening' in self.engine:
                self.engine['start_listening'](self._on_wake_word_detected)
            
            self.is_listening = True
            self.logger.info(f"Wake word detection started with keywords: {self.keywords}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start wake word detection: {e}")
            return False
    
    def stop_detection(self):
        """Stop wake word detection."""
        if not self.is_listening or not self.engine:
            return
        
        try:
            if 'stop_listening' in self.engine:
                self.engine['stop_listening']()
            
            self.is_listening = False
            self.logger.info("Wake word detection stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop wake word detection: {e}")
    
    def _on_wake_word_detected(self, keyword_index):
        """Handle wake word detection."""
        try:
            keyword = self.keywords[keyword_index] if keyword_index < len(self.keywords) else "unknown"
            self.logger.info(f"Wake word detected: {keyword}")
            
            if self.detection_callback:
                self.detection_callback(keyword, keyword_index)
                
        except Exception as e:
            self.logger.error(f"Error handling wake word detection: {e}")
    
    def add_keyword(self, keyword):
        """Add a new wake word keyword."""
        if keyword not in self.keywords:
            self.keywords.append(keyword)
            self.logger.info(f"Added wake word: {keyword}")
            
            # Restart detection if currently active
            if self.is_listening:
                self.stop_detection()
                self.start_detection(self.detection_callback)
    
    def remove_keyword(self, keyword):
        """Remove a wake word keyword."""
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.logger.info(f"Removed wake word: {keyword}")
            
            # Restart detection if currently active
            if self.is_listening:
                self.stop_detection()
                self.start_detection(self.detection_callback)
    
    def set_sensitivity(self, sensitivity):
        """Set wake word detection sensitivity."""
        self.sensitivity = max(0.0, min(1.0, sensitivity))
        self.logger.info(f"Wake word sensitivity set to: {self.sensitivity}")
        
        # Restart detection if currently active
        if self.is_listening:
            self.stop_detection()
            self.start_detection(self.detection_callback)
    
    def get_status(self):
        """Get current status of wake word detection."""
        return {
            'enabled': self.enabled,
            'listening': self.is_listening,
            'engine': self.primary_engine,
            'keywords': self.keywords,
            'sensitivity': self.sensitivity
        }

class SimpleWakeWordDetector:
    """Simple fallback wake word detector using basic audio analysis."""
    
    def __init__(self, keywords=None, threshold=0.8):
        """
        Initialize simple wake word detector.
        
        Args:
            keywords (list): List of wake words
            threshold (float): Detection threshold
        """
        self.keywords = keywords or ['hey assistant', 'halo asisten']
        self.threshold = threshold
        self.is_listening = False
        self.callback = None
        self.logger = logging.getLogger(__name__)
    
    def start_listening(self, callback=None):
        """Start simple wake word detection."""
        self.callback = callback
        self.is_listening = True
        
        # Start listening thread
        listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        listen_thread.start()
        
        self.logger.info("Simple wake word detection started")
    
    def stop_listening(self):
        """Stop wake word detection."""
        self.is_listening = False
        self.logger.info("Simple wake word detection stopped")
    
    def _listen_loop(self):
        """Simple listening loop using STT."""
        try:
            # This would need integration with STT system
            # For now, just log that it's running
            while self.is_listening:
                # In a real implementation, this would:
                # 1. Record short audio chunks
                # 2. Use STT to convert to text
                # 3. Check if text contains wake words
                # 4. Call callback if detected
                
                time.sleep(1)  # Placeholder
                
        except Exception as e:
            self.logger.error(f"Simple wake word detection error: {e}")
    
    def get_info(self):
        """Get detector information."""
        return {
            "name": "Simple Wake Word Detector",
            "description": "Basic wake word detection using STT",
            "keywords": self.keywords,
            "threshold": self.threshold
        }


# Alias for compatibility with tests
WakeWordDetection = WakeWordDetector
