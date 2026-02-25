from video_processor import process_video
from visual_analyzer import analyze_frames
from audio_analyzer import analyze_audio
from nlp_analyzer import transcribe_audio
import json

if __name__ == "__main__":
    video_name = input("Enter filename: ").strip()  # must exist inside uploads/
    result = process_video(video_name)

    print("\n📊 Processing Complete")
    print(json.dumps(result, indent=4))

    frame_path = result['frames_path']
    visual_metrics = analyze_frames(frame_path)
    print("\n**********VISUAL METRICS*************\n")
    print(visual_metrics)

    # Speech-2-text -> transcription
    text = transcribe_audio(video_name)
    #print("\nTranscript:\n")
    #print(text)

    audio_metrics = analyze_audio(video_name, text)
    print("\n**********AUDIO METRICS*************\n")
    print(audio_metrics)