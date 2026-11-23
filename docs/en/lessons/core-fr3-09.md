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

Read the prerequisite [concept chapter](../concepts/control-contact.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How do joint and TCP trajectory errors differ?

## Learning goals

A joint-space trajectory and a Cartesian trajectory ask different questions.

How do joint and TCP trajectory errors differ?

## Preflight

Prerequisites: core-fr3-06. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run core-fr3-09 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-09/baseline-01 --json
```

## Expected

Inspect `trajectory.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Inspect `experiment.json` → `payload`: `joint_targets_rad`, `joint_errors_rad`, `tcp_targets_m`, `tcp_rmse_m`, `time_s`, `initial_q_rad`, `frame`, `control_dt_s` and contact arrays. `tcp_rmse_m` averages only the second half; the plotted error spans both phases. Baseline count is max(160,64×4)=256 and each control command advances ten physics steps. The MuJoCo contact field sums absolute normal forces over all contacts, despite its norm-like name.

## How it works

### Intuition

A joint-space trajectory and a Cartesian trajectory ask different questions. The first half moves FR3 joint one sinusoidally; the second half asks its TCP to follow a circle in the world x/y plane. Both use the FR3 model, not transferred joint arrays from another arm. FR3 position actuators receive joint targets.

### Calculation and units

$$
x^*(\theta)=x_0+0.012v[\sin\theta,1-\cos\theta,0]^T,\qquad e_i=\|x_i^*-x_i\|_2
$$

x is a three-vector in world-frame m, joint targets are seven angles in rad and v is dimensionless `variant`. The circle has radius 0.012v m and is offset from x0; at θ=π its y displacement is 0.024v m. The first-half joint amplitude is 0.06v rad. Worked calculation, not a measured run: v=0.8 gives a 0.0096 m radius and 0.048 rad joint amplitude.

```python
import numpy as np
v = 0.8
assert np.isclose(0.012 * v, 0.0096)
assert np.isclose(0.06 * v, 0.048)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/arm.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py)

`examples/core-fr3-09/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Change only `variant` 1→0.8 with sample count and seed fixed. This single CLI variable scales both the joint waveform and TCP radius, so report both physical changes; it is not a gain-only experiment. Compare per-phase errors and extrema. Smaller commanded paths may have smaller errors without a better controller.

```bash
pal lesson run core-fr3-09 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-fr3-09/comparison-01 --json
pal lesson check core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --json
pal lesson check core-fr3-09 --run-dir .local/runs/core-fr3-09/comparison-01 --json
pal lesson compare core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --comparison-run-dir .local/runs/core-fr3-09/comparison-01 --output-dir .local/comparisons/core-fr3-09/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-fr3-09 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Which quantity is in rad and which in m? Joint error versus TCP position error. Does tracking a FR3 circle establish transfer to another arm or hardware? No; it establishes this model/engine trajectory behavior only.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --comparison-run-dir .local/runs/core-fr3-09/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-fr3-09 --run-dir .local/runs/core-fr3-09/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-10](./core-fr3-10.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
