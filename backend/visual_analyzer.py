import cv2
import mediapipe as mp
import os
import numpy as np
import math

mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_mesh

# distance between 2 points
def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def analyze_frames(frames_dir):
    pose = mp_pose.Pose()
    face_mesh = mp_face.FaceMesh()

    total_frames = 0
    frames_looking_forward = 0
    frames_face_centered = 0
    spine_angles = []
    yaw_values = []
    pitch_values = []
    roll_values = []

    for frame_file in sorted(os.listdir(frames_dir)):
        if not frame_file.endswith(".jpg"):
            continue

        total_frames += 1

        frame_path = os.path.join(frames_dir, frame_file)
        image = cv2.imread(frame_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape

        pose_results = pose.process(rgb)
        face_results = face_mesh.process(rgb)

        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark

            # Shoulders + Hips
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            left_hip = landmarks[23]
            right_hip = landmarks[24]

            # Compute spine midpoint
            shoulder_mid = np.array([
                (left_shoulder.x + right_shoulder.x) / 2,
                (left_shoulder.y + right_shoulder.y) / 2
            ])

            hip_mid = np.array([
                (left_hip.x + right_hip.x) / 2,
                (left_hip.y + right_hip.y) / 2
            ])
            dx = shoulder_mid[0] - hip_mid[0]
            dy = shoulder_mid[1] - hip_mid[1]

            angle = np.degrees(np.arctan2(dx, dy))

            angle = abs(angle)

            

            spine_angles.append(angle)

        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0].landmark

            # Nose landmark (index 1)
            nose = face_landmarks[1]

            # Face centered check
            if 0.4 < nose.x < 0.6:
                frames_face_centered += 1

            # Eye contact approx
            # If nose roughly centered horizontally
            if 0.45 < nose.x < 0.55:
                frames_looking_forward += 1

            # Head Rotation Trio
            left_ear = face_landmarks[234]
            right_ear = face_landmarks[454]

            # Yaw
            center_x = (left_ear.x + right_ear.x) / 2
            yaw = nose.x - center_x
            face_width = abs(left_ear.x - right_ear.x)

            yaw_normalized = yaw / face_width
            yaw_values.append(yaw_normalized)

            # Pitch
            left_eye = face_landmarks[33]
            right_eye = face_landmarks[263]

            eye_center_y = (left_eye.y + right_eye.y) / 2
            pitch_value = nose.y - eye_center_y

            chin = face_landmarks[152]

            face_height = abs(chin.y - eye_center_y)

            pitch_normalized = (pitch_value) / face_height
            pitch_values.append(pitch_normalized)

            # Roll
            left_x, left_y = (left_ear.x * w), (left_ear.y * h)
            right_x, right_y = (right_ear.x * w), (right_ear.y * h)

            dx = right_x - left_x
            dy = right_y - left_y

            roll_angle = math.degrees(math.atan2(dy, dx))
            roll_values.append(roll_angle)



    # Final Metrics
    eye_contact_percentage = frames_looking_forward * 100 / total_frames if total_frames else 0
    face_center_ratio = frames_face_centered / total_frames if total_frames else 0
    posture_stability = np.std(spine_angles) if spine_angles else 0
    yaw_variance = np.std(yaw_values) if yaw_values else 0
    pitch_variance = np.std(pitch_values) if pitch_values else 0
    roll_variance = np.std(roll_values) if roll_values else 0

    

    return {
        "eye_contact_ratio": eye_contact_percentage,
        "face_center_ratio": face_center_ratio,
        "posture_stability": posture_stability,
        "yaw_variance":yaw_variance,
        "pitch_variance": pitch_variance,
        "roll_variance": roll_variance
    }
