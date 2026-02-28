import librosa
import numpy as np
from pathlib import Path
from video_processor import AUDIO_DIR

# BASIC
def load_audio(audio_path):
    # return wave form & sample rate
    y, sr = librosa.load(audio_path, sr=None)
    return y, sr

def get_audio_duration(y, sr):
    return librosa.get_duration(y=y, sr=sr)


# WORDS PER MINUTE
def compute_wpm(transcript, duration_seconds):
    words = transcript.split()
    total_words = len(words)
    minutes = duration_seconds / 60
    if minutes == 0:
        return 0
    return total_words / minutes

# PITCH VARIANCE
def compute_pitch_variance(y, sr):
    f0, _, _ = librosa.pyin(
        y,
        fmin=75,    # lowest expected human pitch
        fmax=350    # highest expected human pitch
    )

    # Remove unvoiced frames (NaN values)
    pitch_values = f0[~np.isnan(f0)]

    if len(pitch_values) < 10:
        return 0

    pitch_mean = np.mean(pitch_values)
    pitch_std = np.std(pitch_values)

    pitch_cv = pitch_std / (pitch_mean + 1e-6)

    return round(float(pitch_cv), 4)

# VOLUME VARIANCE
def compute_volume_variance(y):
    rms = librosa.feature.rms(y=y)[0]
    return np.var(rms)

# PAUSE DETECTION
def compute_pause_metrics(y, sr, silence_threshold=0.01, min_pause_sec=0.5):
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)

    silent_frames = rms < silence_threshold

    pause_durations = []
    current_pause_start = None

    for i, silent in enumerate(silent_frames):
        if silent and current_pause_start is None:
            current_pause_start = times[i]

        elif not silent and current_pause_start is not None:
            duration = times[i] - current_pause_start
            if duration >= min_pause_sec:
                pause_durations.append(duration)
            current_pause_start = None

    if not pause_durations:
        return 0, 0

    total_pause_time = sum(pause_durations)
    total_duration = librosa.get_duration(y=y, sr=sr)

    long_pause_ratio = total_pause_time / total_duration
    avg_pause_duration = np.mean(pause_durations)

    return long_pause_ratio, avg_pause_duration


# MAIN FUNCTION
def analyze_audio(video_filename, transcript=""):
    video_path = Path(video_filename)
    audio_path = Path(AUDIO_DIR) / f"{video_path.stem}/audio.wav"
    y, sr = load_audio(audio_path)
    duration = get_audio_duration(y, sr)

    wpm = compute_wpm(transcript, duration)
    pitch_cv = compute_pitch_variance(y, sr)
    volume_variance = compute_volume_variance(y)
    long_pause_ratio, avg_pause_duration = compute_pause_metrics(y, sr)

    return {
        "duration_seconds": duration,
        "words_per_minute": round(wpm, 2),
        "pitch_cv": round(pitch_cv, 4),
        "volume_variance": round(volume_variance, 4),
        "long_pause_ratio": round(long_pause_ratio, 4),
        "avg_pause_duration": round(avg_pause_duration, 3)
    }