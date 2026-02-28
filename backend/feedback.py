FEEDBACK_MAP = {

    "eye_contact_score": {
        "issue": "Limited eye contact",
        "reason": "When you don’t look at the camera consistently, it feels like you’re not fully connected with the audience. Eye contact builds trust and confidence.",
        "fix": "Practice speaking while focusing directly on the camera lens. Imagine you’re talking to one person and hold that gaze for a few seconds at a time."
    },

    "face_center_score": {
        "issue": "Framing inconsistency",
        "reason": "If your face moves too far from the center, it can feel distracting and slightly unprofessional.",
        "fix": "Position yourself comfortably in the center before recording. Try to keep your head aligned with the frame while speaking."
    },

    "posture_stability_score": {
        "issue": "Unstable posture",
        "reason": "Frequent body movement can reduce the sense of confidence and authority in your delivery.",
        "fix": "Sit or stand with a straight spine and grounded shoulders. Keep movements intentional rather than unconscious."
    },

    "wpm_score": {
        "issue": "Speaking pace needs adjustment",
        "reason": "Your pace affects how engaging and confident you sound. Too slow may lose energy, too fast may reduce clarity.",
        "fix": "Aim for a steady pace of around 130–150 words per minute. Practice with a timer and read short paragraphs aloud to find a natural rhythm."
    },

    "pitch_cv_score": {
        "issue": "Limited vocal variation",
        "reason": "A flat tone can make even strong content feel less engaging. Variation adds emotion and emphasis.",
        "fix": "Highlight key words with slight pitch changes. Try reading a sentence and exaggerating emotion first, then tone it down to a natural level."
    },

    "volume_stability_score": {
        "issue": "Inconsistent volume control",
        "reason": "Sudden changes in loudness can make it harder for listeners to stay focused.",
        "fix": "Maintain a steady speaking volume. Record yourself and listen for sudden drops or spikes, then practice smoothing them out."
    },

    "filler_score": {
        "issue": "Frequent filler words",
        "reason": "Words like 'um', 'uh', and 'like' can weaken clarity and reduce perceived confidence.",
        "fix": "Pause silently instead of filling space. A short pause sounds thoughtful — filler words sound uncertain."
    },

    "lexical_score": {
        "issue": "Limited vocabulary variety",
        "reason": "Repeating similar words can make your message feel less polished and less expressive.",
        "fix": "Expand your word choices. After recording, review your transcript and replace repeated words with stronger alternatives."
    },

    "sentence_structure_score": {
        "issue": "Sentence structure imbalance",
        "reason": "Very short sentences may sound fragmented, while very long ones can feel overwhelming.",
        "fix": "Aim for balanced sentences — clear, structured thoughts with natural pauses between ideas."
    }

}


# Rank metrics
def rank_metrics(visual_scores, audio_scores, nlp_scores):

    combined = {**visual_scores, **audio_scores, **nlp_scores}

    #sort ascending
    sorted_metrics = sorted(combined.items(), key=lambda x:x[1])

    return sorted_metrics


def generate_feedback(visual_scores, audio_scores, nlp_scores):

    ranked = rank_metrics(visual_scores, audio_scores, nlp_scores)

    feedback = []

    # take 3 weakest metric
    weakest_three = ranked[:3]

    for metric, score in weakest_three:
        if metric in FEEDBACK_MAP:
            issue = FEEDBACK_MAP[metric]["issue"]
            reason = FEEDBACK_MAP[metric]["reason"]
            fix = FEEDBACK_MAP[metric]["fix"]

            feedback.append({
                "area": metric,
                "score": round(score,2),
                "growth_area": issue, 
                "why_it_matters": reason,
                "improvement": fix
            })

    return feedback




