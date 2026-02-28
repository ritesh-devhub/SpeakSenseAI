from video_processor import process_video
from visual_analyzer import analyze_frames
from audio_analyzer import analyze_audio
from nlp_analyzer import transcribe_audio, analyze_nlp
from feature_engineering import (
    normalize_audio_metrics,
    normalize_visual_metrics,
    normalize_nlp_metrics
)
from scorer import evaluation
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

    # nlp metrics
    duration_seconds = audio_metrics['duration_seconds']
    nlp_metrics = analyze_nlp(text, duration_seconds)


    # normalizing the metrics and score
    visual_scores = normalize_visual_metrics(visual_metrics)
    audio_scores = normalize_audio_metrics(audio_metrics)
    nlp_scores = normalize_nlp_metrics(nlp_metrics)

    # printing the normalized score
    print(visual_scores,"\n")
    print(audio_scores,"\n")
    print(nlp_scores,"\n")


    # Final score 
    final_result = evaluation(visual_scores, audio_scores, nlp_scores)
    print("Final Result: \n")
    print(final_result)