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

Read the prerequisite [concept chapter](../concepts/physx.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which Shadow coupling and contact properties need PhysX evidence? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

The PhysX introduction must preserve Shadow named joints, drive semantics, coupling and real object contacts after import.

Which Shadow coupling and contact properties need PhysX evidence?

## Preflight

Prerequisites: core-shadow-01. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Requires an Ubuntu NVIDIA GPU host with Isaac Sim installed. Run `pal setup verify --profile isaac --json`. Missing runtime means capability-unavailable; no alternate-engine fallback.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-shadow-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-shadow-01/baseline-01 --json
```

## Expected

Inspect `shadow-physx.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Inspect `physx-observations.json`: `joint_states`, `commands`, `couplings_required`, `object_contact_forces_N` and source/engine identity. The contact sensor filters palm against the named object, and positive finite measured force is required. Imported coupling failures stay blocked. The trace is target/observed first joint; inspect force separately.

## How it works

### Intuition

The PhysX introduction must preserve Shadow named joints, drive semantics, coupling and real object contacts after import. The wrist joints are excluded from the prescribed finger close/open. The importer rejects unverified mimic/tendon mapping; observed dynamic coupling is checked again, rather than inferred from a visually plausible hand.

### Calculation and units

$$
c(\phi)=\frac{1-\cos(2\pi\phi)}2,\qquad \phi\in[0,1]
$$

The dimensionless ramp multiplies 0.7×variant in commanded joint-angle targets (rad). Actual drive response and object force remain measured quantities. Source equality-joint polynomials are checked to within 0.05 rad; a present schema alone is insufficient. Worked calculation, not a run: c(0.5)=1.

```python
import numpy as np
phase = 0.5
ramp = (1 - np.cos(2 * np.pi * phase)) / 2
assert np.isclose(ramp, 1.0)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`examples/sim-shadow-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

## Try it

### Controlled comparison

Change only `variant` 1→0.8 with source, seed and samples fixed. It reduces prescribed closure amplitude; limits and contact may make actual displacement nonlinear. Explain object-contact and per-joint changes separately. Smaller closure is not automatically a better grasp.

```bash
pal lesson run sim-shadow-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-shadow-01/comparison-01 --json
pal lesson check sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --json
pal lesson check sim-shadow-01 --run-dir .local/runs/sim-shadow-01/comparison-01 --json
pal lesson compare sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --comparison-run-dir .local/runs/sim-shadow-01/comparison-01 --output-dir .local/comparisons/sim-shadow-01/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-shadow-01 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Why distinguish object contact from self-contact? A folded finger may touch the hand without touching the task object. Does one positive contact prove stable grasping? No.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --comparison-run-dir .local/runs/sim-shadow-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-stretch3-01](./core-stretch3-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
