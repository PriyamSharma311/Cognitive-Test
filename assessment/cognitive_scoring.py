"""
cognitive_scoring.py

Combines multi-modal cognitive scores into a unified cognitive profile.
This module is explainable, extensible, and NON-diagnostic.
"""

from typing import Dict, Optional


# -------------------------------------------------
# Default modality weights (can be tuned later)
# -------------------------------------------------
MODALITY_WEIGHTS = {
    "text": 0.6,
    "audio": 0.25,
    "vision": 0.15
}


# -------------------------------------------------
# Domain importance weights (optional tuning)
# -------------------------------------------------
DOMAIN_WEIGHTS = {
    "memory": 1.0,
    "attention": 1.1,
    "language": 1.0,
    "reasoning": 1.1,
    "executive": 1.2
}


# -------------------------------------------------
# Normalize helper
# -------------------------------------------------
def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(value, max_val))


# -------------------------------------------------
# Adaptive-test → domain score
# -------------------------------------------------
def adaptive_domain_score(
    correct_ratio: float,
    avg_response_time: float,
    theta: float
) -> float:
    """
    Converts adaptive test signals into a 0–100 domain score.

    correct_ratio: 0–1
    avg_response_time: seconds
    theta: ability estimate (≈ -1 to +1)
    """

    accuracy_component = correct_ratio * 70
    speed_component = max(0, 20 - avg_response_time) * 1.5
    ability_component = (theta + 1) * 15

    raw_score = accuracy_component + speed_component + ability_component
    return clamp(round(raw_score, 2))


# -------------------------------------------------
# Core: build unified cognitive profile
# -------------------------------------------------
def build_cognitive_profile(
    text_scores: Dict[str, float],
    audio_scores: Optional[Dict[str, float]] = None,
    vision_scores: Optional[Dict[str, float]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Builds a unified cognitive profile from multi-modal inputs.

    All inputs are expected to be normalized to 0–100.
    """

    audio_scores = audio_scores or {}
    vision_scores = vision_scores or {}

    unified_scores = {}
    explanations = {}

    for domain in text_scores.keys():

        text_val = text_scores.get(domain, 0)
        audio_val = audio_scores.get(domain, text_val)
        vision_val = vision_scores.get(domain, text_val)

        combined = (
            text_val * MODALITY_WEIGHTS["text"] +
            audio_val * MODALITY_WEIGHTS["audio"] +
            vision_val * MODALITY_WEIGHTS["vision"]
        )

        weighted = combined * DOMAIN_WEIGHTS.get(domain, 1.0)
        final_score = round(clamp(weighted), 2)

        unified_scores[domain] = final_score
        explanations[domain] = explain_score(domain, final_score)

    return {
        "cognitive_profile": unified_scores,
        "explanations": explanations
    }


# -------------------------------------------------
# Explainability layer
# -------------------------------------------------
def explain_score(domain: str, score: float) -> str:
    if score >= 85:
        level = "strong"
    elif score >= 65:
        level = "moderate"
    else:
        level = "needs support"

    explanation_map = {
        "memory": {
            "strong": "Good recall and retention of information.",
            "moderate": "Can remember information with some effort.",
            "needs support": "May benefit from memory aids and repetition."
        },
        "attention": {
            "strong": "Able to focus well on tasks.",
            "moderate": "Focus is present but may drift.",
            "needs support": "Short attention span; structured tasks help."
        },
        "language": {
            "strong": "Understands and uses language effectively.",
            "moderate": "Communicates clearly with some support.",
            "needs support": "May need simpler language and examples."
        },
        "reasoning": {
            "strong": "Good logical thinking and pattern recognition.",
            "moderate": "Can reason with guidance.",
            "needs support": "Needs step-by-step reasoning help."
        },
        "executive": {
            "strong": "Plans and organizes tasks well.",
            "moderate": "Can plan with reminders.",
            "needs support": "Needs help with planning and task order."
        }
    }

    return explanation_map.get(domain, {}).get(level, "")


# -------------------------------------------------
# Optional: overall cognitive index
# -------------------------------------------------
def compute_overall_cognitive_index(profile: Dict[str, float]) -> float:
    if not profile:
        return 0.0

    return round(sum(profile.values()) / len(profile), 2)


# -------------------------------------------------
# Build profile directly from adaptive test
# -------------------------------------------------
def build_profile_from_adaptive_test(
    domain_stats: Dict[str, Dict[str, float]],
    theta: float
) -> Dict[str, Dict[str, float]]:
    """
    Builds a cognitive profile from adaptive test outputs.

    domain_stats example:
    {
        "memory": {"correct_ratio": 0.75, "avg_time": 9.2},
        "attention": {"correct_ratio": 0.6, "avg_time": 13.1}
    }
    """

    text_scores = {}

    for domain, stats in domain_stats.items():
        text_scores[domain] = adaptive_domain_score(
            correct_ratio=stats.get("correct_ratio", 0),
            avg_response_time=stats.get("avg_time", 15),
            theta=theta
        )

    return build_cognitive_profile(text_scores)


# -------------------------------------------------
# Example test run (safe)
# -------------------------------------------------
if __name__ == "__main__":

    text_scores_example = {
        "memory": 78.0,
        "attention": 65.0,
        "language": 85.0,
        "reasoning": 72.0,
        "executive": 60.0
    }

    profile = build_cognitive_profile(text_scores_example)
    overall_index = compute_overall_cognitive_index(profile["cognitive_profile"])

    print("Unified Cognitive Profile:")
    print(profile["cognitive_profile"])
    print("\nExplanations:")
    print(profile["explanations"])
    print("\nOverall Cognitive Index:", overall_index)
