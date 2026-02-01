# Authenex – Gemini-Powered Digital Trust Engine

Authenex is an explainable AI-powered forensic backend that verifies whether
digital images are **real, AI-generated, or manipulated**.

The system combines **Gemini Vision–based structured forensic reasoning**
with a **deterministic trust-scoring engine**, ensuring that every verdict
is **transparent, auditable, and human-understandable**.

This project is designed as a **hackathon-ready demo** with a clear path
toward enterprise-grade digital trust systems.

---

## 🔍 What This Demo Does

1. Accepts an uploaded image
2. Performs multimodal forensic analysis using **Gemini Vision**
3. Extracts category-level signals (texture, lighting, anatomy, etc.)
4. Computes a **Trust Score** using Authenex’s own logic
5. Returns a **clear verdict with explanations**

Gemini provides **evidence**,  
Authenex makes the **final decision**.

---

## 🧠 Key Principles

- No black-box verdicts
- Explainable category-level reasoning
- Deterministic trust scoring
- Safe fallback behavior (never crashes)
- Production-aligned architecture

---

## 🧱 Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini Vision
- **Reasoning**: Structured forensic schema
- **Scoring**: Rule-based trust engine
- **Secrets**: Environment variables
- **Version Control**: Git & GitHub

---

## 📂 Project Structure

```text
authenex-gemini-demo/
├── main.py
├── core/
│   ├── trust_engine.py
│   └── explainability.py
├── services/
│   └── gemini_forensics.py
├── utils/
│   └── file_utils.py
├── uploads/        # local only (git-ignored)
├── .gitignore
└── README.md
```

git clone https://github.com/YOUR_USERNAME/authenex-gemini-demo.git
cd authenex-gemini-demo
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn python-multipart python-dotenv pillow google-generativeai
notepad .env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

Start the Backend Server
uvicorn main:app --reload

If successful, you will see:
Application startup complete.

http://127.0.0.1:8000/docs
