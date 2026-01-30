# src/audio/tts_engine.py

import pyttsx3
import os

_engine = pyttsx3.init()
_engine.setProperty("rate", 160)   # calm pace
_engine.setProperty("volume", 1.0)


def generate_audio_response(text: str, output_path: str):
    """
    Convert AI response text into speech.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    _engine.save_to_file(text, output_path)
    _engine.runAndWait()
