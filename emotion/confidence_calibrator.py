def calibrate_confidence(audio_emotion: dict, audio_conf: float = None):
    """
    Normalizes and safely adjusts emotion confidence.
    """

    if not audio_emotion:
        return audio_emotion

    base_conf = audio_emotion.get("confidence", 0.5)

    # If external confidence not provided, trust model output
    if audio_conf is None:
        audio_emotion["confidence"] = min(max(base_conf, 0.3), 0.95)
        return audio_emotion

    # Fuse both confidences
    fused = 0.6 * base_conf + 0.4 * audio_conf
    audio_emotion["confidence"] = round(min(max(fused, 0.3), 0.95), 2)

    return audio_emotion
