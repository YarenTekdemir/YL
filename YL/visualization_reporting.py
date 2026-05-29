from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

EVALUATION_RESULTS_PATH = BASE_DIR / "evaluation_results.csv"
OUTPUT_DIR = BASE_DIR / "results" / "visualizations"


def load_evaluation_results():
    if not EVALUATION_RESULTS_PATH.exists():
        raise FileNotFoundError(f"File not found: {EVALUATION_RESULTS_PATH}")

    return pd.read_csv(EVALUATION_RESULTS_PATH)


def save_bar_chart(df, x_col, y_col, title, ylabel, output_name):
    plt.figure(figsize=(10, 6))

    labels = df[x_col].astype(str)
    values = df[y_col]

    plt.bar(labels, values)

    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    output_path = OUTPUT_DIR / output_name
    plt.savefig(output_path)
    plt.close()

    print(f"Saved: {output_path}")


def create_method_label_column(df):
    df = df.copy()
    df["MethodLabel"] = df["Method"] + " - " + df["Label"]
    return df


def create_selected_frames_chart(df):
    chart_df = create_method_label_column(df)

    save_bar_chart(
        chart_df,
        "MethodLabel",
        "SelectedFrames",
        "Selected Frame Count by Method",
        "Selected Frames",
        "selected_frames_by_method.png"
    )


def create_reduction_chart(df):
    chart_df = create_method_label_column(df)

    save_bar_chart(
        chart_df,
        "MethodLabel",
        "ReductionPercent",
        "Reduction Percentage by Method",
        "Reduction Percent",
        "reduction_percentage_by_method.png"
    )


def create_motion_score_chart(df):
    chart_df = create_method_label_column(df)

    save_bar_chart(
        chart_df,
        "MethodLabel",
        "AvgMotionScore",
        "Average Motion Score by Method",
        "Average Motion Score",
        "avg_motion_score_by_method.png"
    )


def create_frequency_score_chart(df):
    chart_df = create_method_label_column(df)

    save_bar_chart(
        chart_df,
        "MethodLabel",
        "AvgFrequencyScore",
        "Average Frequency Score by Method",
        "Average Frequency Score",
        "avg_frequency_score_by_method.png"
    )


def create_optical_flow_score_chart(df):
    chart_df = create_method_label_column(df)

    save_bar_chart(
        chart_df,
        "MethodLabel",
        "AvgOpticalFlowScore",
        "Average Optical Flow Score by Method",
        "Average Optical Flow Score",
        "avg_optical_flow_score_by_method.png"
    )


def create_real_fake_comparison_chart(df):
    proposed_df = df[df["Method"] == "ProposedMethod"].copy()

    save_bar_chart(
        proposed_df,
        "Label",
        "AvgMotionScore",
        "Real vs Fake Average Motion Score for Proposed Method",
        "Average Motion Score",
        "real_fake_motion_comparison.png"
    )


def create_markdown_report(df):
    report_path = OUTPUT_DIR / "evaluation_report.md"

    proposed_df = df[df["Method"] == "ProposedMethod"]

    lines = []
    lines.append("# Evaluation Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("This report compares three frame usage strategies:")
    lines.append("")
    lines.append("- AllFrames")
    lines.append("- Every5thFrame")
    lines.append("- ProposedMethod")
    lines.append("")
    lines.append("## Evaluation Results")
    lines.append("")
    lines.append(df.to_markdown(index=False))
    lines.append("")
    lines.append("## Proposed Method Results")
    lines.append("")
    lines.append(proposed_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "The proposed method reduces the number of processed frames while selecting frames with higher average motion and frequency scores."
    )
    lines.append(
        "This supports the idea that informative frames can be prioritized instead of processing every frame."
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved: {report_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_evaluation_results()

    create_selected_frames_chart(df)
    create_reduction_chart(df)
    create_motion_score_chart(df)
    create_frequency_score_chart(df)
    create_optical_flow_score_chart(df)
    create_real_fake_comparison_chart(df)
    create_markdown_report(df)

    print("Visualization and reporting completed.")


if __name__ == "__main__":
    main()