from src.rag.retrieve_context import retrieve_context
from src.rag.llm_generator import generate_llm_response


def explain_adaptive_answer(question: str, correct: str, selected: str) -> str:
    """
    RAG-grounded explanation for adaptive questions.
    """

    context = retrieve_context(question)

    prompt = f"""
Question:
{question}

Correct answer:
{correct}

User selected:
{selected}

Explain simply:
- Why the correct answer is right
- Why the selected answer may be incorrect
- Use ONLY the provided knowledge
- Friendly, non-judgmental tone
"""

    return generate_llm_response(
        user_text=prompt,
        rag_context=context,
        emotion={},
        cognitive_profile={}
    )
