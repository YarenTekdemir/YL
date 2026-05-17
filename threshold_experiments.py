import csv
import os


def count_frames(folder):
    return len([f for f in os.listdir(folder) if f.endswith(".png")])


def run_experiment(csv_path, frames_folder, ssim_threshold, motion_threshold):
    selected_frames = set()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            frame_1 = row["frame_1"]
            frame_2 = row["frame_2"]
            ssim_score = float(row["ssim_score"])
            motion_score = float(row["motion_score"])

            if ssim_score < ssim_threshold or motion_score > motion_threshold:
                selected_frames.add(frame_1)
                selected_frames.add(frame_2)

    original_count = count_frames(frames_folder)
    selected_count = len(selected_frames)
    reduction = ((original_count - selected_count) / original_count) * 100

    return original_count, selected_count, reduction


ssim_values = [0.90, 0.95, 0.98]
motion_values = [0.25, 0.30, 0.35, 0.40, 0.45]

rows = []

for label, csv_path, frames_folder in [
    ("REAL", "motion_scores_real.csv", "frames/real"),
    ("FAKE", "motion_scores_fake.csv", "frames/fake"),
]:
    for ssim_t in ssim_values:
        for motion_t in motion_values:
            original, selected, reduction = run_experiment(
                csv_path,
                frames_folder,
                ssim_t,
                motion_t
            )

            rows.append({
                "label": label,
                "ssim_threshold": ssim_t,
                "motion_threshold": motion_t,
                "original_frames": original,
                "selected_frames": selected,
                "reduction_percent": round(reduction, 2)
            })

with open("threshold_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "label",
            "ssim_threshold",
            "motion_threshold",
            "original_frames",
            "selected_frames",
            "reduction_percent"
        ]
    )
    writer.writeheader()
    writer.writerows(rows)

print("Saved threshold_results.csv")