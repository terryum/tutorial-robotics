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

Read the prerequisite [concept chapter](../concepts/robot-hands.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How do Shadow joint synergies produce object contact?

## Learning goals

The introduction holds the wrist, exercises one finger, then closes/opens a shared finger synergy.

How do Shadow joint synergies produce object contact?

## Preflight

Prerequisites: core-04. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run core-shadow-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-shadow-01/baseline-01 --json
```

## Expected

Inspect `shadow-introduction.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Inspect `experiment.json` → `payload`: `actuator_names`, `groups`, `qpos`, `qvel`, `commands`, `contact_counts`, `couplings`, `nq`, `nu`, `time_s`. `contact_observed` refers to the named sphere. The plot is joint displacement norm, not force or grasp success. A positive count says only that contact occurred.

## How it works

### Intuition

The introduction holds the wrist, exercises one finger, then closes/opens a shared finger synergy. A derived scene places a named spherical `contact_object` at the pinned grasp site; checks count object contacts rather than self-contact. Commands address actuators, while observed `qpos` describes the resulting dynamic state. This is prescribed control, not a trained grasp policy.

### Calculation and units

$$
c(\phi)=\frac{1-\cos(2\pi\phi)}2,\qquad \phi\in[0,1]
$$

The dimensionless ramp starts at 0, reaches 1 at phase 0.5 and returns to 0. MuJoCo commands scale each selected actuator's upper control range by 0.7×variant×ramp, then clip to its bounds. A joint-displacement norm in rad is different from contact force in N. Worked calculation, not a run: c(0.5)=1.

```python
import numpy as np
phase = 0.5
ramp = (1 - np.cos(2 * np.pi * phase)) / 2
assert np.isclose(ramp, 1.0)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/embodiments.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py)

`examples/core-shadow-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Change only `variant` 1→0.8 with source, seed and samples fixed. It reduces prescribed closure amplitude; limits and contact may make actual displacement nonlinear. Explain object-contact and per-joint changes separately. Smaller closure is not automatically a better grasp.

```bash
pal lesson run core-shadow-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-shadow-01/comparison-01 --json
pal lesson check core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --json
pal lesson check core-shadow-01 --run-dir .local/runs/core-shadow-01/comparison-01 --json
pal lesson compare core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --comparison-run-dir .local/runs/core-shadow-01/comparison-01 --output-dir .local/comparisons/core-shadow-01/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-shadow-01 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Why distinguish object contact from self-contact? A folded finger may touch the hand without touching the task object. Does one positive contact prove stable grasping? No.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --comparison-run-dir .local/runs/core-shadow-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-shadow-01](./sim-shadow-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
