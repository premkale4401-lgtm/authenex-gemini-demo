from utils.document_utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_metadata_pdf,
    extract_metadata_docx,
    file_hash
)
from services.text_forensics import analyze_text

def analyze_document(doc_path: str, file_type: str) -> dict:
    ai_score = 30
    findings = []

    # -----------------------------
    # Extract text & metadata
    # -----------------------------
    if file_type == "pdf":
        text = extract_text_from_pdf(doc_path)
        metadata = extract_metadata_pdf(doc_path)
    else:
        text = extract_text_from_docx(doc_path)
        metadata = extract_metadata_docx(doc_path)

    # -----------------------------
    # Metadata analysis (VERY STRONG)
    # -----------------------------
    creator = str(metadata.get("/Creator", metadata.get("author", ""))).lower()

    if any(tool in creator for tool in ["chatgpt", "openai", "ai", "generator"]):
        ai_score += 30
        findings.append("AI-related authoring tool detected in metadata")

    if not metadata:
        ai_score += 15
        findings.append("Missing or stripped document metadata")

    # -----------------------------
    # Text forensic analysis
    # -----------------------------
    if len(text.strip()) > 200:
        text_result = analyze_text(text)
        ai_score += int(text_result["aiPercentage"] * 0.4)
        findings.extend(text_result["findings"])
    else:
        findings.append("Insufficient text for deep semantic analysis")

    # -----------------------------
    # Structural uniformity (documents)
    # -----------------------------
    paragraphs = [p for p in text.split("\n") if len(p.strip()) > 30]
    avg_len = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)

    if avg_len > 300:
        ai_score += 10
        findings.append("Unusually uniform paragraph structure detected")

    # -----------------------------
    # Final result
    # -----------------------------
    return {
        "aiPercentage": min(ai_score, 95),
        "document_hash": file_hash(doc_path),
        "categoryScores": {
            "metadata_risk": bool(metadata),
            "semantic_ai_risk": text_result["aiPercentage"] if len(text.strip()) > 200 else 0,
            "structure_uniformity": round(avg_len, 2)
        },
        "findings": findings or [
            "No strong indicators of AI-generated or manipulated document"
        ]
    }
