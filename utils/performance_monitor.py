"""
Performance Monitor Module
Monitors system performance and resource usage for the voice assistant
"""

import logging
import time
import threading
import psutil
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor system performance and resource usage."""
    
    def __init__(self, config):
        """Initialize performance monitor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Monitoring configuration
        self.enabled = config.get('monitoring.enabled', True)
        self.interval = config.get('monitoring.interval', 30)  # seconds
        self.cpu_threshold = config.get('monitoring.cpu_threshold', 80)  # percent
        self.memory_threshold = config.get('monitoring.memory_threshold', 80)  # percent
        
        # State
        self.monitoring = False
        self.monitor_thread = None
        self.stats = {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
            'network_io': {'bytes_sent': 0, 'bytes_recv': 0},
            'process_memory': 0,
            'process_cpu': 0
        }
        
    def start_monitoring(self):
        """Start performance monitoring."""
        if not self.enabled or self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring."""
        if not self.monitoring:
            return
            
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        self.logger.info("Performance monitoring stopped")
        
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._update_stats()
                self._check_thresholds()
                time.sleep(self.interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                
    def _update_stats(self):
        """Update system statistics."""
        try:
            # System stats
            self.stats['cpu_usage'] = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            self.stats['memory_usage'] = memory.percent
            
            disk = psutil.disk_usage('/')
            self.stats['disk_usage'] = (disk.used / disk.total) * 100
            
            net_io = psutil.net_io_counters()
            self.stats['network_io'] = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv
            }
            
            # Process stats
            process = psutil.Process()
            self.stats['process_memory'] = process.memory_percent()
            self.stats['process_cpu'] = process.cpu_percent()
            
        except Exception as e:
            self.logger.error(f"Error updating stats: {e}")
            
    def _check_thresholds(self):
        """Check if any thresholds are exceeded."""
        if self.stats['cpu_usage'] > self.cpu_threshold:
            self.logger.warning(f"High CPU usage: {self.stats['cpu_usage']:.1f}%")
            
        if self.stats['memory_usage'] > self.memory_threshold:
            self.logger.warning(f"High memory usage: {self.stats['memory_usage']:.1f}%")
            
    def get_stats(self):
        """Get current performance statistics."""
        return self.stats.copy()
        
    def get_system_info(self):
        """Get detailed system information."""
        try:
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu': {
                    'cores': cpu_count,
                    'frequency': cpu_freq.current if cpu_freq else 'Unknown',
                    'usage': psutil.cpu_percent(interval=1)
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': psutil.net_io_counters()._asdict()
            }
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {}

class AudioDeviceMonitor:
    """Monitor audio device status and availability."""
    
    def __init__(self, config):
        """Initialize audio device monitor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Try to import pyaudio for device monitoring
        try:
            import pyaudio
            self.audio = pyaudio.PyAudio()
            self.available = True
        except ImportError:
            self.logger.warning("PyAudio not available - audio device monitoring disabled")
            self.audio = None
            self.available = False
            
    def get_audio_devices(self):
        """Get list of available audio devices."""
        if not self.available:
            return []
            
        devices = []
        try:
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'max_input_channels': device_info['maxInputChannels'],
                    'max_output_channels': device_info['maxOutputChannels'],
                    'default_sample_rate': device_info['defaultSampleRate']
                })
        except Exception as e:
            self.logger.error(f"Error getting audio devices: {e}")
            
        return devices
        
    def get_default_devices(self):
        """Get default input and output devices."""
        if not self.available:
            return {'input': None, 'output': None}
            
        try:
            default_input = self.audio.get_default_input_device_info()
            default_output = self.audio.get_default_output_device_info()
            
            return {
                'input': {
                    'index': default_input['index'],
                    'name': default_input['name']
                },
                'output': {
                    'index': default_output['index'],
                    'name': default_output['name']
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting default devices: {e}")
            return {'input': None, 'output': None}
            
    def test_device(self, device_index, is_input=True):
        """Test if an audio device is working."""
        if not self.available:
            return False
            
        try:
            if is_input:
                # Test input device
                stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=1024
                )
                # Try to read a small amount of data
                data = stream.read(1024, exception_on_overflow=False)
                stream.stop_stream()
                stream.close()
                return len(data) > 0
            else:
                # Test output device  
                stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True,
                    output_device_index=device_index,
                    frames_per_buffer=1024
                )
                # Write silence to test
                silence = b'\x00' * 2048
                stream.write(silence)
                stream.stop_stream()
                stream.close()
                return True
                
        except Exception as e:
            self.logger.error(f"Error testing device {device_index}: {e}")
            return False
            
    def cleanup(self):
        """Cleanup audio resources."""
        if self.audio:
            self.audio.terminate()
