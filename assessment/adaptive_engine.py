from src.assessment.template_retriever import retrieve_template


def generate_single_adaptive_question(
    domain: str,
    difficulty: float,
    q_num: int,
) -> dict:
    """
    Generates ONE adaptive question.

    Guarantees:
    - Always returns a real, answerable question
    - No placeholders
    - No silent fallbacks
    - Compatible with Adaptive_Test UI
    """

    # --------------------------------------------------
    # Task rotation (for future extensibility / logging)
    # --------------------------------------------------
    TASKS = {
        "reasoning": [
            "syllogism",
            "pattern recognition",
            "if-then logic",
            "deductive puzzle"
        ],
        "memory": ["recall"],
        "attention": ["odd_one"],
        "language": ["sentence"],
        "executive": ["priority"]
    }

    task_list = TASKS.get(domain)
    if not task_list:
        raise ValueError(f"Unknown domain: {domain}")

    # Rotate task type (currently informational)
    task_type = task_list[q_num % len(task_list)]

    # --------------------------------------------------
    # Difficulty bucketing (numeric → label)
    # --------------------------------------------------
    if difficulty < 0.4:
        diff_label = "easy"
    elif difficulty < 0.7:
        diff_label = "medium"
    else:
        diff_label = "hard"

    # --------------------------------------------------
    # Retrieve question (DOMAIN + DIFFICULTY ONLY)
    # --------------------------------------------------
    question = retrieve_template(domain, diff_label)

    if question is None:
        raise RuntimeError("No template returned a question")

    # --------------------------------------------------
    # Enforce strict UI contract
    # --------------------------------------------------
    if (
        not isinstance(question, dict)
        or "question" not in question
        or "options" not in question
        or "answer" not in question
    ):
        raise RuntimeError("Invalid question format returned by template")

    # --------------------------------------------------
    # Return clean payload to UI
    # --------------------------------------------------
    return {
        "question": question["question"],
        "options": question["options"],
        "answer": question["answer"],
        "domain": domain,
        "difficulty": diff_label,
        "task_type": task_type
    }
