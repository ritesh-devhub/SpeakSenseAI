# NORMALIZE THE METRICS

def min_max_normalize(value, min_val, max_val, invert=False):
    """
    invert=True -> lower value is better 
    """
    if value <= min_val:
        score = 0
    elif value >= max_val:
        score = 100
    else:
        score = ((value - min_val) / (max_val - min_val)) * 100

    if invert:
        score = 100 - score
    
    return round(float(score), 2)


# normalize visual metrics
def normalize_visual_metrics(v):

    return {
        "eye_contact_score":min_max_normalize(v['eye_contact_ratio'], 40, 80),

        "face_center_score":min_max_normalize(v['face_center_ratio'], 0.6, 1.0),

        "posture_stability_score":min_max_normalize(v['posture_stability'], 0, 5, invert=True),

        "yaw_variance_score":min_max_normalize(v['yaw_variance'], 0, 0.2, invert=True),

        "roll_variance_score":min_max_normalize(v['roll_variance'], 0, 5, invert=True),
    }

# normalize audio metrics
def normalize_audio_metrics(a):

    return {
        "wpm_score": min_max_normalize(
            a["words_per_minute"], 100, 190
        ),

        "pitch_cv_score": min_max_normalize(
            a["pitch_cv"], 0.05, 0.25
        ),

        "volume_stability_score": min_max_normalize(
            a["volume_variance"], 0, 0.01, invert=True
        ),

        "pause_ratio_score": min_max_normalize(
            a["long_pause_ratio"], 0, 0.3, invert=True
        )
    }  

# Normalize NLP metrics 
def normalize_nlp_metrics(n):
    return{
        "filler_score": min_max_normalize(n['filler_rate'], 0, 6, invert=True),

        "lexical_score": min_max_normalize(n['lexical_diversity'], 0.3, 0.6),

        "sentence_structure_score": min_max_normalize(n['avg_sentence_length'], 8, 20)
    }  


