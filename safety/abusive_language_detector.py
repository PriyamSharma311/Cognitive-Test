"""
abusive_language_detector.py

Detects abusive, threatening, or self-harm language.
Acts as the FIRST safety gate in the system.
"""

from typing import Dict
from .risk_flags import RiskLevel
from .safety_rules import evaluate_text_risk


def detect_abusive_language(text: str) -> Dict:
    """
    Main API for abusive language detection.
    """

    if not text or not text.strip():
        return {
            "risk_level": RiskLevel.SAFE,
            "flags": [],
            "safe_to_continue": True
        }

    result = evaluate_text_risk(text)

    risk = result["risk_level"]
    flags = result["matched_rules"]

    safe_to_continue = risk not in {
        RiskLevel.HIGH,
        RiskLevel.CRITICAL
    }

    return {
        "risk_level": risk,
        "flags": flags,
        "safe_to_continue": safe_to_continue
    }


# -------------------------------------------------
# Local test (SAFE — no imports here)
# -------------------------------------------------
if __name__ == "__main__":

    samples = [
        "I hate you",
        "You are stupid",
        "I want to die",
        "I am confused but trying"
    ]

    for s in samples:
        print(s)
        print(detect_abusive_language(s))
        print("-" * 50)
