import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOADS_DIR = BASE_DIR / "uploads"
AUDIO_DIR = OUTPUT_DIR / "audio"
FRAMES_DIR = OUTPUT_DIR / "frames"

def process_video(video_filename, fps=5):

    input_path = UPLOADS_DIR / video_filename

    if not input_path.exists():
        raise FileNotFoundError("Video not found in uploads folder!!")
    
    video_name = input_path.stem

    video_audio_dir = AUDIO_DIR / video_name
    video_frames_dir = FRAMES_DIR / video_name

    video_audio_dir.mkdir(parents=True, exist_ok=True)
    video_frames_dir.mkdir(parents=True, exist_ok=True)

    audio_output = video_audio_dir / "audio.wav"

    audio_command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vn",
        str(audio_output)
    ]

    try:
        subprocess.run(audio_command, check=True)
        print("✅ Audio extracted")

    except subprocess.CalledProcessError as e:
        print("Error extracting audio: ", e)

    frame_pattern = video_frames_dir / "frame_%04d.jpg"

    frames_command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vf",
        f"fps={fps}",
        str(frame_pattern)  
    ]

    try:
        subprocess.run(frames_command, check=True)
        print("✅ Frames extracted")

    except subprocess.CalledProcessError as e:
        print("Error extracting frames:", e)

    return {
        "audio_path" : str(audio_output),
        "frames_path" : str(video_frames_dir)
    }


# video_path = input("Enter filename: ").strip()

# result = process_video(video_path)
# print(result)

