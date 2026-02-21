from video_processor import process_video
from visual_analyzer import analyze_frames
import json

if __name__ == "__main__":
    video_name = input("Enter filename: ").strip()  # must exist inside uploads/
    result = process_video(video_name)

    print("\n📊 Processing Complete")
    print(json.dumps(result, indent=4))

    frame_path = result['frames_path']
    result = analyze_frames(frame_path)

    print(result)