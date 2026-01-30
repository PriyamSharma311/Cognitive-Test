"""
tone_controller.py

Controls tone, wording style, and sentence structure.
"""

from typing import List


TONE_TEMPLATES = {
    "calm_supportive": [
        "Let’s pause for a moment.",
        "You are not alone.",
        "We can take this one step at a time."
    ],
    "supportive": [
        "It’s okay to feel this way.",
        "Let’s work through this together.",
        "I’m here to help."
    ],
    "calm": [
        "Let’s slow down and focus.",
        "We’ll approach this carefully."
    ],
    "encouraging": [
        "You’re doing well.",
        "Keep going — you’re making progress!"
    ],
    "neutral": []
}


def apply_tone(base_text: str, tone: str) -> str:
    """
    Prepends tone-appropriate phrases.
    """

    prefixes: List[str] = TONE_TEMPLATES.get(tone, [])

    if not prefixes:
        return base_text

    prefix = " ".join(prefixes[:2])
    return f"{prefix} {base_text}"
    