"""
audio_processor.py
Multilingual transcription (English + Hindi + Hinglish)
Stable for Streamlit (no reloading, no segfaults)
"""

import os
import whisper
import librosa
import numpy as np
import soundfile as sf

# --------------------------------------------------
# 🔒 THREAD SAFETY (CRITICAL)
# --------------------------------------------------
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# --------------------------------------------------
# 🔥 LOAD WHISPER ONCE (GLOBAL SINGLETON)
# --------------------------------------------------
_whisper_model = None

def get_whisper_model():
    """
    Loads Whisper model only once.
    Prevents memory & OpenMP crashes.
    """
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(
            "medium",   # best balance for Hindi + Hinglish
            device="cpu"
        )
    return _whisper_model


# --------------------------------------------------
# 🧹 REPETITION CLEANER (SAFE)
# --------------------------------------------------
def remove_repetition(text: str) -> str:
    words = text.split()
    cleaned = []

    for w in words:
        # prevent 3-word looping
        if len(cleaned) >= 3 and cleaned[-3:] == [w, w, w]:
            continue
        cleaned.append(w)

    return " ".join(cleaned)


# --------------------------------------------------
# 🎙️ MAIN AUDIO PROCESSOR
# --------------------------------------------------
def process_audio(audio_path: str) -> dict:
    """
    Transcribes speech robustly:
    - English (unchanged quality)
    - Hindi
    - Hinglish (code-mixed)

    Returns:
    {
        "transcript": str,
        "language": "en" | "hi" | "unknown"
    }
    """

    # ---------------------------
    # LOAD AUDIO (NO AGGRESSIVE FILTERING)
    # ---------------------------
    y, sr = librosa.load(audio_path, sr=16000, mono=True)

    # Normalize only (do NOT trim silence — harms Hindi)
    if np.max(np.abs(y)) > 0:
        y = y / np.max(np.abs(y))

    sf.write(audio_path, y, sr)

    # ---------------------------
    # WHISPER TRANSCRIPTION
    # ---------------------------
    model = get_whisper_model()

    result = model.transcribe(
        audio_path,
        task="transcribe",
        language=None,                     # auto-detect
        temperature=0.4,                   # avoids looping
        beam_size=5,                       # better decoding
        patience=1.0,
        condition_on_previous_text=False,  # 🔑 STOP repetition
        initial_prompt=(
            "The speaker may speak English, Hindi, or Hinglish. "
            "Transcribe naturally without repeating phrases."
        ),
        fp16=False                         # CPU-safe
    )

    raw_text = result.get("text", "").strip()
    clean_text = remove_repetition(raw_text)

    return {
        "transcript": clean_text,
        "language": result.get("language", "unknown")
    }
