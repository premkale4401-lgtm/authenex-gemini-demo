import librosa
import numpy as np

def load_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=None, mono=True)
    return y, sr

def spectral_features(y, sr):
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    return float(np.mean(centroid)), float(np.mean(bandwidth))

def pitch_variance(y, sr):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    if len(pitch_values) == 0:
        return 0.0
    return float(np.var(pitch_values))

def zero_crossing_rate(y):
    return float(np.mean(librosa.feature.zero_crossing_rate(y)))
