"""
risk_flags.py

Defines standardized safety risk levels.
Used across safety, emotion, response, and guidance layers.
"""

from enum import Enum


class RiskLevel(Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def escalate(current: RiskLevel, new: RiskLevel) -> RiskLevel:
    """
    Escalate risk conservatively (never downgrade automatically).
    """
    order = [
        RiskLevel.SAFE,
        RiskLevel.LOW,
        RiskLevel.MEDIUM,
        RiskLevel.HIGH,
        RiskLevel.CRITICAL
    ]

    return order[max(order.index(current), order.index(new))]
