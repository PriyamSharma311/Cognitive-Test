"""
text_emotion.py

Detects basic emotional state from text input.
NON-diagnostic. Safety-aware.
"""

from typing import Dict


EMOTION_KEYWORDS = {
    "anger": ["angry", "mad", "hate", "furious", "annoyed"],
    "sadness": ["sad", "cry", "upset", "lonely", "depressed"],
    "fear": ["scared", "afraid", "worried", "nervous", "anxious"],
    "joy": ["happy", "excited", "glad", "joy", "proud"],
    "confusion": ["confused", "don't understand", "lost", "unclear"]
}


def detect_text_emotion(text: str) -> Dict[str, float]:
    """
    Returns soft emotion scores (0–1).
    """

    text = text.lower()
    scores = {e: 0.0 for e in EMOTION_KEYWORDS}

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[emotion] += 1.0

    total = sum(scores.values())
    if total == 0:
        return {e: 0.0 for e in scores}

    # Normalize
    return {e: round(v / total, 2) for e, v in scores.items()}


if __name__ == "__main__":
    sample = "I am confused and a little worried"
    print(detect_text_emotion(sample))
