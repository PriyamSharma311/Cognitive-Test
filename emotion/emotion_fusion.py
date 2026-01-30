"""
emotion_fusion.py

Combines text and audio emotions into a unified emotional state.
Safety-aware and explainable.
"""

from typing import Dict
from src.safety.risk_flags import RiskLevel


TEXT_WEIGHT = 0.6
AUDIO_WEIGHT = 0.4


def fuse_emotions(
    text_emotion: Dict[str, float],
    audio_emotion: Dict[str, float],
    risk_level: RiskLevel = RiskLevel.SAFE
) -> Dict:
    """
    Returns unified emotion + dominant state.
    """

    # Safety override
    if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
        return {
            "dominant_emotion": "distress",
            "confidence": 1.0,
            "details": {},
            "note": "Safety override applied"
        }

    all_emotions = set(text_emotion) | set(audio_emotion)
    combined = {}

    for e in all_emotions:
        combined[e] = round(
            text_emotion.get(e, 0) * TEXT_WEIGHT +
            audio_emotion.get(e, 0) * AUDIO_WEIGHT,
            2
        )

    dominant = max(combined, key=combined.get) if combined else "neutral"

    return {
        "dominant_emotion": dominant,
        "confidence": combined.get(dominant, 0),
        "details": combined
    }


if __name__ == "__main__":
    text = {"confusion": 0.6, "fear": 0.4}
    audio = {"stress": 0.7, "calm": 0.3}

    print(fuse_emotions(text, audio))
