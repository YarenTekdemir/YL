# Teacher Summary

## What this project does

This project builds an intelligent frame selection pipeline for deepfake analysis. By using both temporal and frequency-based measures, it identifies the most informative frames while removing redundant content.

## Why it matters

Deepfake detection models often suffer from high computational cost when processing every frame. This work reduces that cost by selecting fewer frames without losing key facial motion cues.

## Main contributions

- Implemented SSIM and motion-based temporal analysis.
- Added Farneback optical flow to measure motion intensity between frames.
- Developed a threshold-based selection strategy that balances retention and reduction.
- Included FFT-based frequency analysis to detect potential artifacts.

## Current results

- Significant frame reduction is achieved while keeping temporal motion.
- `results/threshold_results.csv` records threshold experiments.
- `results/visual_check_real.png` and `results/visual_check_fake.png` show selected frames visually.
- `results/optical_flow_summary.txt` documents optical flow findings.

## Why this is ready for review

The project is now in a stable state with an organized structure and documented results. The implementation supports writing a thesis section with concrete experimental findings rather than only conceptual ideas.

## Important files

- `extract_frames.py`
- `roi_extraction.py`
- `motion_analysis.py`
- `optical_flow_analysis.py`
- `frame_selection.py`
- `threshold_experiments.py`
- `frequency_analysis.py`
- `frame_statistics.py`
