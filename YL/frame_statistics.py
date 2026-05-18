import os


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



analyze(
    "frames/real",
    "selected_frames/real",
    "REAL"
)

analyze(
    "frames/fake",
    "selected_frames/fake",
    "FAKE"
)