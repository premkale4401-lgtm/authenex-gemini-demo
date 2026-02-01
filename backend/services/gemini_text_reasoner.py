import os
import json
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"

SYSTEM_PROMPT = """
You are a DIGITAL FORENSIC LANGUAGE ANALYST.

Rules:
- You do NOT guess.
- You do NOT give opinions.
- You ONLY report observable linguistic characteristics.

Analyze the given text and return STRICT JSON ONLY
with the following schema:

{
  "ai_structural_patterns": true/false,
  "human_variability_present": true/false,
  "overly_generic_language": true/false,
  "personal_context_present": true/false,
  "semantic_predictability": "low" | "medium" | "high",
  "forensic_notes": "short explanation"
}

DO NOT include any text outside JSON.
"""

def reason_about_text(text: str) -> dict:
    try:
        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(
            [
                {"role": "system", "parts": [SYSTEM_PROMPT]},
                {"role": "user", "parts": [text]}
            ],
            generation_config={"temperature": 0}
        )

        return json.loads(response.text)

    except Exception:
        # Safe fallback
        return {
            "ai_structural_patterns": False,
            "human_variability_present": True,
            "overly_generic_language": False,
            "personal_context_present": True,
            "semantic_predictability": "medium",
            "forensic_notes": "Gemini reasoning unavailable"
        }


def consistency_check(text: str) -> bool:
    """
    Checks if paraphrased text is too similar to original.
    High similarity = AI-like behavior.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)

        paraphrase_prompt = f"""
Paraphrase the following text while preserving meaning:

{text}
"""

        response = model.generate_content(
            paraphrase_prompt,
            generation_config={"temperature": 0.7}
        )

        paraphrase = response.text.lower()
        original = text.lower()

        original_words = set(original.split())
        paraphrase_words = set(paraphrase.split())

        if not original_words:
            return False

        overlap = len(original_words & paraphrase_words) / len(original_words)
        return overlap > 0.75

    except Exception:
        return False
