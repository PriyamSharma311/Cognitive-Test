"""
safety_rules.py

Defines safety rules for detecting abusive, harmful, or risky language.
NON-diagnostic. Used for moderation & adaptive response.
"""

from typing import Dict
from .risk_flags import RiskLevel


# ----------------------------------------
# Keyword dictionaries (simple + expandable)
# ----------------------------------------
ABUSIVE_KEYWORDS = {
    "hate", "kill", "stupid", "idiot", "shut up",
    "dumb", "moron", "ugly", "worthless"
}

SELF_HARM_KEYWORDS = {
    "die", "suicide", "kill myself", "end my life",
    "no reason to live"
}


# ----------------------------------------
# Core rule engine
# ----------------------------------------
def evaluate_text_risk(text: str) -> Dict:
    """
    Evaluate text and assign a safety risk level.
    Returns structured flags for explainability.
    """

    text = text.lower()

    matched_rules = []

    abuse_hits = 0
    for w in ABUSIVE_KEYWORDS:
        if w in text:
            abuse_hits += 1
            matched_rules.append(f"abusive:{w}")

    self_harm_hits = 0
    for w in SELF_HARM_KEYWORDS:
        if w in text:
            self_harm_hits += 1
            matched_rules.append(f"self_harm:{w}")

    if self_harm_hits > 0:
        level = RiskLevel.CRITICAL

    elif abuse_hits >= 2:
        level = RiskLevel.HIGH

    elif abuse_hits == 1:
        level = RiskLevel.MEDIUM

    else:
        level = RiskLevel.SAFE

    return {
        "risk_level": level,
        "matched_rules": matched_rules,
        "abuse_hits": abuse_hits,
        "self_harm_hits": self_harm_hits
    }
