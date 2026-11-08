<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-enlight-03.md" lang="ko">한국어</a> | <a href="sim-enlight-03.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-03 — Enlight PhysX joint and TCP control

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda` |
| Prerequisites | `core-enlight-03` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

This prepared runtime controls, observes and renders in PhysX. Execution is unverified on Mac. Import success alone does not pass this lesson.

## Learning goals

Map Enlight joint1…joint7 and attachment_site separately. Run joint sinusoids, a TCP circle and probe contact in PhysX using Enlight joints, drives and frames; no FR3 weights are used.

## Preflight

Prerequisites: core-enlight-03. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Requires an Ubuntu NVIDIA GPU host with Isaac Sim installed. Run `pal setup verify --profile isaac --json`. Missing runtime means capability-unavailable; no alternate-engine fallback.

## Action

```bash
pal lesson run sim-enlight-03 --samples 64 --json
```

Save the returned run_dir as BASE. Execution alone does not mark completion.

## Expected

Inspect `enlight-physx.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

## How it works

Map Enlight joint1…joint7 and attachment_site separately. Run joint sinusoids, a TCP circle and probe contact in PhysX using Enlight joints, drives and frames; no FR3 weights are used.

## Code connection

[`isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`pai_lab.training` records checkpoints and independent evaluation.

## Try it

Change only variant; keep the other conditions fixed.

```bash
pal lesson run sim-enlight-03 --samples 64 --variant 0.8 --json
pal lesson check sim-enlight-03 --run-dir BASE --json
pal lesson review sim-enlight-03 --run-dir BASE --comparison-run-dir COMPARISON --notes "measured comparison and interpretation"
pal lesson finish sim-enlight-03 --run-dir BASE --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-enlight-03 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

Save explanation, baseline, comparison and next action, then stop after one lesson. Unverified tools or model compatibility keep the stage blocked.

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-04](./sim-enlight-04.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
