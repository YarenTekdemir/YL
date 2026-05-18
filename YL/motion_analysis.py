import cv2
import os
import csv
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_ssim(frame1, frame2):
    """
    Calculates Structural Similarity Index between two grayscale frames.
    High SSIM means frames are very similar.
    Low SSIM means there is more visual change.
    """
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(gray1, gray2, full=True)
    return score


def calculate_optical_flow(frame1, frame2):
    """
    Calculates motion magnitude using Farneback Optical Flow.
    Higher value means stronger motion between two frames.
    """
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(
        gray1,
        gray2,
        None,
        pyr_scale=0.5,
        levels=3,
        winsize=15,
        iterations=3,
        poly_n=5,
        poly_sigma=1.2,
        flags=0
    )

    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    avg_motion = np.mean(magnitude)

    return avg_motion


def analyze_motion(frames_folder, output_csv="motion_scores.csv"):
    """
    Analyzes motion between consecutive frames using SSIM and Optical Flow.
    Saves the result into a CSV file.
    """

    frame_files = sorted([
        file for file in os.listdir(frames_folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if len(frame_files) < 2:
        print(f"Not enough frames for motion analysis in: {frames_folder}")
        return

    results = []

    for i in range(len(frame_files) - 1):
        current_frame_path = os.path.join(frames_folder, frame_files[i])
        next_frame_path = os.path.join(frames_folder, frame_files[i + 1])

        current_frame = cv2.imread(current_frame_path)
        next_frame = cv2.imread(next_frame_path)

        if current_frame is None or next_frame is None:
            print(f"Skipping unreadable frame pair: {frame_files[i]}, {frame_files[i + 1]}")
            continue

        ssim_score = calculate_ssim(current_frame, next_frame)
        motion_score = calculate_optical_flow(current_frame, next_frame)

        results.append({
            "frame_1": frame_files[i],
            "frame_2": frame_files[i + 1],
            "ssim_score": ssim_score,
            "motion_score": motion_score
        })

        print(
            f"{frame_files[i]} -> {frame_files[i + 1]} | "
            f"SSIM: {ssim_score:.4f} | Motion: {motion_score:.4f}"
        )

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["frame_1", "frame_2", "ssim_score", "motion_score"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print(f"\nMotion analysis completed. Results saved to: {output_csv}")


def analyze_motion_auto(base_frames_folder="frames", output_prefix="motion_scores"):
    """
    Analyzes motion from a folder that may contain frames directly
    or class subfolders such as frames/real and frames/fake.
    """
    direct_frame_files = [
        file for file in os.listdir(base_frames_folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(direct_frame_files) >= 2:
        analyze_motion(base_frames_folder, f"{output_prefix}.csv")
        return

    subfolders = sorted([
        folder for folder in os.listdir(base_frames_folder)
        if os.path.isdir(os.path.join(base_frames_folder, folder))
    ])

    analyzed_any = False
    for folder in subfolders:
        folder_path = os.path.join(base_frames_folder, folder)
        frame_files = [
            file for file in os.listdir(folder_path)
            if file.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if len(frame_files) < 2:
            continue

        output_csv = f"{output_prefix}_{folder}.csv"
        analyze_motion(folder_path, output_csv)
        analyzed_any = True

    if not analyzed_any:
        print(
            "No folder with at least 2 image frames was found under "
            f"{base_frames_folder}."
        )


if __name__ == "__main__":
    analyze_motion_auto("frames")