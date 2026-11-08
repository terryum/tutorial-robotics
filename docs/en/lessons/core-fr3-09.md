<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-fr3-09.md" lang="ko">한국어</a> | <a href="core-fr3-09.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-fr3-09 — FR3 joint and TCP trajectory tracking

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-06` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Measure joint/TCP error from the actual MuJoCo arm state. Learning uses arm demonstrations or rollouts and evaluates twenty independent targets.

## Learning goals

The first half commands a 0.06 rad sinusoid on joint one. The second half tracks a 12 mm world-frame TCP circle using damped least-squares IK.

## Preflight

Prerequisites: core-fr3-06. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

```bash
pal lesson run core-fr3-09 --samples 64 --json
```

Save the returned run_dir as BASE. Execution alone does not mark completion.

## Expected

Inspect `trajectory.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

## How it works

The first half commands a 0.06 rad sinusoid on joint one. The second half tracks a 12 mm world-frame TCP circle using damped least-squares IK.

## Code connection

[`arm.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)

`pai_lab.training` records checkpoints and independent evaluation.

## Try it

Change only variant; keep the other conditions fixed.

```bash
pal lesson run core-fr3-09 --samples 64 --variant 0.8 --json
pal lesson check core-fr3-09 --run-dir BASE --json
pal lesson review core-fr3-09 --run-dir BASE --comparison-run-dir COMPARISON --notes "measured comparison and interpretation"
pal lesson finish core-fr3-09 --run-dir BASE --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-fr3-09 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

Save explanation, baseline, comparison and next action, then stop after one lesson. Unverified tools or model compatibility keep the stage blocked.

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-10](./core-fr3-10.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
