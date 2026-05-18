import os
import csv


def count_images(folder):
    if not os.path.exists(folder):
        return 0

    return len([
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])


def calculate_reduction(total, selected):
    if total == 0:
        return 0
    return (1 - (selected / total)) * 100


def summarize():

    data = []

    datasets = ["real", "fake"]

    for d in datasets:
        total_folder = os.path.join("frames", d)
        selected_folder = os.path.join("selected_frames", d)

        total_count = count_images(total_folder)
        selected_count = count_images(selected_folder)

        reduction = calculate_reduction(total_count, selected_count)

        data.append({
            "dataset": d,
            "total_frames": total_count,
            "selected_frames": selected_count,
            "reduction_percent": round(reduction, 2)
        })

    # CSV yaz
    with open("experiment_summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "dataset",
            "total_frames",
            "selected_frames",
            "reduction_percent"
        ])
        writer.writeheader()
        writer.writerows(data)

    # console çıktısı (hocaya direkt göster)
    print("\n=== EXPERIMENT SUMMARY ===\n")
    for row in data:
        print(
            f"{row['dataset'].upper()} | "
            f"Total: {row['total_frames']} | "
            f"Selected: {row['selected_frames']} | "
            f"Reduction: %{row['reduction_percent']}"
        )

    print("\nSaved to experiment_summary.csv")


if __name__ == "__main__":
    summarize()