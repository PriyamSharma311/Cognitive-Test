import math


def irt_probability(theta: float, b: float) -> float:
    """
    Probability of a correct response given:
    theta = user ability
    b = item difficulty
    """
    return 1 / (1 + math.exp(-(theta - b)))


def update_theta(
    theta: float,
    correct: int,
    b: float,
    learning_rate: float = 0.05
) -> float:
    """
    Updates ability estimate using a simplified IRT gradient step.

    correct: 1 if correct, 0 if incorrect
    """
    p = irt_probability(theta, b)
    return round(theta + learning_rate * (correct - p), 4)
