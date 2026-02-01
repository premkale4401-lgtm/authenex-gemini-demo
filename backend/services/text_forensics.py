from utils.text_utils import (
    sentence_length_variance,
    repetition_score,
    lexical_diversity
)
from services.gemini_text_reasoner import (
    reason_about_text,
    consistency_check
)

def analyze_text(text: str) -> dict:
    # Deterministic signals
    length_var = sentence_length_variance(text)
    repetition = repetition_score(text)
    diversity = lexical_diversity(text)

    # Gemini forensic reasoning
    gemini = reason_about_text(text)
    paraphrase_consistent = consistency_check(text)

    ai_score = 30
    findings = []

    # Deterministic evidence
    if length_var < 8:
        ai_score += 10
        findings.append("Highly uniform sentence structure")

    if repetition > 0.25:
        ai_score += 10
        findings.append("Repetitive phrasing patterns detected")

    if diversity < 0.4:
        ai_score += 10
        findings.append("Low lexical diversity")

    # Gemini forensic signals
    if gemini["ai_structural_patterns"]:
        ai_score += 15
        findings.append("AI-like structural patterns detected")

    if gemini["overly_generic_language"]:
        ai_score += 10
        findings.append("Overly generic phrasing")

    if not gemini["personal_context_present"]:
        ai_score += 10
        findings.append("Lack of personal context")

    if gemini["semantic_predictability"] == "high":
        ai_score += 10
        findings.append("High semantic predictability")

    # Consistency amplification
    if paraphrase_consistent:
        ai_score += 15
        findings.append("High paraphrase consistency (AI-like behavior)")

    return {
        "aiPercentage": min(ai_score, 95),
        "categoryScores": {
            "sentence_variance": round(length_var, 2),
            "repetition": round(repetition, 2),
            "lexical_diversity": round(diversity, 2),
            "semantic_predictability": gemini["semantic_predictability"],
            "paraphrase_consistency": paraphrase_consistent
        },
        "findings": findings,
        "forensic_notes": gemini["forensic_notes"]
    }
