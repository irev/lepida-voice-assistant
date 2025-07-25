import whisper
import os

print("Testing Whisper installation...")
try:
    print("Loading tiny model...")
    model = whisper.load_model("tiny")
    print("Model loaded successfully!")
    
    audio_file = "output.wav"
    if os.path.exists(audio_file):
        print(f"Found audio file: {audio_file}")
        print("Starting transcription...")
        result = model.transcribe(audio_file)
        print(f"Transcription: {result['text']}")
    else:
        print("Audio file not found!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
