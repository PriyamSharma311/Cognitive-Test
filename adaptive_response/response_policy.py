"""
response_policy.py

Defines response permissions based on safety risk and emotional state.
This is a GOVERNING layer — nothing bypasses it.
"""

from typing import Dict
from src.safety.risk_flags import RiskLevel


def evaluate_response_policy(
    risk_level: RiskLevel,
    dominant_emotion: str
) -> Dict:
    """
    Returns response constraints.
    """

    # Default policy
    policy = {
        "allow_guidance": True,
        "allow_career_advice": True,
        "tone": "neutral",
        "max_length": "medium",
        "require_support_message": False
    }

    # High-risk override
    if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
        policy.update({
            "allow_guidance": False,
            "allow_career_advice": False,
            "tone": "calm_supportive",
            "max_length": "short",
            "require_support_message": True
        })
        return policy

    # Emotion-based tuning
    if dominant_emotion in ["sadness", "fear", "confusion", "stress"]:
        policy.update({
            "tone": "supportive",
            "max_length": "short"
        })

    if dominant_emotion in ["anger"]:
        policy.update({
            "tone": "calm",
            "max_length": "short"
        })

    if dominant_emotion in ["joy", "calm"]:
        policy.update({
            "tone": "encouraging"
        })

    return policy
