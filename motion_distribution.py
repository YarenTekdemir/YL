import pandas as pd


def analyze(csv_path, label):
    df = pd.read_csv(csv_path)

    print(f"\n--- {label} ---")
    print("Columns:", df.columns.tolist())

    if "motion_score" in df.columns:
        print(df["motion_score"].describe())
    else:
        print("motion_score column not found")


analyze("motion_scores_real.csv", "REAL")
analyze("motion_scores_fake.csv", "FAKE")