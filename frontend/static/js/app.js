// Lepida Voice Assistant Frontend JavaScript
class VoiceAssistant {
    constructor() {
        this.isConnected = false;
        this.isRecording = false;
        this.audioRecorder = null;
        this.mediaStream = null;
        this.currentSection = 'dashboard';
        this.config = {};
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.initNavigation();
        await this.loadConfig();
        await this.checkConnection();
        this.updateSystemInfo();
        this.startPerformanceMonitoring();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.getAttribute('data-section');
                this.showSection(section);
            });
        });

        // Form submissions
        document.getElementById('testTtsForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.testTTS();
        });

        // Audio controls
        document.getElementById('recordButton').addEventListener('click', () => {
            this.toggleRecording();
        });

        document.getElementById('testAudioButton').addEventListener('click', () => {
            this.testAudio();
        });

        // Wake word controls
        document.getElementById('startWakeWord').addEventListener('click', () => {
            this.startWakeWordDetection();
        });

        document.getElementById('stopWakeWord').addEventListener('click', () => {
            this.stopWakeWordDetection();
        });

        // System controls
        document.getElementById('reloadButton').addEventListener('click', () => {
            this.reloadSystem();
        });

        document.getElementById('shutdownButton').addEventListener('click', () => {
            this.shutdownSystem();
        });

        document.getElementById('restartButton').addEventListener('click', () => {
            this.restartSystem();
        });

        // Settings change handlers
        this.setupSettingsHandlers();
    }

    setupSettingsHandlers() {
        // Audio settings
        document.getElementById('volumeSlider').addEventListener('input', (e) => {
            this.updateVolumeDisplay(e.target.value);
            this.updateSetting('audio.volume', e.target.value);
        });

        document.getElementById('micGainSlider').addEventListener('input', (e) => {
            this.updateMicGainDisplay(e.target.value);
            this.updateSetting('audio.microphone_gain', e.target.value);
        });

        // TTS settings
        document.getElementById('ttsEngine').addEventListener('change', (e) => {
            this.updateSetting('tts.engine', e.target.value);
        });

        document.getElementById('ttsLanguage').addEventListener('change', (e) => {
            this.updateSetting('tts.language', e.target.value);
        });

        document.getElementById('ttsSpeed').addEventListener('input', (e) => {
            this.updateTtsSpeedDisplay(e.target.value);
            this.updateSetting('tts.speed', e.target.value);
        });

        // STT settings
        document.getElementById('sttEngine').addEventListener('change', (e) => {
            this.updateSetting('stt.engine', e.target.value);
        });

        document.getElementById('sttLanguage').addEventListener('change', (e) => {
            this.updateSetting('stt.language', e.target.value);
        });

        // Wake word settings
        document.getElementById('wakeWordEngine').addEventListener('change', (e) => {
            this.updateSetting('wake_word.engine', e.target.value);
        });

        document.getElementById('wakeWordSensitivity').addEventListener('input', (e) => {
            this.updateWakeWordSensitivityDisplay(e.target.value);
            this.updateSetting('wake_word.sensitivity', e.target.value);
        });
    }

    initNavigation() {
        // Show dashboard by default
        this.showSection('dashboard');
    }

    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Remove active class from nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        // Show selected section
        const selectedSection = document.getElementById(sectionName);
        if (selectedSection) {
            selectedSection.classList.add('active');
        }

        // Add active class to nav link
        const selectedNavLink = document.querySelector(`[data-section="${sectionName}"]`);
        if (selectedNavLink) {
            selectedNavLink.classList.add('active');
        }

        this.currentSection = sectionName;
    }

    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            this.config = await response.json();
            this.populateSettings();
        } catch (error) {
            console.error('Failed to load config:', error);
            this.logToConsole('error', 'Failed to load configuration');
        }
    }

    populateSettings() {
        if (!this.config) return;

        // Audio settings
        const volumeSlider = document.getElementById('volumeSlider');
        if (volumeSlider && this.config.audio?.volume !== undefined) {
            volumeSlider.value = this.config.audio.volume;
            this.updateVolumeDisplay(this.config.audio.volume);
        }

        const micGainSlider = document.getElementById('micGainSlider');
        if (micGainSlider && this.config.audio?.microphone_gain !== undefined) {
            micGainSlider.value = this.config.audio.microphone_gain;
            this.updateMicGainDisplay(this.config.audio.microphone_gain);
        }

        // TTS settings
        this.setSelectValue('ttsEngine', this.config.tts?.engine);
        this.setSelectValue('ttsLanguage', this.config.tts?.language);
        
        const ttsSpeed = document.getElementById('ttsSpeed');
        if (ttsSpeed && this.config.tts?.speed !== undefined) {
            ttsSpeed.value = this.config.tts.speed;
            this.updateTtsSpeedDisplay(this.config.tts.speed);
        }

        // STT settings
        this.setSelectValue('sttEngine', this.config.stt?.engine);
        this.setSelectValue('sttLanguage', this.config.stt?.language);

        // Wake word settings
        this.setSelectValue('wakeWordEngine', this.config.wake_word?.engine);
        
        const wakeWordSensitivity = document.getElementById('wakeWordSensitivity');
        if (wakeWordSensitivity && this.config.wake_word?.sensitivity !== undefined) {
            wakeWordSensitivity.value = this.config.wake_word.sensitivity;
            this.updateWakeWordSensitivityDisplay(this.config.wake_word.sensitivity);
        }
    }

    setSelectValue(elementId, value) {
        const element = document.getElementById(elementId);
        if (element && value) {
            element.value = value;
        }
    }

    // Display update functions
    updateVolumeDisplay(value) {
        document.getElementById('volumeValue').textContent = `${value}%`;
    }

    updateMicGainDisplay(value) {
        document.getElementById('micGainValue').textContent = `${value}`;
    }

    updateTtsSpeedDisplay(value) {
        document.getElementById('ttsSpeedValue').textContent = `${value}x`;
    }

    updateWakeWordSensitivityDisplay(value) {
        document.getElementById('wakeWordSensitivityValue').textContent = value;
    }

    async checkConnection() {
        try {
            const response = await fetch('/api/status');
            if (response.ok) {
                this.isConnected = true;
                this.updateConnectionStatus(true);
                this.logToConsole('success', 'Connected to voice assistant backend');
            } else {
                throw new Error('Backend not responding');
            }
        } catch (error) {
            this.isConnected = false;
            this.updateConnectionStatus(false);
            this.logToConsole('error', 'Failed to connect to backend');
        }
    }

    updateConnectionStatus(connected) {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        
        if (statusDot) {
            statusDot.classList.toggle('disconnected', !connected);
        }
        
        if (statusText) {
            statusText.textContent = connected ? 'Connected' : 'Disconnected';
        }
    }

    async updateSystemInfo() {
        try {
            const response = await fetch('/api/system/info');
            if (response.ok) {
                const data = await response.json();
                this.updateSystemInfoDisplay(data);
            }
        } catch (error) {
            console.error('Failed to fetch system info:', error);
        }
    }

    updateSystemInfoDisplay(data) {
        const updateElement = (id, value) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value || 'N/A';
        };

        updateElement('systemCpu', `${data.cpu_usage || 0}%`);
        updateElement('systemMemory', `${data.memory_usage || 0}%`);
        updateElement('systemDisk', `${data.disk_usage || 0}%`);
        updateElement('systemUptime', data.uptime || 'N/A');
        updateElement('assistantVersion', data.version || 'N/A');
        updateElement('pythonVersion', data.python_version || 'N/A');
    }

    startPerformanceMonitoring() {
        setInterval(async () => {
            if (this.currentSection === 'dashboard') {
                await this.updatePerformanceData();
            }
        }, 5000);
    }

    async updatePerformanceData() {
        try {
            const response = await fetch('/api/system/performance');
            if (response.ok) {
                const data = await response.json();
                this.updatePerformanceBars(data);
            }
        } catch (error) {
            console.error('Failed to fetch performance data:', error);
        }
    }

    updatePerformanceBars(data) {
        const updateProgressBar = (id, value) => {
            const element = document.getElementById(id);
            if (element) {
                element.style.width = `${value || 0}%`;
            }
        };

        updateProgressBar('cpuProgress', data.cpu_usage);
        updateProgressBar('memoryProgress', data.memory_usage);
        updateProgressBar('diskProgress', data.disk_usage);
    }

    async testTTS() {
        const text = document.getElementById('testText').value;
        if (!text.trim()) {
            this.logToConsole('warning', 'Please enter text to test TTS');
            return;
        }

        try {
            this.logToConsole('info', `Testing TTS with text: "${text}"`);
            
            const response = await fetch('/api/tts/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (response.ok) {
                this.logToConsole('success', 'TTS test completed successfully');
            } else {
                this.logToConsole('error', 'TTS test failed');
            }
        } catch (error) {
            this.logToConsole('error', `TTS test error: ${error.message}`);
        }
    }

    async toggleRecording() {
        if (this.isRecording) {
            await this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.audioRecorder = new MediaRecorder(this.mediaStream);
            
            this.audioRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.sendAudioForTranscription(event.data);
                }
            };

            this.audioRecorder.start();
            this.isRecording = true;
            
            document.getElementById('recordButton').textContent = '⏹️ Stop Recording';
            document.getElementById('recordingStatus').style.display = 'flex';
            
            this.logToConsole('info', 'Started audio recording');
        } catch (error) {
            this.logToConsole('error', `Failed to start recording: ${error.message}`);
        }
    }

    async stopRecording() {
        if (this.audioRecorder) {
            this.audioRecorder.stop();
            this.audioRecorder = null;
        }
        
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
        }

        this.isRecording = false;
        document.getElementById('recordButton').textContent = '🎤 Start Recording';
        document.getElementById('recordingStatus').style.display = 'none';
        
        this.logToConsole('info', 'Stopped audio recording');
    }

    async sendAudioForTranscription(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');

            const response = await fetch('/api/stt/transcribe', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                document.getElementById('sttResult').textContent = result.text || 'No transcription available';
                this.logToConsole('success', `Transcription: ${result.text}`);
            } else {
                this.logToConsole('error', 'Failed to transcribe audio');
            }
        } catch (error) {
            this.logToConsole('error', `Transcription error: ${error.message}`);
        }
    }

    async testAudio() {
        try {
            this.logToConsole('info', 'Testing audio system...');
            
            const response = await fetch('/api/audio/test', {
                method: 'POST'
            });

            if (response.ok) {
                this.logToConsole('success', 'Audio test completed successfully');
            } else {
                this.logToConsole('error', 'Audio test failed');
            }
        } catch (error) {
            this.logToConsole('error', `Audio test error: ${error.message}`);
        }
    }

    async startWakeWordDetection() {
        try {
            const response = await fetch('/api/wakeword/start', {
                method: 'POST'
            });

            if (response.ok) {
                document.getElementById('wakeWordStatus').textContent = 'Wake word detection is active. Say the wake word to test...';
                this.logToConsole('success', 'Wake word detection started');
            } else {
                this.logToConsole('error', 'Failed to start wake word detection');
            }
        } catch (error) {
            this.logToConsole('error', `Wake word start error: ${error.message}`);
        }
    }

    async stopWakeWordDetection() {
        try {
            const response = await fetch('/api/wakeword/stop', {
                method: 'POST'
            });

            if (response.ok) {
                document.getElementById('wakeWordStatus').textContent = 'Wake word detection is stopped.';
                this.logToConsole('success', 'Wake word detection stopped');
            } else {
                this.logToConsole('error', 'Failed to stop wake word detection');
            }
        } catch (error) {
            this.logToConsole('error', `Wake word stop error: ${error.message}`);
        }
    }

    async updateSetting(key, value) {
        try {
            const response = await fetch('/api/config/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    key: key,
                    value: value
                })
            });

            if (response.ok) {
                this.logToConsole('info', `Updated setting: ${key} = ${value}`);
            } else {
                this.logToConsole('error', `Failed to update setting: ${key}`);
            }
        } catch (error) {
            this.logToConsole('error', `Setting update error: ${error.message}`);
        }
    }

    async reloadSystem() {
        try {
            this.logToConsole('info', 'Reloading voice assistant system...');
            
            const response = await fetch('/api/system/reload', {
                method: 'POST'
            });

            if (response.ok) {
                this.logToConsole('success', 'System reloaded successfully');
                setTimeout(() => {
                    this.checkConnection();
                    this.loadConfig();
                }, 2000);
            } else {
                this.logToConsole('error', 'Failed to reload system');
            }
        } catch (error) {
            this.logToConsole('error', `System reload error: ${error.message}`);
        }
    }

    async shutdownSystem() {
        if (confirm('Are you sure you want to shutdown the voice assistant?')) {
            try {
                this.logToConsole('warning', 'Shutting down voice assistant...');
                
                const response = await fetch('/api/system/shutdown', {
                    method: 'POST'
                });

                if (response.ok) {
                    this.logToConsole('warning', 'System shutdown initiated');
                    this.updateConnectionStatus(false);
                } else {
                    this.logToConsole('error', 'Failed to shutdown system');
                }
            } catch (error) {
                this.logToConsole('error', `Shutdown error: ${error.message}`);
            }
        }
    }

    async restartSystem() {
        if (confirm('Are you sure you want to restart the voice assistant?')) {
            try {
                this.logToConsole('warning', 'Restarting voice assistant...');
                
                const response = await fetch('/api/system/restart', {
                    method: 'POST'
                });

                if (response.ok) {
                    this.logToConsole('warning', 'System restart initiated');
                    this.updateConnectionStatus(false);
                    
                    // Try to reconnect after restart
                    setTimeout(() => {
                        this.checkConnection();
                    }, 10000);
                } else {
                    this.logToConsole('error', 'Failed to restart system');
                }
            } catch (error) {
                this.logToConsole('error', `Restart error: ${error.message}`);
            }
        }
    }

    logToConsole(level, message) {
        const console = document.getElementById('consoleContent');
        if (!console) return;

        const timestamp = new Date().toLocaleTimeString();
        const logLine = document.createElement('div');
        logLine.className = `console-line ${level}`;
        logLine.textContent = `[${timestamp}] ${message}`;
        
        console.appendChild(logLine);
        console.scrollTop = console.scrollHeight;

        // Keep only last 100 lines
        while (console.children.length > 100) {
            console.removeChild(console.firstChild);
        }
    }

    clearConsole() {
        const console = document.getElementById('consoleContent');
        if (console) {
            console.innerHTML = '';
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.voiceAssistant = new VoiceAssistant();
});

// Console control functions
function clearConsole() {
    if (window.voiceAssistant) {
        window.voiceAssistant.clearConsole();
    }
}
