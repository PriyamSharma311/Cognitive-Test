# src/emotion/emotion_tracker.py

def update_emotion_history(
    session_state,
    emotion_state: str
):
    if "emotion_history" not in session_state:
        session_state.emotion_history = []

    session_state.emotion_history.append(emotion_state)

    # Keep last 10
    session_state.emotion_history = session_state.emotion_history[-10:]


def summarize_trend(history):
    if not history:
        return "No emotional trend detected yet."

    if history.count("distressed") >= 3:
        return "Repeated distress signals detected over time."

    if history[-1] != history[0]:
        return "Emotional state appears to be changing."

    return "Emotional state appears stable."
