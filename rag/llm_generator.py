"""
llm_generator.py
Central LLM call used everywhere in the app
Groq-backed (free, fast)
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# =====================================================
# LOAD .env FROM app/ (DO NOT MOVE IT)
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / "app" / ".env"

load_dotenv(dotenv_path=ENV_PATH)

# =====================================================
# API KEY
# =====================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a non-clinical cognitive question generator.
Return ONLY valid JSON when asked.
"""

def generate_llm_response(
    user_text: str,
    rag_context: str = "",
    emotion: dict | None = None,
    cognitive_profile: dict | None = None
) -> str:

    prompt = f"""
{user_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
