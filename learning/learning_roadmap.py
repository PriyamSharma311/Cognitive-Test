# src/learning/learning_roadmap.py

import streamlit as st
from openai import RateLimitError

from src.rag.retrieve_context import retrieve_context
from src.rag.llm_generator import generate_llm_response


@st.cache_data(show_spinner=False)
def generate_learning_roadmap(scores: dict) -> str:
    """
    Generates a personalized learning roadmap.
    Cached to prevent repeated LLM calls on Streamlit reruns.
    """

    if not scores:
        return "No cognitive scores available to generate a roadmap."

    weak_areas = [k for k, v in scores.items() if v < 50]

    if not weak_areas:
        return (
            "🎉 Great news!\n\n"
            "No major weak areas detected. Continue strengthening your current skills "
            "with consistent practice and real-world application."
        )

    rag_context = retrieve_context(
        f"learning roadmap for {', '.join(weak_areas)} skills"
    )

    prompt = f"""
Create a short, personalized learning roadmap.

Weak cognitive areas:
{weak_areas}

Rules:
- Simple steps
- Beginner friendly
- Accessible language
- No medical or diagnostic terms
- Encouraging tone

Background information:
{rag_context}
"""

    try:
        return generate_llm_response(
            user_text=prompt,
            rag_context="",
            emotion={},
            cognitive_profile=scores
        )

    except RateLimitError:
        return (
            "⚠️ The AI service is temporarily busy.\n\n"
            "Please wait a few minutes and try generating the learning roadmap again."
        )

    except Exception as e:
        return (
            "⚠️ Unable to generate learning roadmap at the moment.\n\n"
            f"Error: {str(e)}"
        )
