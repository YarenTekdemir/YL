import os
import csv


def count_frames(folder):
    return len([
        f for f in os.listdir(folder)
        if f.endswith(".png")
    ])


def analyze(original_folder, selected_folder, label):
    original_count = count_frames(original_folder)
    selected_count = count_frames(selected_folder)

    reduction = (
        (original_count - selected_count)
        / original_count
    ) * 100

    print(f"\n--- {label} ---")
    print(f"Original frames : {original_count}")
    print(f"Selected frames : {selected_count}")
    print(f"Reduction       : {reduction:.2f}%")

    return {
        "label": label,
        "original_frames": original_count,
        "selected_frames": selected_count,
        "reduction_percent": round(reduction, 2)
    }


real_result = analyze(
    "frames/real",
    "selected_frames/real",
    "REAL"
)

fake_result = analyze(
    "frames/fake",
    "selected_frames/fake",
    "FAKE"
)

rows = [
    real_result,
    fake_result
]

os.makedirs("results", exist_ok=True)

with open("results/frame_statistics.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "label",
            "original_frames",
            "selected_frames",
            "reduction_percent"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print("\nSaved results/frame_statistics.csv")