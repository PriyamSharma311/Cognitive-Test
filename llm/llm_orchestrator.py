from typing import Dict, Optional
from src.rag.llm_generator import generate_llm_response
from src.rag.retrieve_context import retrieve_context

# --------------------------------------------------
# 🚫 USAGE CONTRACT (IMPORTANT)
# --------------------------------------------------
# This orchestrator is ONLY for:
# - Post-assessment guidance
# - Career insights
# - Emotional support (non-clinical)
#
# ❌ MUST NOT be used during adaptive testing
# ❌ MUST NOT be used for question generation
# --------------------------------------------------


# --------------------------------------------------
# Gemini (optional refinement layer)
# --------------------------------------------------
try:
    from src.llm.gemini_refiner import refine_with_gemini
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def generate_final_response(
    user_text: str,
    rag_context: str,
    text_emotion: Dict,
    audio_emotion: Optional[Dict],
    cognitive_profile: Dict,
    risk_level: str,
    mode: str
) -> str:
    """
    Final response orchestrator.

    This is the SINGLE place where:
    - RAG is enforced
    - Mode is enforced
    - Safety is enforced
    - Non-diagnostic behavior is guaranteed

    ❌ Not for adaptive assessment
    """

    # --------------------------------------------------
    # 🧪 GUARD AGAINST MISUSE DURING ASSESSMENT
    # --------------------------------------------------
    if mode.lower().startswith("assessment"):
        raise RuntimeError(
            "llm_orchestrator.generate_final_response() "
            "must NOT be called during adaptive assessment."
        )

    # --------------------------------------------------
    # 🔒 SAFETY OVERRIDE
    # --------------------------------------------------
    if risk_level in {"HIGH", "CRITICAL"}:
        mode = "💙 Emotional Support (Non-clinical)"

    # --------------------------------------------------
    # 📚 GUARANTEED RAG CONTEXT
    # --------------------------------------------------
    if not rag_context or len(rag_context.strip()) < 10:
        rag_context = retrieve_context(
            user_text + " " + " ".join(cognitive_profile.keys())
        )

    # --------------------------------------------------
    # 🧠 EMOTION FUSION (ONLY FOR 💙 MODE)
    # --------------------------------------------------
    emotion_context = {}
    if mode.startswith("💙"):
        emotion_context = {
            "text": text_emotion,
            "audio": audio_emotion or {}
        }

    # --------------------------------------------------
    # 🎭 MODE-BASED SYSTEM STYLE
    # --------------------------------------------------
    if mode.startswith("💙"):
        system_style = """
You are a calm, empathetic, NON-CLINICAL emotional support assistant.

RULES:
- Reflect emotions gently
- Explain why you think this
- Offer grounding suggestions
- NEVER diagnose
- NEVER label disorders
- NEVER give medical advice
"""
    else:
        system_style = """
You are a PROFESSIONAL CAREER GUIDANCE assistant.

STRICT RULES:
- Do NOT discuss emotions
- Do NOT mention mental health
- Focus ONLY on:
  - cognitive strengths
  - skills
  - learning ability
  - career paths
  - improvement plans
- Be structured, factual, and practical
"""

    # --------------------------------------------------
    # 🧩 STRUCTURED PROMPT (JUDGE-FRIENDLY)
    # --------------------------------------------------
    prompt = (
        system_style
        + "\n\nUser input:\n"
        + user_text
        + "\n\nDetected emotional signals:\n"
        + str(emotion_context)
        + "\n\nCognitive profile:\n"
        + str(cognitive_profile)
        + "\n\nRelevant background knowledge:\n"
        + str(rag_context)
        + "\n\nRespond with:\n"
        + "1. Clear understanding of the user's state\n"
        + "2. Why you think this (signals, behavior)\n"
        + "3. Mode-appropriate guidance\n"
        + "4. Safe, non-diagnostic language\n"
    )

    # --------------------------------------------------
    # 🤖 CORE LLM CALL
    # --------------------------------------------------
    response = generate_llm_response(
        user_text=prompt,
        rag_context="",
        emotion=emotion_context,
        cognitive_profile=cognitive_profile
    )

    # --------------------------------------------------
    # ✨ OPTIONAL GEMINI REFINEMENT
    # --------------------------------------------------
    if GEMINI_AVAILABLE:
        try:
            response = refine_with_gemini(response)
        except Exception:
            pass

    return response
