import math
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

MOTION_REAL_PATH = BASE_DIR / "motion_scores_real.csv"
MOTION_FAKE_PATH = BASE_DIR / "motion_scores_fake.csv"

FREQUENCY_REAL_PATH = BASE_DIR / "frequency_scores_real.csv"
FREQUENCY_FAKE_PATH = BASE_DIR / "frequency_scores_fake.csv"

OPTICAL_REAL_PATH = BASE_DIR / "optical_flow_scores_real.csv"
OPTICAL_FAKE_PATH = BASE_DIR / "optical_flow_scores_fake.csv"

OUTPUT_PATH = BASE_DIR / "evaluation_results.csv"


def read_score_file(path, label, score_name):
    df = pd.read_csv(path)
    df["Label"] = label

    frame_col = None
    for col in ["frame", "frame_name", "filename", "image", "frame_path", "frame_2"]:
        if col in df.columns:
            frame_col = col
            break

    if frame_col is None:
        raise ValueError(f"No frame column found in {path.name}")

    df = df.rename(columns={frame_col: "Frame"})

    expected_score_columns = {
        "MotionScore": "motion_score",
        "FrequencyScore": "frequency_score",
        "OpticalFlowScore": "optical_flow_score"
    }

    source_score_col = expected_score_columns.get(score_name)

    if source_score_col not in df.columns:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            raise ValueError(f"No numeric score column found in {path.name}")
        source_score_col = numeric_cols[-1]

    df = df.rename(columns={source_score_col: score_name})

    return df[["Frame", "Label", score_name]]


def load_combined_data():
    motion = pd.concat([
        read_score_file(MOTION_REAL_PATH, "Real", "MotionScore"),
        read_score_file(MOTION_FAKE_PATH, "Fake", "MotionScore")
    ])

    frequency = pd.concat([
        read_score_file(FREQUENCY_REAL_PATH, "Real", "FrequencyScore"),
        read_score_file(FREQUENCY_FAKE_PATH, "Fake", "FrequencyScore")
    ])

    optical = pd.concat([
        read_score_file(OPTICAL_REAL_PATH, "Real", "OpticalFlowScore"),
        read_score_file(OPTICAL_FAKE_PATH, "Fake", "OpticalFlowScore")
    ])

    df = motion.merge(frequency, on=["Frame", "Label"], how="left")
    df = df.merge(optical, on=["Frame", "Label"], how="left")

    df = df.fillna(0)

    return df


def create_result_row(method, label, total_frames, selected_df, all_df):
    selected_frames = len(selected_df)
    removed_frames = total_frames - selected_frames

    reduction_percent = 0
    if total_frames > 0:
        reduction_percent = round((removed_frames / total_frames) * 100, 2)

    return {
        "Method": method,
        "Label": label,
        "TotalFrames": total_frames,
        "SelectedFrames": selected_frames,
        "RemovedFrames": removed_frames,
        "ReductionPercent": reduction_percent,
        "AvgMotionScore": round(selected_df["MotionScore"].mean(), 4),
        "AvgFrequencyScore": round(selected_df["FrequencyScore"].mean(), 4),
        "AvgOpticalFlowScore": round(selected_df["OpticalFlowScore"].mean(), 4),
        "MaxMotionScore": round(all_df["MotionScore"].max(), 4),
        "MaxFrequencyScore": round(all_df["FrequencyScore"].max(), 4),
        "MaxOpticalFlowScore": round(all_df["OpticalFlowScore"].max(), 4)
    }


def evaluate_label(df, label):
    label_df = df[df["Label"] == label].copy()
    total_frames = len(label_df)

    every_5th_df = label_df.iloc[::5]

    proposed_count = max(1, math.ceil(total_frames * 0.125))
    proposed_df = label_df.sort_values(
        by=["MotionScore", "OpticalFlowScore", "FrequencyScore"],
        ascending=False
    ).head(proposed_count)

    rows = []

    rows.append(create_result_row(
        "AllFrames",
        label,
        total_frames,
        label_df,
        label_df
    ))

    rows.append(create_result_row(
        "Every5thFrame",
        label,
        total_frames,
        every_5th_df,
        label_df
    ))

    rows.append(create_result_row(
        "ProposedMethod",
        label,
        total_frames,
        proposed_df,
        label_df
    ))

    return rows


def main():
    df = load_combined_data()

    rows = []
    rows.extend(evaluate_label(df, "Real"))
    rows.extend(evaluate_label(df, "Fake"))

    result_df = pd.DataFrame(rows)
    result_df.to_csv(OUTPUT_PATH, index=False)

    print("Evaluation completed.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(result_df)


if __name__ == "__main__":
    main()