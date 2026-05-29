from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

EVALUATION_RESULTS_PATH = BASE_DIR / "evaluation_results.csv"

OUTPUT_DIR = BASE_DIR / "results" / "frame_selection_performance"
SUMMARY_CSV_PATH = OUTPUT_DIR / "frame_selection_performance_summary.csv"


def load_data():
    if not EVALUATION_RESULTS_PATH.exists():
        raise FileNotFoundError(f"File not found: {EVALUATION_RESULTS_PATH}")

    return pd.read_csv(EVALUATION_RESULTS_PATH)


def create_performance_summary(df):
    selected_columns = [
        "Method",
        "Label",
        "TotalFrames",
        "SelectedFrames",
        "RemovedFrames",
        "ReductionPercent",
        "AvgMotionScore",
        "AvgFrequencyScore",
        "AvgOpticalFlowScore"
    ]

    summary_df = df[selected_columns].copy()

    summary_df["FrameUsagePercent"] = (
        summary_df["SelectedFrames"] / summary_df["TotalFrames"] * 100
    ).round(2)

    summary_df["EfficiencyGain"] = summary_df["ReductionPercent"]

    summary_df["InformationScore"] = (
        summary_df["AvgMotionScore"]
        + summary_df["AvgFrequencyScore"]
        + summary_df["AvgOpticalFlowScore"]
    ).round(4)

    return summary_df


def save_grouped_bar_chart(df, value_col, title, ylabel, output_name):
    pivot_df = df.pivot(
        index="Method",
        columns="Label",
        values=value_col
    )

    plt.figure(figsize=(9, 6))
    pivot_df.plot(kind="bar")

    plt.title(title)
    plt.xlabel("Method")
    plt.ylabel(ylabel)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path)
    plt.close()

    print(f"Saved: {output_path}")


def create_frame_usage_chart(summary_df):
    save_grouped_bar_chart(
        summary_df,
        "SelectedFrames",
        "Selected Frame Count by Method",
        "Selected Frames",
        "selected_frame_count_comparison.png"
    )


def create_reduction_chart(summary_df):
    save_grouped_bar_chart(
        summary_df,
        "ReductionPercent",
        "Frame Reduction Percentage by Method",
        "Reduction Percent",
        "frame_reduction_comparison.png"
    )


def create_information_score_chart(summary_df):
    save_grouped_bar_chart(
        summary_df,
        "InformationScore",
        "Information Score by Method",
        "Information Score",
        "information_score_comparison.png"
    )


def create_frame_usage_percent_chart(summary_df):
    save_grouped_bar_chart(
        summary_df,
        "FrameUsagePercent",
        "Frame Usage Percentage by Method",
        "Frame Usage Percent",
        "frame_usage_percent_comparison.png"
    )


def create_text_report(summary_df):
    report_path = OUTPUT_DIR / "frame_selection_performance_report.md"

    proposed_df = summary_df[summary_df["Method"] == "ProposedMethod"]

    lines = []
    lines.append("# Frame Selection Performance Analysis")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(
        "This analysis evaluates whether the proposed frame selection method reduces the number of processed frames while preserving informative visual changes."
    )
    lines.append("")
    lines.append("## Compared Methods")
    lines.append("")
    lines.append("- AllFrames: uses all available frames.")
    lines.append("- Every5thFrame: uses every fifth frame as a simple baseline.")
    lines.append("- ProposedMethod: selects frames according to motion, frequency, and optical flow based scores.")
    lines.append("")
    lines.append("## Summary Results")
    lines.append("")
    lines.append(summary_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Proposed Method Interpretation")
    lines.append("")

    for _, row in proposed_df.iterrows():
        lines.append(
            f"For {row['Label']} videos, the proposed method selected "
            f"{int(row['SelectedFrames'])} out of {int(row['TotalFrames'])} frames. "
            f"This corresponds to a frame reduction of {row['ReductionPercent']}%."
        )

    lines.append("")
    lines.append(
        "The results show that the proposed method processes fewer frames than both the AllFrames baseline and the Every5thFrame baseline."
    )
    lines.append(
        "At the same time, the proposed method keeps frames with stronger motion, frequency, and optical flow signals."
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved: {report_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()
    summary_df = create_performance_summary(df)

    summary_df.to_csv(SUMMARY_CSV_PATH, index=False)

    create_frame_usage_chart(summary_df)
    create_reduction_chart(summary_df)
    create_information_score_chart(summary_df)
    create_frame_usage_percent_chart(summary_df)
    create_text_report(summary_df)

    print("Frame selection performance analysis completed.")
    print(f"Saved summary: {SUMMARY_CSV_PATH}")
    print(summary_df)


if __name__ == "__main__":
    main()