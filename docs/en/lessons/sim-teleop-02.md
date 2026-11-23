<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-teleop-02.md" lang="ko">한국어</a> | <a href="sim-teleop-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-teleop-02 — Spatial alignment and command sink

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / common` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-teleop-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Spatial alignment is an explicit transform chain, not a pose-array copy. In integrated mode, `InputMux` selects VIVE wrists, MANUS fingers and Quest switches; quest-only is another explicit mode. The lesson's `integrated_frame` provides synthetic samples and a known 0.05 m frame translation, so it tests source selection and transform arithmetic without claiming live calibration.

Read the prerequisite [concept chapter](../concepts/kinematics.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How do calibrated SE3 transforms and a stale-input sink constrain retargeting?

## Learning goals

Spatial alignment is an explicit transform chain, not a pose-array copy.

How do calibrated SE3 transforms and a stale-input sink constrain retargeting?

## Preflight

Use a host matching the catalog platforms and capabilities; computer names do not grant readiness. `core-teleop-01` supports macOS arm64 and Linux x86_64; the later optional input/collection lessons are cataloged for Linux x86_64. Read [VR setup](../setup/vr-teleop.md), [equipment stages](../equipment-stages.md) and the synthetic/live distinction in [verification](../../verification/vr-teleop-2026-11-13.md). Preserve devices, calibration and raw episodes under ignored `.local/`; no automatic vendor installation or device consent is implied.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-teleop-02 --headless --seed 7 --samples 16 --output-dir .local/runs/sim-teleop-02/baseline-01 --json
```

## Expected

Expect synthetic replay/collection evidence, not a live-device acceptance report. Inspect the catalog artifact, `experiment.json`, `trace.csv`, `plot.png` and episode manifests. Three saved episodes plus discarded/aborted records preserve lifecycle and provenance. Actual 60-second device-rate/tracking/occlusion/reconnect acceptance belongs to the separate live-input gate.

## Observe

Inspect recorded input and applied targets separately; synthetic timestamps are generated test clocks.

### Reading the artifacts

Inspect raw `devices`, Quest switches and `mode` inside each saved frame alongside transformed left/right `pose_source`, `finger_source`, frame/calibration IDs and receiver times. Combined freshness uses the oldest selected receiver stamp, so a fresh wrist cannot hide stale fingers or switches. Episode manifests and `live_input_verified=False` remain essential; device clocks are retained without cross-host subtraction.

## How it works

### Intuition

Spatial alignment is an explicit transform chain, not a pose-array copy. In integrated mode, `InputMux` selects VIVE wrists, MANUS fingers and Quest switches; quest-only is another explicit mode. The lesson's `integrated_frame` provides synthetic samples and a known 0.05 m frame translation, so it tests source selection and transform arithmetic without claiming live calibration.

### Calculation and units

$$
T_{world,wrist}=T_{world,device}T_{device,tracker}T_{tracker,wrist}
$$

Each T is a finite right-handed 4×4 rigid transform. Translation uses m, rotation is dimensionless and exported poses use xyz+xyzw. Multiplication order matters: the wrist mount offset rotates with the tracked orientation. Worked calculation, not calibration: identity rotations with device x=0.3 m and world translation +0.05 m yield world x=0.35 m.

```python
import numpy as np
world_from_device = np.eye(4)
world_from_device[0, 3] = 0.05
point = np.array([0.3, 0.0, 0.0, 1.0])
assert np.isclose((world_from_device @ point)[0], 0.35)
```

## Code connection

### Source trace

[`src/pai_lab/teleop_sources.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_sources.py)

`examples/sim-teleop-02/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

See also [`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py) and the [VR verification record](../../verification/vr-teleop-2026-11-13.md).

## Try it

### Controlled comparison

Change only synthetic input displacement `variant` 1→0.8; preserve world/mount matrices, source mode, sample count and switches. Pose values can change while accepted-frame counts remain identical. For a paper transform sensitivity, change one mount translation separately; never call that the same input-displacement experiment.

```bash
pal lesson run sim-teleop-02 --headless --seed 7 --samples 16 --variant 0.8 --output-dir .local/runs/sim-teleop-02/comparison-01 --json
pal lesson check sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --json
pal lesson check sim-teleop-02 --run-dir .local/runs/sim-teleop-02/comparison-01 --json
pal lesson compare sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --comparison-run-dir .local/runs/sim-teleop-02/comparison-01 --output-dir .local/comparisons/sim-teleop-02/comparison-01 --json
```

## Recovery

Keep interrupted episodes; saved, discarded and aborted states are distinct. Never overwrite an existing episode or resume control after reconnect without local rearm.

## Checkpoint

### Check understanding

Why choose the oldest receive time? Every selected source must be fresh. Can a correct 4×4 synthetic transform certify a physical mount? No; real calibration and live stream evidence are separate.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --comparison-run-dir .local/runs/sim-teleop-02/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-teleop-02 --run-dir .local/runs/sim-teleop-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-06](./sim-enlight-06.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
