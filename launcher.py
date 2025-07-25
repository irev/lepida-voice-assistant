#!/usr/bin/env python3
"""
Voice Assistant Launcher
Simple launcher script for the Lepida Voice Assistant
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Launch the voice assistant application."""
    try:
        from app import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Make sure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting voice assistant: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
