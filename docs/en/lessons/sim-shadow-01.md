<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-shadow-01.md" lang="ko">한국어</a> | <a href="sim-shadow-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-shadow-01 — Shadow Hand PhysX introduction

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / shadow` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda` |
| Prerequisites | `core-shadow-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

This prepared runtime controls, observes and renders in PhysX. Execution is unverified on Mac. Import success alone does not pass this lesson.

## Learning goals

Inspect actual single-finger and open/close synergy responses. Check object-filtered contact forces, dynamic joint coupling and rendering; incomplete coupling import blocks execution.

## Preflight

Prerequisites: core-shadow-01. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Requires an Ubuntu NVIDIA GPU host with Isaac Sim installed. Run `pal setup verify --profile isaac --json`. Missing runtime means capability-unavailable; no alternate-engine fallback.

## Action

```bash
pal lesson run sim-shadow-01 --samples 64 --json
```

Save the returned run_dir as BASE. Execution alone does not mark completion.

## Expected

Inspect `shadow-physx.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

## How it works

Inspect actual single-finger and open/close synergy responses. Check object-filtered contact forces, dynamic joint coupling and rendering; incomplete coupling import blocks execution.

## Code connection

[`isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`pai_lab.training` records checkpoints and independent evaluation.

## Try it

Change only variant; keep the other conditions fixed.

```bash
pal lesson run sim-shadow-01 --samples 64 --variant 0.8 --json
pal lesson check sim-shadow-01 --run-dir BASE --json
pal lesson review sim-shadow-01 --run-dir BASE --comparison-run-dir COMPARISON --notes "measured comparison and interpretation"
pal lesson finish sim-shadow-01 --run-dir BASE --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-shadow-01 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

Save explanation, baseline, comparison and next action, then stop after one lesson. Unverified tools or model compatibility keep the stage blocked.

<!-- pal:navigation:start -->
## Next lesson

[core-stretch3-01](./core-stretch3-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
