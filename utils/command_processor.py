"""
Voice Command Processor
Handles voice commands and responses for the assistant
"""

import logging
import re
import datetime
import random
from pathlib import Path

logger = logging.getLogger(__name__)

class VoiceCommandProcessor:
    """Processes voice commands and generates appropriate responses."""
    
    def __init__(self, config, tts, stt=None):
        """
        Initialize command processor.
        
        Args:
            config: Configuration object
            tts: Text-to-speech instance
            stt: Speech-to-text instance (optional)
        """
        self.config = config
        self.tts = tts
        self.stt = stt
        self.logger = logging.getLogger(__name__)
        
        # Command patterns
        self.command_patterns = {
            'greeting': [
                r'halo|hai|hello|selamat.*pagi|selamat.*siang|selamat.*sore|selamat.*malam',
                r'apa.*kabar|how.*are.*you'
            ],
            'time': [
                r'jam.*berapa|what.*time|waktu.*sekarang',
                r'tanggal.*berapa|what.*date|hari.*ini'
            ],
            'weather': [
                r'cuaca.*hari.*ini|weather.*today|bagaimana.*cuaca',
                r'hujan.*tidak|will.*it.*rain'
            ],
            'music': [
                r'putar.*musik|play.*music|nyalakan.*musik',
                r'stop.*musik|stop.*music|matikan.*musik'
            ],
            'news': [
                r'berita.*terbaru|latest.*news|kabar.*terbaru',
                r'apa.*yang.*terjadi|what.*happening'
            ],
            'calculation': [
                r'hitung|calculate|berapa.*\+.*|berapa.*\-.*|berapa.*\*.*|berapa.*\/.*',
                r'\d+.*\+.*\d+|\d+.*\-.*\d+|\d+.*\*.*\d+|\d+.*\/.*\d+'
            ],
            'reminder': [
                r'ingatkan.*saya|remind.*me|set.*reminder',
                r'alarm.*untuk|set.*alarm'
            ],
            'help': [
                r'bantuan|help|apa.*yang.*bisa.*kamu.*lakukan',
                r'perintah.*apa.*saja|what.*can.*you.*do'
            ],
            'goodbye': [
                r'selamat.*tinggal|goodbye|bye|sampai.*jumpa',
                r'matikan|shutdown|exit|keluar'
            ]
        }
        
        # Response templates
        self.responses = {
            'greeting': [
                "Halo! Selamat datang. Ada yang bisa saya bantu?",
                "Hai! Saya siap membantu Anda hari ini.",
                "Selamat datang! Bagaimana kabar Anda?"
            ],
            'time': self._get_current_time,
            'weather': [
                "Maaf, saya belum terhubung dengan layanan cuaca. Coba periksa aplikasi cuaca Anda.",
                "Fitur cuaca sedang dalam pengembangan. Silakan cek cuaca melalui aplikasi lain."
            ],
            'music': [
                "Maaf, saya belum bisa memutar musik. Fitur ini akan segera tersedia.",
                "Kontrol musik belum tersedia. Gunakan aplikasi musik favorit Anda."
            ],
            'news': [
                "Maaf, saya belum terhubung dengan layanan berita. Coba buka aplikasi berita Anda.",
                "Fitur berita sedang dalam pengembangan."
            ],
            'calculation': self._handle_calculation,
            'reminder': [
                "Fitur pengingat sedang dalam pengembangan. Gunakan aplikasi pengingat lain untuk sementara.",
                "Maaf, saya belum bisa mengatur pengingat."
            ],
            'help': [
                "Saya bisa membantu dengan: memberikan waktu, perhitungan sederhana, dan percakapan dasar. Katakan 'bantuan' untuk mendengar ini lagi.",
                "Fitur yang tersedia: waktu, perhitungan, dan percakapan. Lebih banyak fitur akan segera ditambahkan."
            ],
            'goodbye': [
                "Sampai jumpa! Terima kasih telah menggunakan asisten suara.",
                "Selamat tinggal! Semoga hari Anda menyenangkan.",
                "Sampai bertemu lagi!"
            ],
            'unknown': [
                "Maaf, saya tidak mengerti perintah tersebut. Coba katakan 'bantuan' untuk melihat yang bisa saya lakukan.",
                "Saya belum memahami itu. Bisakah Anda mengulang dengan kata-kata yang berbeda?",
                "Perintah tidak dikenali. Katakan 'bantuan' untuk melihat daftar perintah."
            ]
        }
    
    def process_command(self, text):
        """
        Process voice command and return response.
        
        Args:
            text (str): Input text to process
            
        Returns:
            str: Response text
        """
        if not text or not text.strip():
            return "Maaf, saya tidak mendengar apa-apa."
        
        text = text.lower().strip()
        self.logger.info(f"Processing command: {text}")
        
        # Find matching command type
        command_type = self._classify_command(text)
        
        # Get response
        response = self._generate_response(command_type, text)
        
        self.logger.info(f"Command type: {command_type}, Response: {response[:50]}...")
        return response
    
    def _classify_command(self, text):
        """Classify the command type based on text patterns."""
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return command_type
        return 'unknown'
    
    def _generate_response(self, command_type, text):
        """Generate response for command type."""
        response_template = self.responses.get(command_type, self.responses['unknown'])
        
        # Handle function responses
        if callable(response_template):
            return response_template(text)
        
        # Handle list responses
        if isinstance(response_template, list):
            return random.choice(response_template)
        
        return str(response_template)
    
    def _get_current_time(self, text=None):
        """Get current time and date."""
        now = datetime.datetime.now()
        
        if 'tanggal' in text or 'date' in text:
            return f"Hari ini adalah {now.strftime('%A, %d %B %Y')}"
        else:
            return f"Sekarang pukul {now.strftime('%H:%M')} pada hari {now.strftime('%A, %d %B %Y')}"
    
    def _handle_calculation(self, text):
        """Handle simple calculations."""
        try:
            # Extract numbers and operators
            calculation_match = re.search(r'(\d+\.?\d*)\s*([\+\-\*\/])\s*(\d+\.?\d*)', text)
            
            if calculation_match:
                num1 = float(calculation_match.group(1))
                operator = calculation_match.group(2)
                num2 = float(calculation_match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "Maaf, tidak bisa membagi dengan nol."
                    result = num1 / num2
                else:
                    return "Operasi matematika tidak dikenali."
                
                # Format result
                if result.is_integer():
                    result = int(result)
                
                return f"Hasil dari {num1} {operator} {num2} adalah {result}"
            
            # Try to evaluate simple expressions
            # WARNING: This is potentially unsafe for user input
            # In production, use a proper math expression parser
            safe_chars = set('0123456789+-*/.() ')
            if all(c in safe_chars for c in text):
                try:
                    result = eval(text)
                    return f"Hasilnya adalah {result}"
                except:
                    pass
            
            return "Maaf, saya tidak bisa menghitung itu. Coba gunakan format seperti '5 plus 3' atau '10 kali 2'."
            
        except Exception as e:
            self.logger.error(f"Calculation error: {e}")
            return "Maaf, terjadi kesalahan dalam perhitungan."
    
    def add_custom_command(self, command_type, patterns, responses):
        """
        Add custom command patterns and responses.
        
        Args:
            command_type (str): Name of the command type
            patterns (list): List of regex patterns
            responses (list or callable): List of responses or function
        """
        self.command_patterns[command_type] = patterns
        self.responses[command_type] = responses
        self.logger.info(f"Added custom command: {command_type}")
    
    def get_command_types(self):
        """Get list of available command types."""
        return list(self.command_patterns.keys())
    
    def get_help_text(self):
        """Get help text describing available commands."""
        help_items = [
            "Saya dapat membantu dengan:",
            "- Menyapa: 'Halo', 'Apa kabar'",
            "- Waktu: 'Jam berapa', 'Tanggal berapa'",
            "- Perhitungan: '5 plus 3', '10 kali 2'",
            "- Bantuan: 'Bantuan', 'Apa yang bisa kamu lakukan'",
            "- Perpisahan: 'Sampai jumpa', 'Selamat tinggal'"
        ]
        return "\n".join(help_items)
