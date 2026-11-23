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

Read the prerequisite [concept chapter](../concepts/physx.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which Enlight control properties must be rechecked in PhysX? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

A joint-space trajectory and a Cartesian trajectory ask different questions.

Which Enlight control properties must be rechecked in PhysX?

## Preflight

Prerequisites: core-enlight-03. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Requires an Ubuntu NVIDIA GPU host with Isaac Sim installed. Run `pal setup verify --profile isaac --json`. Missing runtime means capability-unavailable; no alternate-engine fallback.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-enlight-03 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-enlight-03/baseline-01 --json
```

## Expected

Inspect `enlight-physx.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Inspect `physx-observations.json` and `experiment.json` → `payload`: `tcp_targets_m`, `tcp_errors_m`, `joint_errors_rad`, `initial_q_rad`, `frame`, `control_dt_s`, `joint_reaction_forces`, `contact_force_norms_N`, and separate `probe_contact_forces_N`. Reactions include gravity; they are not the contact sensor. After the trajectory, a distinct collision-probe experiment must report positive finite PhysX force. A rendered image or imported USD alone cannot satisfy these dynamics/contact requirements. Actual GPU execution remains a separate verification gate.

## How it works

### Intuition

A joint-space trajectory and a Cartesian trajectory ask different questions. The first half moves Enlight joint one sinusoidally; the second half asks its TCP to follow a circle in the world x/y plane. Both use the Enlight model, not transferred joint arrays from another arm. Named PhysX joints receive position-drive targets. TCP motion, Jacobian and observed state come from PhysX; MuJoCo only supplies pinned source metadata/export.

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

[`src/pai_lab/lessons/isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`examples/sim-enlight-03/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Change only `variant` 1→0.8 with sample count and seed fixed. This single CLI variable scales both the joint waveform and TCP radius, so report both physical changes; it is not a gain-only experiment. Compare per-phase errors and extrema. Smaller commanded paths may have smaller errors without a better controller.

```bash
pal lesson run sim-enlight-03 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-enlight-03/comparison-01 --json
pal lesson check sim-enlight-03 --run-dir .local/runs/sim-enlight-03/baseline-01 --json
pal lesson check sim-enlight-03 --run-dir .local/runs/sim-enlight-03/comparison-01 --json
pal lesson compare sim-enlight-03 --run-dir .local/runs/sim-enlight-03/baseline-01 --comparison-run-dir .local/runs/sim-enlight-03/comparison-01 --output-dir .local/comparisons/sim-enlight-03/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-enlight-03 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Which quantity is in rad and which in m? Joint error versus TCP position error. Does tracking a Enlight circle establish transfer to another arm or hardware? No; it establishes this model/engine trajectory behavior only.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-enlight-03 --run-dir .local/runs/sim-enlight-03/baseline-01 --comparison-run-dir .local/runs/sim-enlight-03/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-03 --run-dir .local/runs/sim-enlight-03/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-04](./sim-enlight-04.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
