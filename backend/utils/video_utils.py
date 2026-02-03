import cv2
import os

def extract_frames(video_path: str, output_dir: str, every_n_seconds=1):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        return []

    frame_interval = int(fps * every_n_seconds)
    frames = []

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_path = os.path.join(
                output_dir, f"frame_{saved_count}.jpg"
            )
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
            saved_count += 1

        frame_count += 1

    cap.release()
    return frames
