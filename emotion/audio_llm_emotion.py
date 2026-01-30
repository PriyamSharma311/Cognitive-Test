from typing import Dict
import json
from src.rag.llm_generator import generate_llm_response


def infer_audio_emotion_with_llm(
    transcript: str,
    rag_context: str = "",
    detected_language: str = "unknown"
) -> Dict:
    """
    NON-diagnostic emotion inference.
    Hinglish-aware, Hindi-aware, accent-aware.
    """

    if not transcript.strip():
        return {
            "state": "unknown",
            "confidence": 0.0,
            "signals": [],
            "explanation": "No clear speech detected to analyze.",
            "disclaimer": "No inference was made."
        }

    prompt = f"""
You are an empathetic assistant analyzing emotional cues in speech.

IMPORTANT:
- Speaker may use Indian English, Hindi, or Hinglish
- Hindi words written in English script are common
- DO NOT diagnose
- Focus ONLY on how the person SOUNDS

Detected language: {detected_language}

Speech transcript:
\"\"\"{transcript}\"\"\"

Respond ONLY in valid JSON:
{{
  "state": "calm | uncertain | stressed | overwhelmed | low | angry",
  "confidence": 0.0-1.0,
  "signals": ["observed cues"],
  "explanation": "1–2 gentle sentences",
  "disclaimer": "Supportive, non-diagnostic disclaimer"
}}
"""

    raw = generate_llm_response(
        user_text=prompt,
        rag_context="",
        emotion={},
        cognitive_profile={}
    )

    try:
        parsed = json.loads(raw)
        return {
            "state": parsed.get("state", "uncertain"),
            "confidence": float(parsed.get("confidence", 0.4)),
            "signals": parsed.get("signals", []),
            "explanation": parsed.get("explanation", ""),
            "disclaimer": parsed.get(
                "disclaimer",
                "This is a supportive interpretation, not a diagnosis."
            )
        }
    except Exception:
        return {
            "state": "uncertain",
            "confidence": 0.4,
            "signals": [],
            "explanation": "Mixed emotional cues detected.",
            "disclaimer": "This is a supportive interpretation, not a diagnosis."
        }
