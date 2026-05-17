import cv2
import numpy as np
import os
import pandas as pd

def high_frequency_score(image_path, radius=30):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude = np.abs(fshift)

    h, w = magnitude.shape
    center_y, center_x = h // 2, w // 2

    mask = np.ones((h, w), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 0, -1)

    high_freq_energy = np.sum(magnitude * mask)
    total_energy = np.sum(magnitude)

    return high_freq_energy / total_energy if total_energy != 0 else 0


def process_folder(folder, output_csv):
    rows = []

    for file in sorted(os.listdir(folder)):
        if not file.endswith(".png"):
            continue

        path = os.path.join(folder, file)
        score = high_frequency_score(path)

        if score is not None:
            rows.append({
                "frame": file,
                "frequency_score": score
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)

    print(f"Saved: {output_csv}")
    print(df["frequency_score"].describe())


process_folder("selected_frames/real", "frequency_scores_real.csv")
process_folder("selected_frames/fake", "frequency_scores_fake.csv")