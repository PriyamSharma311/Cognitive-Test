# src/assessment/reasoning_llm_generator.py

import json
import uuid
from typing import List
from src.rag.llm_generator import generate_llm_response


LEVEL_DEFINITIONS = {
    1: "Primary school level (Classes 1–5). Simple counting, basic patterns, obvious logic.",
    2: "Middle/high school level (Classes 6–12). Sequences, verbal reasoning, basic deductions.",
    3: "Post-graduate level. Complex analytical and multi-step logical reasoning.",
    4: "Competitive exams (CAT/GMAT/UPSC). Data sufficiency, syllogisms, traps.",
    5: "Elite (Stanford/Ivy). Abstract reasoning, lateral thinking, deep logic puzzles."
}


FORBIDDEN_OPTIONS = {
    "all of the above",
    "none of the above",
    "cannot be determined",
    "insufficient information",
}


def _is_valid_question(q: dict) -> bool:
    """Strict validation to block vague / unusable questions"""
    if not all(k in q for k in ("question", "options", "answer")):
        return False

    if not isinstance(q["options"], list) or len(q["options"]) != 4:
        return False

    options_lower = [o.strip().lower() for o in q["options"]]
    if any(opt in FORBIDDEN_OPTIONS for opt in options_lower):
        return False

    if q["answer"] not in q["options"]:
        return False

    return True


def generate_reasoning_batch(level: int, count: int = 20) -> List[dict]:
    """
    Generates EXACTLY `count` valid reasoning questions for a given level.
    Retries internally. Fails HARD if cannot satisfy requirements.
    """

    assert level in LEVEL_DEFINITIONS, "Invalid reasoning level"

    questions = []
    seen_questions = set()
    attempts = 0
    MAX_ATTEMPTS = count * 10  # generous retry buffer

    while len(questions) < count and attempts < MAX_ATTEMPTS:
        attempts += 1

        prompt = f"""
You are an Adaptive Cognitive Assessment Engine.

Generate ONE reasoning MCQ.

Difficulty Tier:
Level {level}: {LEVEL_DEFINITIONS[level]}

STRICT RULES:
- Return ONLY valid JSON (no markdown, no explanation)
- Exactly 4 options
- Exactly 1 objectively correct answer
- NO vague options
- NO "all of the above", "none", or similar
- Question must be solvable logically
- No trick wording
- Unique question

JSON format:
{{
  "question": "string",
  "options": ["A", "B", "C", "D"],
  "answer": "exact option text"
}}
"""

        try:
            raw = generate_llm_response(prompt)
            raw = raw.strip().replace("```json", "").replace("```", "")
            data = json.loads(raw)

            if not _is_valid_question(data):
                continue

            normalized_q = data["question"].strip().lower()
            if normalized_q in seen_questions:
                continue

            seen_questions.add(normalized_q)

            questions.append({
                "id": str(uuid.uuid4()),
                "level": level,
                "question": data["question"].strip(),
                "options": [opt.strip() for opt in data["options"]],
                "answer": data["answer"].strip()
            })

        except Exception:
            continue

    if len(questions) < count:
        raise RuntimeError(
            f"❌ Failed to generate enough Level {level} questions "
            f"({len(questions)} / {count}). Increase retries or check LLM output."
        )

    return questions
