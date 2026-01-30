from collections import defaultdict

DOMAIN_LABELS = {
    "reasoning": "Logical & Analytical Thinking",
    "memory": "Recall & Retention",
    "attention": "Focus & Concentration",
    "language": "Reading & Language Skills",
    "executive": "Planning & Decision Making"
}


def compute_domain_statistics(answers):
    """
    Computes raw adaptive-test statistics per domain.

    answers item format:
    {
        "domain": str,
        "correct": bool,
        "response_time": float
    }
    """

    stats = defaultdict(lambda: {
        "total": 0,
        "correct": 0,
        "total_time": 0.0
    })

    for a in answers:
        d = a["domain"]
        stats[d]["total"] += 1
        stats[d]["correct"] += int(a["correct"])
        stats[d]["total_time"] += a["response_time"]

    domain_stats = {}

    for d, s in stats.items():
        domain_stats[d] = {
            "correct_ratio": round(s["correct"] / s["total"], 2),
            "avg_time": round(s["total_time"] / s["total"], 2)
        }

    return domain_stats


def classify_domain(score: float) -> str:
    if score >= 75:
        return "Strength"
    elif score >= 50:
        return "Developing"
    else:
        return "Needs Support"


def build_domain_summary(domain_scores):
    """
    Converts numeric domain scores into labeled summaries.
    """
    return {
        domain: {
            "label": DOMAIN_LABELS.get(domain, domain),
            "score": score,
            "status": classify_domain(score)
        }
        for domain, score in domain_scores.items()
    }
