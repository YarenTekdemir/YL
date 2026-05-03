import csv
import os
import shutil


def select_frames(csv_path, frames_folder, output_folder,
                  ssim_threshold=0.95, motion_threshold=1.0):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    selected_frames = set()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            frame_1 = row["frame_1"]
            frame_2 = row["frame_2"]
            ssim_score = float(row["ssim_score"])
            motion_score = float(row["motion_score"])

            # seçim mantığı
            if ssim_score < ssim_threshold or motion_score > motion_threshold:
                selected_frames.add(frame_1)
                selected_frames.add(frame_2)

    print(f"Selected {len(selected_frames)} frames")

    # seçilenleri kopyala
    for frame in selected_frames:
        src = os.path.join(frames_folder, frame)
        dst = os.path.join(output_folder, frame)

        if os.path.exists(src):
            shutil.copy(src, dst)

    print("Frame selection completed.")


if __name__ == "__main__":

    # REAL
    select_frames(
        csv_path="motion_scores_real.csv",
        frames_folder="frames/real",
        output_folder="selected_frames/real"
    )

    # FAKE
    select_frames(
        csv_path="motion_scores_fake.csv",
        frames_folder="frames/fake",
        output_folder="selected_frames/fake"
    )