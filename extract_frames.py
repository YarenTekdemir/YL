import cv2
import os

def extract_frames(video_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imwrite(f"{output_folder}/frame_{count:04d}.png", frame)
        count += 1

    cap.release()
    print(f"{video_path} -> {count} frames extracted")

# SENİN PATHLER
real_video = r"data\original_sequences\youtube\c23\videos\183.mp4"
fake_video = r"data\manipulated_sequences\Deepfakes\c23\videos\183_253.mp4"

extract_frames(real_video, "frames/real")
extract_frames(fake_video, "frames/fake")