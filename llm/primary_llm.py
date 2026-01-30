from src.adaptive_response.empathy_prompt import build_empathy_prompt
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_primary_response(
    user_text,
    rag_context,
    emotion,
    cognitive_profile,
    risk_level
):
    prompt = build_empathy_prompt(
        user_text=user_text,
        rag_context=rag_context,
        emotion=emotion,
        cognitive_profile=cognitive_profile,
        risk_level=risk_level
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
