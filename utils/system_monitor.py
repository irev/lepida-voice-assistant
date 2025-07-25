#!/usr/bin/env python3
"""
System Monitor for Lepida Voice Assistant
Monitors system resources including CPU, memory, disk, and network usage
"""

import logging
import psutil
import time
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SystemMonitor:
    """
    System resource monitor for voice assistant.
    Tracks CPU, memory, disk, and network usage.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize system monitor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Monitoring settings
        self.monitor_interval = self.config.get('monitor_interval', 5.0)  # seconds
        self.history_limit = self.config.get('history_limit', 100)  # number of readings
        
        # Data storage
        self.cpu_history = []
        self.memory_history = []
        self.disk_history = []
        self.network_history = []
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        
        # Thresholds for alerts
        self.cpu_threshold = self.config.get('cpu_threshold', 80.0)  # %
        self.memory_threshold = self.config.get('memory_threshold', 85.0)  # %
        self.disk_threshold = self.config.get('disk_threshold', 90.0)  # %
        
        self.logger.info("SystemMonitor initialized")
    
    def get_current_stats(self) -> Dict[str, Any]:
        """
        Get current system statistics.
        
        Returns:
            Dictionary containing current system stats
        """
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory usage
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network stats
            network = psutil.net_io_counters()
            
            # System info
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'frequency': {
                        'current': cpu_freq.current if cpu_freq else None,
                        'min': cpu_freq.min if cpu_freq else None,
                        'max': cpu_freq.max if cpu_freq else None
                    }
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percent': memory.percent,
                    'free': memory.free
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'free': swap.free,
                    'percent': swap.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100 if disk.total > 0 else 0
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'system': {
                    'boot_time': boot_time.isoformat(),
                    'uptime_seconds': uptime.total_seconds(),
                    'uptime_string': str(uptime).split('.')[0]  # Remove microseconds
                }
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting system stats: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def start_monitoring(self):
        """Start continuous monitoring in background thread."""
        if self.monitoring:
            self.logger.warning("Monitoring already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("System monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        self.logger.info("System monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop running in background thread."""
        while self.monitoring:
            try:
                stats = self.get_current_stats()
                
                if 'error' not in stats:
                    # Store in history
                    self._add_to_history(stats)
                    
                    # Check for alerts
                    self._check_alerts(stats)
                
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitor_interval)
    
    def _add_to_history(self, stats: Dict[str, Any]):
        """Add stats to history and maintain size limit."""
        # Add to histories
        self.cpu_history.append({
            'timestamp': stats['timestamp'],
            'percent': stats['cpu']['percent']
        })
        
        self.memory_history.append({
            'timestamp': stats['timestamp'],
            'percent': stats['memory']['percent']
        })
        
        self.disk_history.append({
            'timestamp': stats['timestamp'],
            'percent': stats['disk']['percent']
        })
        
        if 'network' in stats:
            self.network_history.append({
                'timestamp': stats['timestamp'],
                'bytes_sent': stats['network']['bytes_sent'],
                'bytes_recv': stats['network']['bytes_recv']
            })
        
        # Trim histories to maintain size limit
        self.cpu_history = self.cpu_history[-self.history_limit:]
        self.memory_history = self.memory_history[-self.history_limit:]
        self.disk_history = self.disk_history[-self.history_limit:]
        self.network_history = self.network_history[-self.history_limit:]
    
    def _check_alerts(self, stats: Dict[str, Any]):
        """Check for system alerts based on thresholds."""
        alerts = []
        
        # Check CPU
        if stats['cpu']['percent'] > self.cpu_threshold:
            alerts.append(f"High CPU usage: {stats['cpu']['percent']:.1f}%")
        
        # Check Memory
        if stats['memory']['percent'] > self.memory_threshold:
            alerts.append(f"High memory usage: {stats['memory']['percent']:.1f}%")
        
        # Check Disk
        if stats['disk']['percent'] > self.disk_threshold:
            alerts.append(f"High disk usage: {stats['disk']['percent']:.1f}%")
        
        # Log alerts
        for alert in alerts:
            self.logger.warning(f"System Alert: {alert}")
    
    def get_history(self, metric: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get historical data for a specific metric.
        
        Args:
            metric: Metric name ('cpu', 'memory', 'disk', 'network')
            limit: Maximum number of records to return
            
        Returns:
            List of historical data points
        """
        history_map = {
            'cpu': self.cpu_history,
            'memory': self.memory_history,
            'disk': self.disk_history,
            'network': self.network_history
        }
        
        history = history_map.get(metric, [])
        
        if limit:
            return history[-limit:]
        return history
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of system status.
        
        Returns:
            Summary dictionary
        """
        current_stats = self.get_current_stats()
        
        if 'error' in current_stats:
            return current_stats
        
        # Calculate averages if we have history
        cpu_avg = None
        memory_avg = None
        disk_current = current_stats['disk']['percent']
        
        if self.cpu_history:
            cpu_avg = sum(h['percent'] for h in self.cpu_history[-10:]) / len(self.cpu_history[-10:])
        
        if self.memory_history:
            memory_avg = sum(h['percent'] for h in self.memory_history[-10:]) / len(self.memory_history[-10:])
        
        # Determine system health
        health_score = 100
        warnings = []
        
        if current_stats['cpu']['percent'] > self.cpu_threshold:
            health_score -= 30
            warnings.append("High CPU usage")
        
        if current_stats['memory']['percent'] > self.memory_threshold:
            health_score -= 25
            warnings.append("High memory usage")
        
        if disk_current > self.disk_threshold:
            health_score -= 25
            warnings.append("High disk usage")
        
        health_status = 'excellent' if health_score >= 90 else \
                       'good' if health_score >= 70 else \
                       'fair' if health_score >= 50 else 'poor'
        
        return {
            'timestamp': current_stats['timestamp'],
            'health': {
                'score': max(0, health_score),
                'status': health_status,
                'warnings': warnings
            },
            'current': {
                'cpu_percent': current_stats['cpu']['percent'],
                'memory_percent': current_stats['memory']['percent'],
                'disk_percent': disk_current,
                'uptime': current_stats['system']['uptime_string']
            },
            'averages': {
                'cpu_percent': cpu_avg,
                'memory_percent': memory_avg
            },
            'monitoring': {
                'active': self.monitoring,
                'interval': self.monitor_interval,
                'history_size': len(self.cpu_history)
            }
        }
    
    def format_bytes(self, bytes_value: float) -> str:
        """
        Format bytes to human readable format.
        
        Args:
            bytes_value: Value in bytes
            
        Returns:
            Formatted string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"


def main():
    """Test the system monitor."""
    import json
    
    monitor = SystemMonitor()
    
    print("🖥️  System Monitor Test")
    print("=" * 50)
    
    # Get current stats
    print("\n📊 Current System Stats:")
    stats = monitor.get_current_stats()
    print(json.dumps(stats, indent=2, default=str))
    
    # Get summary
    print("\n📋 System Summary:")
    summary = monitor.get_summary()
    print(json.dumps(summary, indent=2, default=str))
    
    # Test monitoring for a short time
    print("\n⏱️  Starting monitoring for 10 seconds...")
    monitor.start_monitoring()
    time.sleep(10)
    monitor.stop_monitoring()
    
    print("\n📈 CPU History (last 5 readings):")
    cpu_history = monitor.get_history('cpu', 5)
    for entry in cpu_history:
        print(f"  {entry['timestamp']}: {entry['percent']:.1f}%")


if __name__ == "__main__":
    main()
