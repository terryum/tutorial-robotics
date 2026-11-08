<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-shadow-01.md" lang="ko">한국어</a> | <a href="core-shadow-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-shadow-01 — Shadow Hand joints, synergies and object contact

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / shadow` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Inspect named joints/actuators and addresses in the pinned model, then record actual motion and contact.

## Learning goals

Hold the wrist, exercise a single finger, then open/close through a finger synergy. Observe contact with a spherical object placed at the palm.

## Preflight

Prerequisites: core-04. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

```bash
pal lesson run core-shadow-01 --samples 64 --json
```

Save the returned run_dir as BASE. Execution alone does not mark completion.

## Expected

Inspect `shadow-introduction.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

## How it works

Hold the wrist, exercise a single finger, then open/close through a finger synergy. Observe contact with a spherical object placed at the palm.

## Code connection

[`embodiments.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py)

`pai_lab.training` records checkpoints and independent evaluation.

## Try it

Change only variant; keep the other conditions fixed.

```bash
pal lesson run core-shadow-01 --samples 64 --variant 0.8 --json
pal lesson check core-shadow-01 --run-dir BASE --json
pal lesson review core-shadow-01 --run-dir BASE --comparison-run-dir COMPARISON --notes "measured comparison and interpretation"
pal lesson finish core-shadow-01 --run-dir BASE --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-shadow-01 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

Save explanation, baseline, comparison and next action, then stop after one lesson. Unverified tools or model compatibility keep the stage blocked.

<!-- pal:navigation:start -->
## Next lesson

[sim-shadow-01](./sim-shadow-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
