import whisper
from video_processor import AUDIO_DIR
from pathlib import Path

model = whisper.load_model("base")

def transcribe_audio(video_filename):
    video_path = Path(video_filename)
    audio_path = Path(AUDIO_DIR) / f"{video_path.stem}/audio.wav"
    result = model.transcribe(str(audio_path))
    return(result["text"])

