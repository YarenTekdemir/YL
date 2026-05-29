# Frame Selection Performance Analysis

## Purpose

This analysis evaluates whether the proposed frame selection method reduces the number of processed frames while preserving informative visual changes.

## Compared Methods

- AllFrames: uses all available frames.
- Every5thFrame: uses every fifth frame as a simple baseline.
- ProposedMethod: selects frames according to motion, frequency, and optical flow based scores.

## Summary Results

| Method         | Label   |   TotalFrames |   SelectedFrames |   RemovedFrames |   ReductionPercent |   AvgMotionScore |   AvgFrequencyScore |   AvgOpticalFlowScore |   FrameUsagePercent |   EfficiencyGain |   InformationScore |
|:---------------|:--------|--------------:|-----------------:|----------------:|-------------------:|-----------------:|--------------------:|----------------------:|--------------------:|-----------------:|-------------------:|
| AllFrames      | Real    |           389 |              389 |               0 |               0    |           0.3289 |              0.1076 |                0.3289 |              100    |             0    |             0.7654 |
| Every5thFrame  | Real    |           389 |               78 |             311 |              79.95 |           0.3368 |              0.1205 |                0.3368 |               20.05 |            79.95 |             0.7941 |
| ProposedMethod | Real    |           389 |               49 |             340 |              87.4  |           0.4887 |              0.7149 |                0.4887 |               12.6  |            87.4  |             1.6923 |
| AllFrames      | Fake    |           389 |              389 |               0 |               0    |           0.3219 |              0.0703 |                0.3219 |              100    |             0    |             0.7141 |
| Every5thFrame  | Fake    |           389 |               78 |             311 |              79.95 |           0.33   |              0.0767 |                0.33   |               20.05 |            79.95 |             0.7367 |
| ProposedMethod | Fake    |           389 |               49 |             340 |              87.4  |           0.4679 |              0.5232 |                0.4679 |               12.6  |            87.4  |             1.459  |

## Proposed Method Interpretation

For Real videos, the proposed method selected 49 out of 389 frames. This corresponds to a frame reduction of 87.4%.
For Fake videos, the proposed method selected 49 out of 389 frames. This corresponds to a frame reduction of 87.4%.

The results show that the proposed method processes fewer frames than both the AllFrames baseline and the Every5thFrame baseline.
At the same time, the proposed method keeps frames with stronger motion, frequency, and optical flow signals.