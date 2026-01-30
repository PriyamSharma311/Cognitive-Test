# scripts/generate_reasoning_bank.py

import json

# src/assessment/reasoning_bank.py

import json
from pathlib import Path

# --------------------------------------------------
# BANK LOCATION
# --------------------------------------------------
BANK_PATH = Path("data/reasoning_bank.json")


def load_reasoning_bank():
    """
    Loads the pre-generated reasoning question bank.

    Structure:
    {
      "1": [20 questions],
      "2": [20 questions],
      ...
      "5": [20 questions]
    }
    """

    if not BANK_PATH.exists():
        raise FileNotFoundError(
            f"❌ Reasoning bank not found at {BANK_PATH.resolve()}. "
            "Run scripts/generate_reasoning_bank.py first."
        )

    with open(BANK_PATH, "r") as f:
        bank = json.load(f)

    return bank


from src.assessment.reasoning_llm_generator import generate_reasoning_batch

BANK_PATH = Path("data/reasoning_bank.json")
QUESTIONS_PER_LEVEL = 20
LEVELS = [1, 2, 3, 4, 5]


def main():
    print("🔄 Generating reasoning question bank...\n")

    bank = {}

    for level in LEVELS:
        print(f"▶ Generating Level {level} questions...")
        questions = generate_reasoning_batch(level=level, count=QUESTIONS_PER_LEVEL)
        bank[str(level)] = questions
        print(f"✅ Level {level}: {len(questions)} questions generated")

    BANK_PATH.parent.mkdir(exist_ok=True)
    BANK_PATH.write_text(json.dumps(bank, indent=2))

    print("\n🎉 Reasoning bank generated successfully!")
    print(f"📁 Saved at: {BANK_PATH.resolve()}")


if __name__ == "__main__":
    main()
