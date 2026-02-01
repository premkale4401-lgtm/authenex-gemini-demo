import os
import shutil
from fastapi import UploadFile

# --------------------------------------------------
# Save uploaded file safely
# --------------------------------------------------

def save_upload_file(upload_file: UploadFile, upload_dir: str) -> str:
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, upload_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


# --------------------------------------------------
# Determine file type based on extension
# --------------------------------------------------

def get_file_type(filename: str) -> str:
    ext = filename.lower().split(".")[-1]

    if ext in ["jpg", "jpeg", "png", "webp"]:
        return "image"
    elif ext in ["mp4", "mov", "avi", "mkv"]:
        return "video"
    elif ext in ["mp3", "wav", "aac"]:
        return "audio"
    elif ext in ["pdf", "docx"]:
        return "document"
    else:
        return "unknown"
