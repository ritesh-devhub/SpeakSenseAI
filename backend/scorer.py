from feedback import generate_feedback


def compute_visual_score(v):

    return round(
        0.35 * v["eye_contact_score"] +
        0.20 * v["face_center_score"] +
        0.20 * v["posture_stability_score"] +
        0.15 * v["yaw_variance_score"] +
        0.10 * v["roll_variance_score"],
        2
    )

def compute_audio_score(a):

    return round(
        0.40 * a["wpm_score"] +
        0.25 * a["pitch_cv_score"] +
        0.20 * a["volume_stability_score"] +
        0.15 * a["pause_ratio_score"],
        2
    )

def compute_nlp_score(n):

    return round(
        0.4 * n['filler_score'] + 
        0.35 * n['lexical_score'] + 
        0.25 * n['sentence_structure_score'], 
        2
    )


def compute_overall_score(visual_score, audio_score, nlp_score):

    return round(
        0.4 * visual_score +
        0.35 * audio_score + 
        0.25 * nlp_score,
        2
    )

def detect_weak_areas(visual_scores, audio_scores):

    combined = {**visual_scores, **audio_scores}    # merge dictionaries
    weakest_metric = min(combined, key=combined.get)    # find key with lowest value

    return weakest_metric



def evaluation(visual_scores, audio_scores, nlp_scores):

    visual_score = compute_visual_score(visual_scores)
    audio_score = compute_audio_score(audio_scores)
    nlp_score = compute_nlp_score(nlp_scores)
    overall_score = compute_overall_score(visual_score, audio_score, nlp_score)

    feedback = generate_feedback(visual_scores, audio_scores, nlp_scores)

    performance_level = classify_performance(overall_score)

    return {
        "visual_score": visual_score,
        "audio_score": audio_score,
        "nlp_score": nlp_score,
        "overall_score": overall_score,
        "performance_level": performance_level,
        "feedback": feedback
    }




def classify_performance(overall_score):
    if overall_score < 40:
        return "Needs significant improvement"
    elif overall_score < 60:
        return "Developing"
    elif overall_score < 80:
        return "Good"
    else:
        return "Excellent"
    
