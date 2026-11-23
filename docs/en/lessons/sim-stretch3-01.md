<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-stretch3-01.md" lang="ko">한국어</a> | <a href="sim-stretch3-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-stretch3-01 — Stretch 3 PhysX introduction

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / stretch3` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda` |
| Prerequisites | `core-stretch3-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

This prepared runtime controls, observes and renders in PhysX. Execution is unverified on Mac. Import success alone does not pass this lesson.

Read the prerequisite [concept chapter](../concepts/physx.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How can Stretch base-arm behavior be verified after PhysX import? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

After PhysX import, Stretch must retain a free base and named wheel, lift and telescoping-joint controls.

How can Stretch base-arm behavior be verified after PhysX import?

## Preflight

Prerequisites: core-stretch3-01. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Requires an Ubuntu NVIDIA GPU host with Isaac Sim installed. Run `pal setup verify --profile isaac --json`. Missing runtime means capability-unavailable; no alternate-engine fallback.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-stretch3-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-stretch3-01/baseline-01 --json
```

## Expected

Inspect `stretch-physx.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Read `base_positions_m`, `joint_states`, `free_base_required`, `couplings_required` and engine/source identity. The gate requires base movement above 0.005 m and joint movement above 0.01, plus imported dynamic coupling checks where needed. `commands` stores a general target array that does not encode the separately applied wheel/lift commands; inspect the named source commands before treating that array as a full replay log.

## How it works

### Intuition

After PhysX import, Stretch must retain a free base and named wheel, lift and telescoping-joint controls. Wheel velocity commands and arm position commands are separate actuator semantics. The current PhysX schedule demonstrates forward/turn/arm movement; it does not implement the MuJoCo introduction's final feedback reach controller. Do not promise matched reach-error improvement from an import alone.

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

[`src/pai_lab/lessons/isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`examples/sim-stretch3-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

## Try it

### Controlled comparison

Change only `variant` with seed, samples and source fixed. It scales wheel schedule and part of arm extension; report this as one schedule multiplier with multiple physical effects, not an isolated wheel-gain experiment. Preserve free-base/contact configuration. Compare actual base/TCP states rather than only requested commands.

```bash
pal lesson run sim-stretch3-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-stretch3-01/comparison-01 --json
pal lesson check sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --json
pal lesson check sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/comparison-01 --json
pal lesson compare sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --comparison-run-dir .local/runs/sim-stretch3-01/comparison-01 --output-dir .local/comparisons/sim-stretch3-01/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-stretch3-01 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Why not write the free-base quaternion into actuator controls? It is a state representation, not a wheel or arm action. Does base movement prove navigation? No; this is a small prescribed simulation schedule.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --comparison-run-dir .local/runs/sim-stretch3-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-stretch3-01 --run-dir .local/runs/sim-stretch3-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-04](./hw-enlight-04.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
