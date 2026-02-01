import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# ---------------------------------------------------------------------
# Load environment variables explicitly (Windows-safe)
# ---------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found. Check backend/.env file")

genai.configure(api_key=API_KEY)

# Strong multimodal reasoning model
model = genai.GenerativeModel("models/gemini-2.5-flash-image")



# ---------------------------------------------------------------------
# Helper: Extract JSON safely from Gemini output
# ---------------------------------------------------------------------

def _extract_json(text: str) -> dict:
    """
    Gemini may wrap JSON with text.
    This extracts the first valid JSON object.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in Gemini response")

    return json.loads(match.group())

# ---------------------------------------------------------------------
# Main forensic analysis function (IMAGE)
# ---------------------------------------------------------------------

def analyze_image(image_path: str) -> dict:
    """
    Uses Gemini for structured forensic reasoning.
    Gemini provides evidence — AUTHENEX decides verdict.
    """

    prompt = """
You are a digital forensic analysis system.

Analyze the provided image for indicators of AI generation
or digital manipulation.

Return your response STRICTLY in the following JSON format:

{
  "aiPercentage": number (0-100),
  "humanPercentage": number (0-100),
  "categoryScores": {
    "texture": number (0-100),
    "lighting": number (0-100),
    "anatomy": number (0-100),
    "background": number (0-100),
    "semantics": number (0-100)
  },
  "findings": [
    "short factual observation",
    "short factual observation"
  ]
}

Rules:
- Percentages must be internally consistent
- Category scores must justify aiPercentage
- Be conservative; avoid absolute certainty
- Do NOT say 'real' or 'fake'
- Do NOT mention AI models or tools
- Findings must be visual or semantic observations only
"""

    try:
        # ✅ CORRECT: Gemini requires PIL.Image, not file buffer
        with Image.open(image_path) as img:
            response = model.generate_content(
                [prompt, img],
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 500
                }
            )

        raw_text = response.text.strip()
        data = _extract_json(raw_text)

        # Schema validation (fail fast if Gemini misbehaves)
        required_keys = {
            "aiPercentage",
            "humanPercentage",
            "categoryScores",
            "findings"
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError("Incomplete forensic JSON returned by Gemini")

        return data

    except Exception as e:
        # 🔒 Fail-safe fallback (demo never crashes)
        return {
            "aiPercentage": 50,
            "humanPercentage": 50,
            "categoryScores": {
                "texture": 50,
                "lighting": 50,
                "anatomy": 50,
                "background": 50,
                "semantics": 50
            },
            "findings": [
                f"Gemini analysis failed safely: {str(e)}"
            ]
        }
