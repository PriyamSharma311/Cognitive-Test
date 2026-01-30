import librosa
import numpy as np

def extract_audio_behavior(audio_path: str) -> dict:
    y, sr = librosa.load(audio_path, sr=16000)

    duration = librosa.get_duration(y=y, sr=sr)
    rms = float(np.mean(librosa.feature.rms(y=y)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    pauses = np.mean(librosa.effects.split(y, top_db=30).shape[0])

    return {
        "duration_sec": round(duration, 2),
        "energy": round(rms, 4),
        "speech_rate": round(zcr, 4),
        "tempo": round(float(tempo), 2),
        "pause_density": round(pauses, 2)
    }
