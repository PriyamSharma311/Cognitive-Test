from typing import Dict, List


def difficulty_alignment(answers: List[Dict]) -> float:
    """
    Ideal adaptive test keeps accuracy around ~70%.
    Lower value = better alignment.
    """
    if not answers:
        return 1.0

    accuracy = sum(a["correct"] for a in answers) / len(answers)
    return round(abs(accuracy - 0.7), 3)


def fatigue_index(answers: List[Dict]) -> float:
    """
    Measures increase in response time across the test.
    Positive value = possible fatigue.
    """
    if len(answers) < 6:
        return 0.0

    first = [a["response_time"] for a in answers[:3]]
    last = [a["response_time"] for a in answers[-3:]]

    return round((sum(last) / 3) - (sum(first) / 3), 2)


def stability_score(answers: List[Dict]) -> float:
    """
    Measures consistency of performance.
    Lower variance = higher stability.
    """
    if len(answers) < 5:
        return 0.0

    correctness = [int(a["correct"]) for a in answers]
    mean = sum(correctness) / len(correctness)

    variance = sum((x - mean) ** 2 for x in correctness) / len(correctness)
    return round(1 - variance, 3)


def adaptive_quality_report(answers: List[Dict]) -> Dict[str, float]:
    """
    Single-call adaptive quality summary.
    """

    return {
        "difficulty_alignment": difficulty_alignment(answers),
        "fatigue_index": fatigue_index(answers),
        "stability_score": stability_score(answers)
    }
