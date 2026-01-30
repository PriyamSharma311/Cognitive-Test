"""
scoring_rules.py

Scoring logic for text-based cognitive tests.
This module is NON-diagnostic and focuses on functional skill estimation.
"""

from typing import Dict, Any


# -------------------------------------------
# Difficulty weights (can be tuned later)
# -------------------------------------------
DIFFICULTY_WEIGHTS = {
    "easy": 1.0,
    "medium": 1.2,
    "hard": 1.5
}


# -------------------------------------------
# Utility: normalize text
# -------------------------------------------
def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return text.strip().lower()


# -------------------------------------------
# Core: score a single question
# -------------------------------------------
def score_question(
    question: Dict[str, Any],
    user_answer: str,
    response_time_sec: float
) -> float:
    """
    Scores a single question.

    Returns:
        score (float): score earned for the question
    """

    correct_answer = normalize_text(questsion.get("correct_answer", ""))
    user_answer = normalize_text(user_answer)

    max_score = question.get("max_score", 1)
    difficulty = question.get("difficulty", "easy")
    time_limit = question.get("time_limit_sec", None)

    # -----------------------------
    # Check correctness
    # -----------------------------
    if correct_answer == "":
        base_score = 0.0
    elif correct_answer in user_answer:
        base_score = max_score
    else:
        base_score = 0.0

    # -----------------------------
    # Difficulty weighting
    # -----------------------------
    difficulty_weight = DIFFICULTY_WEIGHTS.get(difficulty, 1.0)
    weighted_score = base_score * difficulty_weight

    # -----------------------------
    # Time penalty (soft penalty)
    # -----------------------------
    if time_limit and response_time_sec:
        if response_time_sec > time_limit:
            penalty_factor = max(0.7, time_limit / response_time_sec)
            weighted_score *= penalty_factor

    return round(weighted_score, 2)


# -------------------------------------------
# Score multiple responses
# -------------------------------------------
from typing import Dict


def score_responses(user_responses: Dict, questions: Dict) -> Dict:
    """
    Scores user responses against cognitive test questions.

    Supports BOTH formats:
    1) user_responses[qid] = "answer"
    2) user_responses[qid] = {"answer": "...", "time": seconds}

    Returns normalized domain scores (0–100), raw scores, and details.
    """

    domain_scores = {}
    domain_max = {}
    detailed_scores = []

    for q in questions["questions"]:
        qid = q["question_id"]
        domain = q["domain"]
        correct = str(q["correct_answer"]).lower()
        max_score = float(q.get("max_score", 1))

        domain_scores.setdefault(domain, 0.0)
        domain_max.setdefault(domain, 0.0)

        domain_max[domain] += max_score

        # ---------- USER ANSWER HANDLING ----------
        if qid in user_responses:
            response = user_responses[qid]

            # Accept both dict and string
            if isinstance(response, dict):
                user_answer = str(response.get("answer", "")).lower()
            else:
                user_answer = str(response).lower()

            score = max_score if user_answer == correct else 0.0
        else:
            score = 0.0

        domain_scores[domain] += score

        detailed_scores.append({
            "question_id": qid,
            "domain": domain,
            "score": score,
            "max_possible": max_score
        })

    # ---------- NORMALIZATION ----------
    normalized_scores = {
        domain: round((domain_scores[domain] / domain_max[domain]) * 100, 2)
        if domain_max[domain] > 0 else 0.0
        for domain in domain_scores
    }

    return {
        "normalized_scores": normalized_scores,
        "raw_scores": domain_scores,
        "details": detailed_scores
    }



# ✅ ONLY FOR LOCAL TESTING

