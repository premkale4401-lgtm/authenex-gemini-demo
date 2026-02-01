def compute_trust(data: dict):
    """
    Computes final trust score and verdict
    using Gemini forensic category scores.
    """

    ai_pct = float(data.get("aiPercentage", 50))
    category = data.get("categoryScores", {})

    # Defensive defaults
    texture = float(category.get("texture", 50))
    lighting = float(category.get("lighting", 50))
    anatomy = float(category.get("anatomy", 50))
    background = float(category.get("background", 50))
    semantics = float(category.get("semantics", 50))

    # Weighted category aggregation (transparent & explainable)
    weighted_ai = (
        0.25 * texture +
        0.20 * lighting +
        0.20 * anatomy +
        0.15 * background +
        0.20 * semantics
    )

    # Final AI probability (Gemini + AUTHENEX logic)
    final_ai_probability = (0.6 * ai_pct) + (0.4 * weighted_ai)

    # Trust score is inverse
    trust_score = int(round(100 - final_ai_probability))

    # Verdict thresholds (conservative, judge-safe)
    if trust_score >= 85:
        verdict = "REAL"
    elif trust_score >= 65:
        verdict = "LIKELY REAL"
    elif trust_score >= 45:
        verdict = "SUSPICIOUS"
    else:
        verdict = "LIKELY AI-GENERATED"

    return trust_score, verdict, final_ai_probability, data
