import cv2
import os
import csv
import numpy as np


def compute_optical_flow(frame1, frame2):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(
        gray1,
        gray2,
        None,
        0.5,
        3,
        15,
        3,
        5,
        1.2,
        0
    )

    magnitude, angle = cv2.cartToPolar(
        flow[..., 0],
        flow[..., 1]
    )

    mean_flow = float(np.mean(magnitude))
    max_flow = float(np.max(magnitude))

    threshold = mean_flow + np.std(magnitude)
    moving_pixels = magnitude > threshold
    motion_area_ratio = float(np.sum(moving_pixels) / magnitude.size)

    return mean_flow, max_flow, motion_area_ratio, magnitude


def save_flow_visualization(magnitude, output_path):
    normalized = cv2.normalize(
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    cv2.imwrite(output_path, normalized)


def process_folder(frames_folder, output_csv, visual_folder):
    os.makedirs(visual_folder, exist_ok=True)

    files = sorted([
        f for f in os.listdir(frames_folder)
        if f.endswith(".png")
    ])

    rows = []

    for i in range(len(files) - 1):

        path1 = os.path.join(frames_folder, files[i])
        path2 = os.path.join(frames_folder, files[i + 1])

        frame1 = cv2.imread(path1)
        frame2 = cv2.imread(path2)

        if frame1 is None or frame2 is None:
            continue

        mean_flow, max_flow, motion_area_ratio, magnitude = compute_optical_flow(
            frame1,
            frame2
        )

        rows.append({
            "frame_1": files[i],
            "frame_2": files[i + 1],
            "optical_flow_score": mean_flow,
            "max_optical_flow": max_flow,
            "motion_area_ratio": motion_area_ratio
        })

        visual_path = os.path.join(
            visual_folder,
            f"flow_{i:04d}.png"
        )

        save_flow_visualization(
            magnitude,
            visual_path
        )

        print(
            f"{files[i]} -> {files[i + 1]} : "
            f"mean={mean_flow:.4f}, "
            f"max={max_flow:.4f}, "
            f"area={motion_area_ratio:.4f}"
        )

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "frame_1",
                "frame_2",
                "optical_flow_score",
                "max_optical_flow",
                "motion_area_ratio"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {output_csv}")


process_folder(
    "frames/real",
    "optical_flow_scores_real.csv",
    "optical_flow_visuals/real"
)

process_folder(
    "frames/fake",
    "optical_flow_scores_fake.csv",
    "optical_flow_visuals/fake"
)