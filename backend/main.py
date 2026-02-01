import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime

from services.gemini_forensics import analyze_image
from services.text_forensics import analyze_text
from services.email_forensics import analyze_email

from core.trust_engine import compute_trust
from core.explainability import generate_explanation
from utils.file_utils import save_upload_file, get_file_type

# --------------------------------------------------
# App setup
# --------------------------------------------------

load_dotenv()

app = FastAPI(
    title="Authenex – Digital Trust Engine",
    description="Explainable AI system for detecting AI-generated and manipulated content",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Authenex backend is running",
        "supported_endpoints": [
            "/analyze (image)",
            "/analyze-text (AI text)",
            "/analyze-email (phishing email)"
        ]
    }

# --------------------------------------------------
# IMAGE ANALYSIS (EXISTING – DO NOT BREAK)
# --------------------------------------------------

@app.post("/analyze")
async def analyze_image_api(file: UploadFile = File(...)):
    # Validate file type
    file_type = get_file_type(file.filename)
    if file_type != "image":
        raise HTTPException(
            status_code=415,
            detail="This endpoint currently supports image analysis only"
        )

    # Save file
    file_path = save_upload_file(file, UPLOAD_DIR)

    # Run image forensics
    data = analyze_image(file_path)

    # Trust computation
    trust_score, verdict, ai_prob, data = compute_trust(data)
    explanation = generate_explanation(data, ai_prob)

    return {
        "file_name": file.filename,
        "file_type": "image",
        "trust_score": trust_score,
        "deepfake_probability": ai_prob,
        "verdict": verdict,
        "explanation": explanation,
        "details": data,
        "analyzed_at": datetime.utcnow().isoformat() + "Z"
    }

# --------------------------------------------------
# TEXT ANALYSIS (AI-GENERATED TEXT)
# --------------------------------------------------

@app.post("/analyze-text")
async def analyze_text_api(payload: dict):
    text = payload.get("text", "").strip()

    if len(text) < 50:
        raise HTTPException(
            status_code=400,
            detail="Text too short for reliable analysis"
        )

    # Run text forensics
    data = analyze_text(text)

    # Trust computation
    trust_score, verdict, ai_prob, data = compute_trust(data)
    explanation = generate_explanation(data, ai_prob)

    return {
        "content_type": "text",
        "trust_score": trust_score,
        "deepfake_probability": ai_prob,
        "verdict": verdict,
        "explanation": explanation,
        "details": data,
        "analyzed_at": datetime.utcnow().isoformat() + "Z"
    }

# --------------------------------------------------
# EMAIL ANALYSIS (PHISHING / FAKE EMAILS)
# --------------------------------------------------

@app.post("/analyze-email")
async def analyze_email_api(payload: dict):
    email_text = payload.get("email", "").strip()

    if len(email_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="Email content too short for analysis"
        )

    # Run email forensics
    data = analyze_email(email_text)

    # Trust computation
    trust_score, verdict, ai_prob, data = compute_trust(data)
    explanation = generate_explanation(data, ai_prob)

    return {
        "content_type": "email",
        "trust_score": trust_score,
        "deepfake_probability": ai_prob,
        "verdict": verdict,
        "explanation": explanation,
        "details": data,
        "analyzed_at": datetime.utcnow().isoformat() + "Z"
    }
