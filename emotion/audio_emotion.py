"""
audio_emotion.py

Infers emotional tone from speech audio features.
Uses energy & pitch variance proxies.
"""

from typing import Dict


def detect_audio_emotion(audio_features: Dict[str, float]) -> Dict[str, float]:
    """
    Input: extracted audio features
    Output: soft emotion probabilities (0–1)
    """

    energy = audio_features.get("energy", 0)
    pitch_var = audio_features.get("pitch_variance", 0)

    emotions = {
        "calm": 0.0,
        "stress": 0.0,
        "excitement": 0.0,
        "sadness": 0.0
    }

    # Heuristic rules (explainable)
    if energy < 0.02:
        emotions["sadness"] += 0.6
        emotions["calm"] += 0.4

    if energy > 0.06:
        emotions["excitement"] += 0.7

    if pitch_var > 300:
        emotions["stress"] += 0.8

    total = sum(emotions.values())
    if total == 0:
        return emotions

    return {k: round(v / total, 2) for k, v in emotions.items()}


if __name__ == "__main__":
    sample_features = {
        "energy": 0.03,
        "pitch_variance": 450
    }
    print(detect_audio_emotion(sample_features))
