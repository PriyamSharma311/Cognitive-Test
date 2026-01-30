import json
import os
from datetime import datetime

STORE_PATH = "src/emotion/emotion_history.json"


def load_emotion_history():
    if not os.path.exists(STORE_PATH):
        return []
    with open(STORE_PATH, "r") as f:
        return json.load(f)


def save_emotion(history):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, "w") as f:
        json.dump(history, f, indent=2)


def append_emotion(state: str):
    history = load_emotion_history()
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "state": state
    })
    save_emotion(history)
    return history
