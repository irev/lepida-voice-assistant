#!/usr/bin/env python3
"""
Command Processing Module
Handles voice command interpretation and processing for Lepida Voice Assistant
"""

import logging
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import helper modules
from helper.numberToText import NumberToText

logger = logging.getLogger(__name__)

class CommandProcessor:
    """
    Main command processor for Lepida Voice Assistant.
    Handles voice command interpretation and execution.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize command processor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.number_converter = NumberToText()
        
        # Command patterns
        self.command_patterns = {
            'greeting': [
                r'halo',
                r'hai', 
                r'selamat (pagi|siang|sore|malam)',
                r'apa kabar'
            ],
            'time': [
                r'jam berapa',
                r'waktu sekarang',
                r'hari apa'
            ],
            'weather': [
                r'cuaca',
                r'hujan',
                r'panas'
            ],
            'system': [
                r'matikan',
                r'restart',
                r'volume',
                r'berhenti'
            ]
        }
        
        self.logger.info("CommandProcessor initialized")
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process input text and convert numbers to words.
        
        Args:
            text: Input text to process
            
        Returns:
            Dict containing processed text and metadata
        """
        if not text:
            return {
                'original': text,
                'processed': '',
                'has_numbers': False,
                'command_type': 'unknown'
            }
        
        # Convert text to lowercase for processing
        processed_text = text.lower().strip()
        
        # Check for numbers and convert them
        has_numbers = bool(re.search(r'\d+', processed_text))
        if has_numbers:
            processed_text = self._convert_numbers_in_text(processed_text)
        
        # Detect command type
        command_type = self._detect_command_type(processed_text)
        
        return {
            'original': text,
            'processed': processed_text,
            'has_numbers': has_numbers,
            'command_type': command_type
        }
    
    def _convert_numbers_in_text(self, text: str) -> str:
        """
        Convert numbers in text to Indonesian words.
        
        Args:
            text: Text containing numbers
            
        Returns:
            Text with numbers converted to words
        """
        def replace_number(match):
            number_str = match.group()
            try:
                number = int(number_str)
                if 0 <= number <= 999999999:  # Within supported range
                    return self.number_converter.convert(number)
                else:
                    return number_str  # Keep original if out of range
            except ValueError:
                return number_str  # Keep original if conversion fails
        
        # Replace all numbers in text
        return re.sub(r'\d+', replace_number, text)
    
    def _detect_command_type(self, text: str) -> str:
        """
        Detect the type of command from processed text.
        
        Args:
            text: Processed text
            
        Returns:
            Command type string
        """
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return command_type
        
        return 'general'
    
    def execute_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a processed command.
        
        Args:
            command_data: Processed command data
            
        Returns:
            Execution result
        """
        command_type = command_data.get('command_type', 'general')
        processed_text = command_data.get('processed', '')
        
        try:
            if command_type == 'greeting':
                return self._handle_greeting(processed_text)
            elif command_type == 'time':
                return self._handle_time_request(processed_text)
            elif command_type == 'weather':
                return self._handle_weather_request(processed_text)
            elif command_type == 'system':
                return self._handle_system_command(processed_text)
            else:
                return self._handle_general_command(processed_text)
                
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat memproses perintah.',
                'error': str(e)
            }
    
    def _handle_greeting(self, text: str) -> Dict[str, Any]:
        """Handle greeting commands."""
        responses = [
            "Halo! Selamat datang di Lepida Voice Assistant.",
            "Hai! Ada yang bisa saya bantu?",
            "Selamat datang! Bagaimana kabar Anda?"
        ]
        
        import random
        return {
            'success': True,
            'response': random.choice(responses),
            'command_type': 'greeting'
        }
    
    def _handle_time_request(self, text: str) -> Dict[str, Any]:
        """Handle time-related requests."""
        from datetime import datetime
        
        now = datetime.now()
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        
        if 'jam berapa' in text or 'waktu sekarang' in text:
            time_str = now.strftime('%H:%M')
            response = f"Sekarang pukul {time_str}."
        elif 'hari apa' in text:
            day_name = days[now.weekday()]
            response = f"Hari ini hari {day_name}."
        else:
            response = f"Sekarang hari {days[now.weekday()]}, pukul {now.strftime('%H:%M')}."
        
        return {
            'success': True,
            'response': response,
            'command_type': 'time'
        }
    
    def _handle_weather_request(self, text: str) -> Dict[str, Any]:
        """Handle weather-related requests."""
        return {
            'success': False,
            'response': 'Maaf, fitur cuaca sedang dalam pengembangan. Silakan cek cuaca melalui aplikasi lain.',
            'command_type': 'weather'
        }
    
    def _handle_system_command(self, text: str) -> Dict[str, Any]:
        """Handle system commands."""
        if 'matikan' in text or 'berhenti' in text:
            return {
                'success': True,
                'response': 'Baik, saya akan berhenti. Sampai jumpa!',
                'command_type': 'system',
                'action': 'shutdown'
            }
        elif 'volume' in text:
            return {
                'success': True,
                'response': 'Pengaturan volume sedang dalam pengembangan.',
                'command_type': 'system'
            }
        else:
            return {
                'success': False,
                'response': 'Perintah sistem tidak dikenali.',
                'command_type': 'system'
            }
    
    def _handle_general_command(self, text: str) -> Dict[str, Any]:
        """Handle general commands."""
        return {
            'success': True,
            'response': f'Anda mengatakan: "{text}". Terima kasih atas inputnya!',
            'command_type': 'general'
        }
    
    def get_supported_commands(self) -> List[str]:
        """
        Get list of supported command types.
        
        Returns:
            List of supported command types
        """
        return list(self.command_patterns.keys()) + ['general']
    
    def get_command_examples(self) -> Dict[str, List[str]]:
        """
        Get examples for each command type.
        
        Returns:
            Dictionary of command examples
        """
        return {
            'greeting': ['Halo', 'Selamat pagi', 'Apa kabar'],
            'time': ['Jam berapa sekarang?', 'Hari apa ini?'],
            'weather': ['Bagaimana cuaca hari ini?'],
            'system': ['Matikan', 'Berhenti', 'Atur volume'],
            'general': ['Apa pun yang ingin Anda katakan']
        }


def main():
    """Test the command processor."""
    processor = CommandProcessor()
    
    test_commands = [
        "Halo lepida",
        "Jam berapa sekarang?",
        "Saya punya 12 apel",
        "Matikan sistem",
        "Bagaimana cuaca hari ini?"
    ]
    
    for command in test_commands:
        print(f"\nInput: {command}")
        processed = processor.process_text(command)
        print(f"Processed: {processed}")
        
        result = processor.execute_command(processed)
        print(f"Response: {result.get('response', 'No response')}")


if __name__ == "__main__":
    main()
