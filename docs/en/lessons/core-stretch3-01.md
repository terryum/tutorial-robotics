<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-stretch3-01.md" lang="ko">한국어</a> | <a href="core-stretch3-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-stretch3-01 — Stretch 3 base, arm and coordinated reach

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / stretch3` |
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

Read the prerequisite [concept chapter](../concepts/mobile-motion.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How do base and arm motions combine to reach a target?

## Learning goals

A mobile manipulator can use both base and arm to reduce tool error.

How do base and arm motions combine to reach a target?

## Preflight

Prerequisites: core-04. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run core-stretch3-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-stretch3-01/baseline-01 --json
```

## Expected

Inspect `stretch-introduction.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Read `groups`, `free_base`, `actuator_names`, `commands`, `tcp_positions_m`, `reach_target_m`, `reach_errors_m`, `qpos`, `qvel`. Early trace values are TCP height; after the target exists they are reach error, both in m but with different meaning. The check requires reduced final reach error and actual contacts, not a trained or millimetre-accurate policy.

## How it works

### Intuition

A mobile manipulator can use both base and arm to reduce tool error. The introductory schedule moves forward, turns, moves lift/arm, then coordinates planar wheel correction and vertical lift correction toward a generated world target. Named actuators distinguish wheels, telescoping arm, wrist and gripper from free-base state. This is a prescribed simulated controller, not a learned navigation policy.

### Calculation and units

$$
v=\frac r2(\omega_R+\omega_L),\qquad \dot\psi=\frac rL(\omega_R-\omega_L)
$$

This ideal no-slip differential-drive relation explains direction, not a fitted simulator model. Wheel radius r and separation L use m; angular speeds use rad/s, body speed m/s and yaw rate rad/s. Worked calculation, not measured Stretch geometry: r=0.1 m, L=0.4 m and both wheels 0.2 rad/s yield v=0.02 m/s and zero turn.

```python
import numpy as np
r_m, separation_m = 0.1, 0.4
left_rad_s = right_rad_s = 0.2
assert np.isclose(r_m * (left_rad_s + right_rad_s) / 2, 0.02)
assert r_m * (right_rad_s - left_rad_s) / separation_m == 0
```

## Code connection

### Source trace

[`src/pai_lab/lessons/embodiments.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py)

`examples/core-stretch3-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Change only `variant` with seed, samples and source fixed. It scales wheel schedule and part of arm extension; report this as one schedule multiplier with multiple physical effects, not an isolated wheel-gain experiment. Preserve free-base/contact configuration. Compare actual base/TCP states rather than only requested commands.

```bash
pal lesson run core-stretch3-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-stretch3-01/comparison-01 --json
pal lesson check core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --json
pal lesson check core-stretch3-01 --run-dir .local/runs/core-stretch3-01/comparison-01 --json
pal lesson compare core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --comparison-run-dir .local/runs/core-stretch3-01/comparison-01 --output-dir .local/comparisons/core-stretch3-01/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-stretch3-01 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Why not write the free-base quaternion into actuator controls? It is a state representation, not a wheel or arm action. Does base movement prove navigation? No; this is a small prescribed simulation schedule.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --comparison-run-dir .local/runs/core-stretch3-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-stretch3-01 --run-dir .local/runs/core-stretch3-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-stretch3-01](./sim-stretch3-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
