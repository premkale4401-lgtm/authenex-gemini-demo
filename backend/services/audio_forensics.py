from utils.audio_utils import (
    load_audio,
    spectral_features,
    pitch_variance,
    zero_crossing_rate
)

def analyze_audio(audio_path: str) -> dict:
    y, sr = load_audio(audio_path)

    centroid, bandwidth = spectral_features(y, sr)
    pitch_var = pitch_variance(y, sr)
    zcr = zero_crossing_rate(y)

    ai_score = 30
    findings = []

    # Spectral centroid (AI voices often unnaturally stable)
    if centroid < 2000:
        ai_score += 15
        findings.append("Unnaturally low spectral centroid detected")

    # Bandwidth collapse (common in neural vocoders)
    if bandwidth < 1200:
        ai_score += 15
        findings.append("Compressed spectral bandwidth detected")

    # Pitch smoothness (AI voices lack micro-variation)
    if pitch_var < 50:
        ai_score += 20
        findings.append("Unnaturally smooth pitch contours detected")

    # Zero crossing irregularities
    if zcr < 0.02 or zcr > 0.15:
        ai_score += 10
        findings.append("Abnormal zero-crossing rate detected")

    return {
        "aiPercentage": min(ai_score, 95),
        "categoryScores": {
            "spectral_centroid": round(centroid, 2),
            "spectral_bandwidth": round(bandwidth, 2),
            "pitch_variance": round(pitch_var, 2),
            "zero_crossing_rate": round(zcr, 4)
        },
        "findings": findings or [
            "Audio characteristics consistent with natural human speech"
        ]
    }
