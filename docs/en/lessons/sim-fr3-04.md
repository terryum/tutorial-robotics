<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-fr3-04.md" lang="ko">한국어</a> | <a href="sim-fr3-04.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-fr3-04 — FR3 matched-engine evidence comparison

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / fr3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `sim-fr3-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Compare completed FR3 MuJoCo/PhysX measurements only after matching initial pose, targets, frame and control period.

## Learning goals

Match target arrays, initial pose, world frame and control period in two completed runs. Compare TCP error RMS difference, joint errors and measured contact forces. Investigate import, drive and engine differences without inferring hardware safety.

## Preflight

Prerequisites: sim-fr3-01. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

```bash
pal lesson run sim-fr3-04 --samples 64 --json
```

Save the returned run_dir as BASE. Execution alone does not mark completion.

## Expected

Inspect `engine-comparison.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

## How it works

Match target arrays, initial pose, world frame and control period in two completed runs. Compare TCP error RMS difference, joint errors and measured contact forces. Investigate import, drive and engine differences without inferring hardware safety.

## Code connection

[`comparison.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/comparison.py)

`pai_lab.training` records checkpoints and independent evaluation.

## Try it

Change only variant; keep the other conditions fixed.

```bash
pal lesson run sim-fr3-04 --samples 64 --variant 0.8 --json
pal lesson check sim-fr3-04 --run-dir BASE --json
pal lesson review sim-fr3-04 --run-dir BASE --comparison-run-dir COMPARISON --notes "measured comparison and interpretation"
pal lesson finish sim-fr3-04 --run-dir BASE --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-fr3-04 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

Save explanation, baseline, comparison and next action, then stop after one lesson. Unverified tools or model compatibility keep the stage blocked.

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-03](./core-enlight-03.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
