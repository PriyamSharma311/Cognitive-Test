import os, sys
import streamlit as st
import numpy as np
from io import BytesIO
import soundfile as sf
from audiorecorder import audiorecorder

st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-size: 18px !important;
    line-height: 1.6;
}
button {
    font-size: 18px !important;
}
</style>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# 🔧 PATH FIX (CRITICAL)
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --------------------------------------------------
# IMPORTS
# --------------------------------------------------
from src.audio.audio_processor import process_audio
from src.emotion.audio_llm_emotion import infer_audio_emotion_with_llm
from src.emotion.confidence_calibrator import calibrate_confidence
from src.emotion.emotion_tracker import update_emotion_history

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
defaults = {
    "raw_audio_bytes": None,
    "transcript": "",
    "detected_language": "unknown",
    "audio_emotion": None,
    "emotion_history": []
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("🎙️ Audio Capture")
st.write("Supports **Hindi, English, Hinglish (Indian accents)**")

# 🔁 RESET
if st.button("🔄 Record Again"):
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

# --------------------------------------------------
# RECORD AUDIO
# --------------------------------------------------
audio = audiorecorder("🎤 Start Recording", "⏹ Stop Recording")

# --------------------------------------------------
# SAVE RAW AUDIO
# --------------------------------------------------
if len(audio) > 0:
    buffer = BytesIO()
    audio.export(buffer, format="wav", parameters=["-ar", "16000", "-ac", "1"])
    st.session_state.raw_audio_bytes = buffer.getvalue()

# --------------------------------------------------
# PROCESS AUDIO
# --------------------------------------------------
if st.session_state.raw_audio_bytes:

    st.audio(st.session_state.raw_audio_bytes)

    audio_path = os.path.join(PROJECT_ROOT, "src/audio/temp/live.wav")
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    # Load audio
    samples, sr = sf.read(BytesIO(st.session_state.raw_audio_bytes))
    samples = samples.astype(np.float32)

    # ⚠️ DO NOT aggressively trim → preserves Hinglish cadence
    if np.max(np.abs(samples)) > 0:
        samples = samples / np.max(np.abs(samples))

    sf.write(audio_path, samples, 16000)

    # ---------------------------
    # SPEECH → TEXT (Whisper multilingual)
    # ---------------------------
    result = process_audio(audio_path)

    st.session_state.transcript = result.get("transcript", "").strip()
    st.session_state.detected_language = result.get("language", "unknown")

    # --------------------------------------------------
    # UI OUTPUT
    # --------------------------------------------------
    st.subheader("🗣 Transcript")
    st.write(
        st.session_state.transcript
        if st.session_state.transcript
        else "_No clear speech detected yet_"
    )

    st.subheader("🌍 Detected Language")
    st.code(st.session_state.detected_language)

    # --------------------------------------------------
    # ℹ️ HINGLISH SHORT-HINDI WARNING (UI ONLY)
    # --------------------------------------------------
    if (
        st.session_state.detected_language == "hi"
        and len(st.session_state.transcript.split()) < 6
    ):
        st.info(
            "ℹ️ Short Hindi phrases detected. "
            "If you are speaking Hinglish, try speaking continuously "
            "without long pauses."
        )

    # --------------------------------------------------
    # EMOTION FROM AUDIO (LLM)
    # --------------------------------------------------
    if st.session_state.transcript:
        audio_emotion = infer_audio_emotion_with_llm(
            transcript=st.session_state.transcript,
            rag_context=""
        )

        audio_emotion = calibrate_confidence(audio_emotion)

        # 🔁 Confidence fallback (UI explanation only)
        if (
            st.session_state.detected_language == "hi"
            and audio_emotion.get("confidence", 0) < 0.5
        ):
            audio_emotion["explanation"] += (
                " The speech may be code-mixed (Hinglish), which can reduce certainty."
            )

        st.session_state.audio_emotion = audio_emotion

        st.subheader("💙 Emotional Insight")
        st.json(audio_emotion)

        st.subheader("🧠 Why we think this")
        st.write(audio_emotion.get("explanation", ""))
        st.caption(
            audio_emotion.get(
                "disclaimer",
                "This is a supportive interpretation, not a diagnosis."
            )
        )

        update_emotion_history(
            st.session_state,
            audio_emotion.get("state", "unknown")
        )
