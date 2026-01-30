from src.assessment.templates import (
    generate_reasoning,
    generate_memory,
    generate_attention,
    generate_language,
    generate_executive
)


def retrieve_template(domain: str, difficulty: str) -> dict | None:
    """
    Returns a fully formed question dict.
    NEVER returns placeholders.
    """

    if domain == "reasoning":
        return generate_reasoning(difficulty)

    if domain == "memory":
        return generate_memory(difficulty)

    if domain == "attention":
        return generate_attention(difficulty)

    if domain == "language":
        return generate_language(difficulty)

    if domain == "executive":
        return generate_executive(difficulty)

    return None
