# Lepida Voice Assistant Frontend

Antarmuka web untuk mengelola dan mengontrol Lepida Voice Assistant.

## 🌟 Fitur Frontend

### 📊 Dashboard
- **Status Sistem Real-time**: Monitoring CPU, Memory, Disk usage
- **Informasi Sistem**: Versi aplikasi, Python version, uptime
- **Status Koneksi**: Indikator koneksi ke backend voice assistant
- **Performance Monitoring**: Grafik real-time untuk monitoring performa

### 🎤 Audio Management
- **Volume Control**: Slider untuk mengatur volume output
- **Microphone Gain**: Pengaturan gain mikrophone
- **Audio Testing**: Tombol test untuk sistem audio
- **Live Recording**: Fitur record dan test STT secara real-time

### 🗣️ Text-to-Speech (TTS)
- **Engine Selection**: Pilihan TTS engine (MMS TTS, Coqui, Piper)
- **Language Settings**: Pengaturan bahasa untuk TTS
- **Speed Control**: Kontrol kecepatan bicara
- **Test Interface**: Input teks untuk testing TTS

### 👂 Speech-to-Text (STT)
- **Engine Selection**: Pilihan STT engine (Whisper, Google STT)
- **Language Settings**: Pengaturan bahasa untuk STT
- **Live Transcription**: Real-time transcription dari mikrophone
- **Audio Upload**: Upload file audio untuk transcription

### 🎯 Wake Word Detection
- **Engine Selection**: Pilihan wake word engine (Porcupine)
- **Sensitivity Control**: Pengaturan sensitivitas wake word
- **Start/Stop Control**: Kontrol aktivasi wake word detection
- **Status Monitoring**: Monitor status wake word detection

### ⚙️ System Administration
- **Configuration Management**: Edit dan simpan konfigurasi sistem
- **Plugin Management**: Monitor status dan validasi plugin
- **System Control**: Reload, restart, shutdown sistem
- **Log Console**: Real-time system logs dan aktivitas

## 🚀 Instalasi dan Setup

### Prerequisites
```bash
# Install Python dependencies untuk frontend
pip install -r frontend/requirements.txt
```

### Menjalankan Frontend

#### Development Mode
```bash
cd frontend
python app.py
```

#### Production Mode
```bash
cd frontend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Access Web Interface
- **Local**: http://localhost:5000
- **Network**: http://[IP_ADDRESS]:5000

## 📁 Struktur Frontend

```
frontend/
├── app.py                      # Flask web server dan API endpoints
├── requirements.txt            # Dependencies untuk frontend
├── README.md                   # Dokumentasi frontend
├── templates/
│   └── index.html             # Template HTML utama
├── static/
│   ├── css/
│   │   └── style.css          # Styling untuk web interface
│   └── js/
│       └── app.js             # JavaScript untuk interaktivitas
└── temp/                      # Temporary files untuk upload audio
```

## 🔌 API Endpoints

### System Status
- `GET /api/status` - Status sistem dan komponen
- `GET /api/system/info` - Informasi sistem detail
- `GET /api/system/performance` - Data performa real-time

### Configuration
- `GET /api/config` - Ambil konfigurasi current
- `POST /api/config/update` - Update setting konfigurasi

### Text-to-Speech
- `POST /api/tts/test` - Test TTS dengan teks

### Speech-to-Text
- `POST /api/stt/transcribe` - Upload dan transkripsi audio

### Audio System
- `POST /api/audio/test` - Test sistem audio

### Wake Word
- `POST /api/wakeword/start` - Start wake word detection
- `POST /api/wakeword/stop` - Stop wake word detection

### System Control
- `POST /api/system/reload` - Reload sistem
- `POST /api/system/restart` - Restart aplikasi
- `POST /api/system/shutdown` - Shutdown aplikasi

## 🎨 UI Features

### Modern Design
- **Responsive Layout**: Mendukung desktop, tablet, dan mobile
- **Dark Mode Support**: Otomatis mengikuti sistem preference
- **Interactive Elements**: Hover effects, transitions, animations
- **Real-time Updates**: Live data updates tanpa refresh

### User Experience
- **Intuitive Navigation**: Tab-based navigation yang mudah
- **Visual Feedback**: Status indicators, progress bars, notifications
- **Error Handling**: User-friendly error messages
- **Console Integration**: Real-time logs dan system feedback

### Performance
- **Optimized Assets**: Compressed CSS dan JS
- **Lazy Loading**: Load data sesuai kebutuhan
- **Caching**: Browser caching untuk assets statis
- **Minimal Dependencies**: Hanya dependencies yang diperlukan

## 🔧 Customization

### Styling
Edit `static/css/style.css` untuk mengubah tampilan:
- Color scheme dan branding
- Layout dan spacing
- Typography dan fonts
- Responsive breakpoints

### Functionality
Edit `static/js/app.js` untuk menambah fitur:
- API endpoints baru
- Interactive features
- Real-time updates
- Custom validations

### Backend Integration
Edit `app.py` untuk API endpoints:
- Route handlers baru
- Data processing
- Error handling
- System integration

## 🛡️ Security

### Development
- CORS enabled untuk development
- Debug mode untuk development

### Production
- Disable debug mode
- Configure proper CORS origins
- Use HTTPS dengan SSL certificates
- Implement rate limiting

## 📱 Mobile Support

Frontend fully responsive dan mendukung:
- **Touch Interface**: Optimized untuk touch devices
- **Mobile Navigation**: Collapsible menu untuk mobile
- **Responsive Grid**: Auto-adjust layout untuk screen size
- **Performance Optimized**: Fast loading untuk mobile connections

## 🔄 Real-time Features

- **WebSocket Support**: Ready untuk real-time communication
- **Auto-refresh**: Otomatis update data sistem
- **Live Monitoring**: Real-time performance monitoring
- **Event Notifications**: Instant feedback untuk user actions

## 🎯 Use Cases

1. **Development Testing**: Quick testing TTS, STT, dan audio features
2. **System Monitoring**: Monitor performa dan health sistem
3. **Configuration Management**: Easy configuration tanpa edit file
4. **Remote Management**: Control voice assistant dari web browser
5. **Debugging**: Real-time logs dan system diagnostics
