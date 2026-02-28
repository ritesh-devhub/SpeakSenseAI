import whisper
from video_processor import AUDIO_DIR
from pathlib import Path
import re

model = whisper.load_model("base")

def transcribe_audio(video_filename):
    video_path = Path(video_filename)
    audio_path = Path(AUDIO_DIR) / f"{video_path.stem}/audio.wav"
    result = model.transcribe(str(audio_path))
    return(result["text"])


# Filler words 
FILLER_WORDS = ["um", "uh", "like", "basically", "actually", "so", "er", "you know", "i mean", "indeed", "in fact", "of course", "certainly", "absolutely", "in other words", "moreover", "for example","essentially"]

def compute_filler_rate(transcript, duration):

    words = transcript.lower().split()
    filler_count = sum(words.count(f) for f in FILLER_WORDS)

    minutes = duration / 60 
    if minutes == 0:
        return 0
    return filler_count / minutes


# Lexical diversity -> vocab

def compute_lexical_diversity(transcript):

    words = transcript.lower().split()
    if len(words) == 0:
        return 0
    unique_words = len(set(words))

    return unique_words / len(words)


def compute_avg_sentence_length(transcript):
    sentences = re.split(r"[!.?]+", transcript)

    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]

    if len(sentences) == 0:
        return 0
    
    word_counts = [len(s.split()) for s in sentences]

    return sum(word_counts) / len(word_counts)


def analyze_nlp(transcript, duration_seconds):
    filler_rate = compute_filler_rate(transcript, duration_seconds)
    lexical_diversity = compute_lexical_diversity(transcript)
    avg_sentence_length = compute_avg_sentence_length(transcript)

    return{
        "filler_rate": round(filler_rate, 2), 
        "lexical_diversity": round(lexical_diversity, 2),
        "avg_sentence_length": round(avg_sentence_length, 2)
    }
