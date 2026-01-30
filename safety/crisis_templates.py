# src/safety/crisis_templates.py

def get_crisis_message(level: str) -> str:
    """
    Returns safe, supportive language.
    """

    if level == "CRITICAL":
        return (
            "I’m really glad you shared this. "
            "You don’t have to go through it alone. "
            "If you feel unsafe, please consider reaching out to "
            "a trusted person or local support service."
        )

    if level == "HIGH":
        return (
            "It sounds like things feel heavy right now. "
            "Taking a pause and talking to someone you trust can help."
        )

    return ""
