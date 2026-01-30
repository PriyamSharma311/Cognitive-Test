from src.assessment.adaptive_engine import generate_single_adaptive_question


DOMAINS = ["memory", "reasoning", "attention", "language", "executive"]


def select_question(state, question_index: int):
    """
    Selects the next question based on cognitive state.

    Rules:
    - Rotate domains to avoid fatigue
    - Use LLM only when user is struggling or at the start
    """

    domain = DOMAINS[question_index % len(DOMAINS)]

    # LLM only when really needed
    use_llm = (
        state.questions_seen < 2
        or state.avg_time > 20
        or state.difficulty > 0.8
    )

    question = generate_single_adaptive_question(
        domain=domain,
        difficulty=state.difficulty,
        q_num=question_index,
        use_llm=use_llm
    )

    # Item difficulty proxy (used by IRT)
    b = state.difficulty

    return question, domain, b
