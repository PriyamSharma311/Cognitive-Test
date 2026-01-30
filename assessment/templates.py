import random


# --------------------------------------------------
# REASONING
# --------------------------------------------------
def generate_reasoning(difficulty: str) -> dict:
    if difficulty == "easy":
        a, b = random.randint(1, 9), random.randint(1, 9)
        return {
            "question": f"What is {a} + {b}?",
            "options": [
                str(a + b),
                str(a + b + 1),
                str(a + b - 1),
                str(a + b + 2)
            ],
            "answer": str(a + b)
        }

    if difficulty == "medium":
        seq = [2, 4, 6]
        return {
            "question": f"What comes next in the sequence: {seq}?",
            "options": ["8", "6", "10", "4"],
            "answer": "8"
        }

    return {
        "question": "If A > B and B > C, which is largest?",
        "options": ["A", "B", "C", "None"],
        "answer": "A"
    }


# --------------------------------------------------
# MEMORY
# --------------------------------------------------
def generate_memory(difficulty: str) -> dict:
    length = 3 if difficulty == "easy" else 5
    seq = random.sample(range(1, 10), length)
    index = random.randint(0, length - 1)

    return {
        "question": f"Remember this sequence: {seq}. What was the {index + 1} number?",
        "options": [
            str(seq[index]),
            "0",
            "9",
            "None"
        ],
        "answer": str(seq[index])
    }


# --------------------------------------------------
# ATTENTION
# --------------------------------------------------
def generate_attention(difficulty: str) -> dict:
    symbols = ["@", "@", "#", "@"] if difficulty == "easy" else ["*", "*", "%", "*"]
    correct = next(s for s in symbols if symbols.count(s) == 1)

    return {
        "question": "Which symbol is different?",
        "options": symbols,
        "answer": correct
    }


# --------------------------------------------------
# LANGUAGE
# --------------------------------------------------
def generate_language(difficulty: str) -> dict:
    return {
        "question": "Which sentence means the same as: 'He arrived early'?",
        "options": [
            "He came before time",
            "He was late",
            "He delayed arrival",
            "He missed the event"
        ],
        "answer": "He came before time"
    }


# --------------------------------------------------
# EXECUTIVE
# --------------------------------------------------
def generate_executive(difficulty: str) -> dict:
    return {
        "question": "What should you do first when many tasks are pending?",
        "options": [
            "Prioritize tasks",
            "Ignore deadlines",
            "Do easiest task",
            "Delay all"
        ],
        "answer": "Prioritize tasks"
    }
