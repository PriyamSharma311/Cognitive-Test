"""
response_builder.py

Builds final user-facing response by combining:
- RAG output
- Safety policy
- Tone control
"""

from typing import Dict
from .response_policy import evaluate_response_policy
from .tone_controller import apply_tone
from src.safety.risk_flags import RiskLevel


def build_response(
    rag_text: str,
    risk_level: RiskLevel,
    emotion_state: Dict
) -> str:
    """
    Produces final response text.
    """

    dominant_emotion = emotion_state.get("dominant_emotion", "neutral")

    policy = evaluate_response_policy(risk_level, dominant_emotion)

    # Safety override message
    if policy["require_support_message"]:
        return (
            "I’m really glad you shared this. "
            "If you’re feeling overwhelmed or unsafe, "
            "please consider reaching out to someone you trust "
            "or a local support service."
        )

    # Restrict length if needed
    text = rag_text
    if policy["max_length"] == "short":
        text = rag_text.split(".")[0] + "."

    # Apply tone
    final_text = apply_tone(text, policy["tone"])

    return final_text
