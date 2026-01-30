# src/llm/gemini_refiner.py

import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def refine_with_gemini(text: str) -> str:
    """
    Optional Gemini refinement.
    If Gemini API key is not available, return text unchanged.
    """

    if not GEMINI_API_KEY:
        # Gemini not configured → safely skip
        return text

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Refine the following response with empathetic, supportive language:\n\n{text}"
        )

        return response.text.strip()

    except Exception as e:
        # Fail gracefully
        return text
