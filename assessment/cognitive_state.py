from dataclasses import dataclass, field


@dataclass
class CognitiveState:
    """
    Central cognitive state for adaptive testing.

    This object is:
    - Updated after every question
    - Stored in Streamlit session_state
    - Used for adaptivity decisions
    """

    # Ability estimate (IRT-style)
    theta: float = 0.0

    # Adaptive difficulty (0.2 – 0.9)
    difficulty: float = 0.5

    # Average response time (seconds)
    avg_time: float = 0.0

    # Total questions attempted
    questions_seen: int = 0

    # Domain-wise correctness counts
    domain_scores: dict = field(default_factory=lambda: {
        "memory": 0,
        "attention": 0,
        "language": 0,
        "reasoning": 0,
        "executive": 0
    })

    def reset_for_new_domain(self):
        """
        Optional helper if you want per-domain reset behavior.
        """
        self.difficulty = 0.5
        self.avg_time = 0.0
