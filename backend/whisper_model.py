"""
whisper_model.py
Shared singleton loader for OpenAI Whisper model to prevent duplicate RAM allocation.
"""
import whisper

_whisper_instance = None

def get_whisper_model(model_name: str = "base"):
    global _whisper_instance
    if _whisper_instance is None:
        print(f"Loading shared Whisper model ({model_name})...")
        _whisper_instance = whisper.load_model(model_name)
    return _whisper_instance
