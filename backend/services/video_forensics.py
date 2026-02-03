import os
import statistics
from services.gemini_forensics import analyze_image
from utils.video_utils import extract_frames

def analyze_video(video_path: str) -> dict:
    frames_dir = "uploads/frames"
    frames = extract_frames(video_path, frames_dir, every_n_seconds=1)

    if len(frames) < 3:
        return {
            "aiPercentage": 50,
            "findings": ["Insufficient frames for reliable analysis"],
            "frame_analysis": []
        }

    frame_scores = []
    frame_details = []

    for frame_path in frames:
        try:
            result = analyze_image(frame_path)
            score = result.get("aiPercentage", 50)
            frame_scores.append(score)
            frame_details.append({
                "frame": os.path.basename(frame_path),
                "ai_probability": score
            })
        except Exception:
            continue

    if not frame_scores:
        return {
            "aiPercentage": 50,
            "findings": ["Frame analysis failed"],
            "frame_analysis": []
        }

    avg_score = statistics.mean(frame_scores)
    variance = statistics.pvariance(frame_scores)

    findings = []

    # Temporal inconsistency detection
    if variance > 400:
        avg_score += 15
        findings.append(
            "Significant temporal inconsistency detected across frames"
        )

    if avg_score > 60:
        findings.append("Multiple frames exhibit AI-generated characteristics")

    if avg_score < 35:
        findings.append("Frames show consistent real-world visual patterns")

    return {
        "aiPercentage": min(int(avg_score), 95),
        "categoryScores": {
            "average_frame_ai": round(avg_score, 2),
            "temporal_variance": round(variance, 2),
            "frames_analyzed": len(frame_scores)
        },
        "frame_analysis": frame_details[:10],  # cap for response size
        "findings": findings
    }
