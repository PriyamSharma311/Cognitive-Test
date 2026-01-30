import json
import os
from datetime import datetime

BASE = "user_profiles"

def save_profile(user_id: str, data: dict):
    os.makedirs(BASE, exist_ok=True)
    path = os.path.join(BASE, f"{user_id}.json")

    data["last_updated"] = datetime.utcnow().isoformat()

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_profile(user_id: str):
    path = os.path.join(BASE, f"{user_id}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)
