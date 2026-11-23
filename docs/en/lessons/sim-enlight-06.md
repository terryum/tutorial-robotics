<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-enlight-06.md" lang="ko">한국어</a> | <a href="sim-enlight-06.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-06 — Enlight arm teleoperation and collection

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-enlight-05, sim-teleop-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Collection closes a data loop in simulation: synthetic wrist pose → Enlight-only IK → bounded arm action → camera/state/target episode → model-bound BC input. It does not connect a headset or physical arm. Three synthetic episodes are saved with one complete episode in each split. The gripper is unavailable and no human demonstration is claimed.

Read the prerequisite [concept chapter](../concepts/data-imitation.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How are timestamped simulated Enlight episodes collected without physical authority?

## Learning goals

Collection closes a data loop in simulation: synthetic wrist pose → Enlight-only IK → bounded arm action → camera/state/target episode → model-bound BC input.

How are timestamped simulated Enlight episodes collected without physical authority?

## Preflight

Use a host matching the catalog platforms and capabilities; computer names do not grant readiness. `core-teleop-01` supports macOS arm64 and Linux x86_64; the later optional input/collection lessons are cataloged for Linux x86_64. Read [VR setup](../setup/vr-teleop.md), [equipment stages](../equipment-stages.md) and the synthetic/live distinction in [verification](../../verification/vr-teleop-2026-11-13.md). Preserve devices, calibration and raw episodes under ignored `.local/`; no automatic vendor installation or device consent is implied.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-enlight-06 --headless --seed 7 --samples 16 --output-dir .local/runs/sim-enlight-06/baseline-01 --json
```

## Expected

Expect synthetic replay/collection evidence, not a live-device acceptance report. Inspect the catalog artifact, `experiment.json`, `trace.csv`, `plot.png` and episode manifests. Three saved episodes plus discarded/aborted records preserve lifecycle and provenance. Actual 60-second device-rate/tracking/occlusion/reconnect acceptance belongs to the separate live-input gate.

## Observe

Inspect recorded input and applied targets separately; synthetic timestamps are generated test clocks.

### Reading the artifacts

`collected-demonstrations.json` records model=enlight, provenance=synthetic, 17-value observations and seven pre-transform actions with episode splits. `episodes/*/frames.jsonl` stores named pre-action state/target and a 64×64 RGB camera frame; state/camera and synthetic input clocks are recorded explicitly. The applied action leads to the plotted post-step TCP x. The summary metric is maximum absolute x error, not full 3D pose error. `human_demonstration=False`, `gripper_verified=False`, `command_publishers=0` remain visible.

## How it works

### Intuition

Collection closes a data loop in simulation: synthetic wrist pose → Enlight-only IK → bounded arm action → camera/state/target episode → model-bound BC input. It does not connect a headset or physical arm. Three synthetic episodes are saved with one complete episode in each split. The gripper is unavailable and no human demonstration is claimed.

### Calculation and units

$$
\Delta q=J^T(JJ^T+0.001I_6)^{-1}e,\qquad a=\operatorname{arctanh}(\operatorname{clip}((q^*-q)/0.03,-0.999,0.999))
$$

The stacked Jacobian J is 6×7: position rows map rad to world m and rotational rows map to rotation-vector rad. Error e combines position and orientation; its mixed scales are a teaching numerical choice, not a physically uniform norm. IK increments clip to ±0.02 rad and model limits. Worked calculation, not device data: desired delta 0.003 rad gives pre-transform action arctanh(0.1)≈0.100335.

```python
import numpy as np
a = np.arctanh(0.003 / 0.03)
assert np.isclose(0.03 * np.tanh(a), 0.003)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/teleop.py)

`examples/sim-enlight-06/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

See also [`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py) and the [VR verification record](../../verification/vr-teleop-2026-11-13.md).

## Try it

### Controlled comparison

Change only `variant` 1→0.8: the synthetic wrist x sinusoid amplitude changes 0.005→0.004 m, while orientation, samples and 20 ms frame schedule remain fixed. Compare target and post-step x plus episode data. Optional subsequent BC is a new training run with the explicit demonstration file; inspect independent evaluation separately. The public short collected-BC example achieved 0/20, not deployable performance.

```bash
pal lesson run sim-enlight-06 --headless --seed 7 --samples 16 --variant 0.8 --output-dir .local/runs/sim-enlight-06/comparison-01 --json
pal lesson check sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --json
pal lesson check sim-enlight-06 --run-dir .local/runs/sim-enlight-06/comparison-01 --json
pal lesson compare sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --comparison-run-dir .local/runs/sim-enlight-06/comparison-01 --output-dir .local/comparisons/sim-enlight-06/comparison-01 --json
```

## Recovery

Keep interrupted episodes; saved, discarded and aborted states are distinct. Never overwrite an existing episode or resume control after reconnect without local rearm.

## Checkpoint

### Check understanding

Why keep episodes disjoint? Otherwise neighboring collection states leak into held-out data. Does small collected x error ensure BC reaches unseen targets? No; data collection and policy evaluation answer different questions.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --comparison-run-dir .local/runs/sim-enlight-06/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-06 --run-dir .local/runs/sim-enlight-06/baseline-01 --json
```

Optional follow-on training, after inspecting collection. This creates a separate training artifact, not another lesson completion:

```bash
pal train run --model enlight --algorithm bc --epochs 4 --demonstrations .local/runs/sim-enlight-06/baseline-01/collected-demonstrations.json --output-dir .local/teleop-bc-unique --json
```

<!-- pal:navigation:start -->
## Next lesson

Course end

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
