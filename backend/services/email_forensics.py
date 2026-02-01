import re
from services.text_forensics import analyze_text

PHISHING_KEYWORDS = [
    "urgent",
    "immediately",
    "verify",
    "suspended",
    "restricted",
    "action required",
    "confirm your account",
    "reset password",
    "security alert",
    "unusual activity",
    "click below"
]

def analyze_email(email_text: str) -> dict:
    ai_score = 25
    findings = []

    lowered = email_text.lower()

    # 1️⃣ Phishing keyword detection
    for keyword in PHISHING_KEYWORDS:
        if keyword in lowered:
            ai_score += 8
            findings.append(f"Urgency or phishing keyword detected: '{keyword}'")

    # 2️⃣ Link detection
    links = re.findall(r"http[s]?://\S+", email_text)
    if links:
        ai_score += 15
        findings.append("External links detected in email body")

    # 3️⃣ Credential request detection
    if any(word in lowered for word in ["password", "otp", "pin", "login", "credentials"]):
        ai_score += 20
        findings.append("Credential-related request detected")

    # 4️⃣ Reuse text forensics
    text_result = analyze_text(email_text)
    ai_score += int(text_result["aiPercentage"] * 0.3)

    findings.extend(text_result["findings"])

    return {
        "aiPercentage": min(ai_score, 95),
        "categoryScores": {
            "phishing_keywords": sum(1 for k in PHISHING_KEYWORDS if k in lowered),
            "external_links": len(links),
            "text_ai_risk": text_result["aiPercentage"]
        },
        "findings": findings or ["No strong phishing indicators detected"]
    }
