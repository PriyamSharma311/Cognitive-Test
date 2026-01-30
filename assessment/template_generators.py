import random


# -----------------------------
# Reasoning generators
# -----------------------------
def reasoning_sequence(length: int, difficulty: str = "easy"):
    start = random.randint(1, 5)
    step = random.randint(1, 4)

    sequence = [start + i * step for i in range(length)]
    answer = start + length * step

    distractors = [answer + i for i in (-2, -1, 1, 2)]
    options = random.sample(distractors + [answer], 4)

    return {
        "question": f"What number comes next in the sequence: {', '.join(map(str, sequence))}?",
        "options": list(map(str, options)),
        "answer": str(answer)
    }


# -----------------------------
# Memory generators
# -----------------------------
def memory_recall(length: int):
    items = random.sample(range(10, 99), length)
    answer = " ".join(map(str, items))

    options = [answer]
    for _ in range(3):
        options.append(" ".join(map(str, random.sample(range(10, 99), length))))

    random.shuffle(options)

    return {
        "question": f"Remember these numbers: {' '.join(map(str, items))}. What were they?",
        "options": options,
        "answer": answer
    }


# -----------------------------
# Attention generators
# -----------------------------
def attention_odd_one():
    symbols = random.sample(list("ABCDEFGHJKLMNPQRSTUVWXYZ"), 4)
    odd = random.choice(symbols)

    return {
        "question": "Which symbol is different from the others?",
        "options": symbols,
        "answer": odd
    }


# -----------------------------
# Language generators
# -----------------------------
def language_sentence():
    correct = "She finished her work before the deadline."

    options = [
        correct,
        "She work finish deadline.",
        "She deadline finish work.",
        "She finishing work deadline."
    ]

    random.shuffle(options)

    return {
        "question": "Choose the sentence that best completes the meaning.",
        "options": options,
        "answer": correct
    }


# -----------------------------
# Executive function generators
# -----------------------------
def executive_priority():
    correct = "Complete the most urgent and important task"

    options = [
        correct,
        "Do the easiest task first",
        "Delay all tasks",
        "Work randomly without planning"
    ]

    random.shuffle(options)

    return {
        "question": "You have multiple tasks and limited time. What should you do first?",
        "options": options,
        "answer": correct
    }
