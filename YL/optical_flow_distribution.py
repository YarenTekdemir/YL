import pandas as pd


def analyze(csv_path, label):
    df = pd.read_csv(csv_path)

    print(f"\n--- {label} ---")
    print("Columns:", df.columns.tolist())

    if "optical_flow_score" not in df.columns:
        print("optical_flow_score column not found")
        return

    print(df["optical_flow_score"].describe())

    print("\nTop 10 highest optical flow frames:")
    print(
        df.sort_values("optical_flow_score", ascending=False)
        .head(10)
        [["frame_1", "frame_2", "optical_flow_score"]]
    )


analyze("optical_flow_scores_real.csv", "REAL")
analyze("optical_flow_scores_fake.csv", "FAKE")