<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-enlight-01.md" lang="ko">한국어</a> | <a href="sim-enlight-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-01 — Enlight ROS 2 fake hardware

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `T18` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `core-enlight-01, sim-ros-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the prerequisite [concept chapter](../concepts/ros.md) and [equipment progression](../equipment-stages.md). This lesson addresses: What does fake hardware verify before any device connection? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

Fake hardware separates communication from physical authority.

What does fake hardware verify before any device connection?

## Preflight

Device setup and manual references: [Enlight](../setup/enlight.md).

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-enlight-01 --json
```

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-enlight-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-enlight-01/baseline-01 --json
```

## Expected

Inspect the seven joint names, exact received state and reset result. Verify all ROS entities close on failure or completion.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-enlight-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-enlight-01/baseline-01/experiment.json
```

### Reading the artifacts

Read `qos`, `domain`, `localhost_only`, `source`, topic/service graph and top-level `checks` in `experiment.json`. This path uses reliable depth 10, localhost-only domain 217, service and receive deadlines. `state_equal`, `all_messages_received`, `tf_received` and `service_roundtrip` must correspond to actual DDS traffic. A static identity TF does not calibrate the real arm.

## How it works

### Intuition

Fake hardware separates communication from physical authority. Here `ros.run` loads the Enlight MuJoCo draft, steps its simulated dynamics and publishes named joint state in an isolated ROS context. The Trigger reset service resets simulation. It does not open a production Flexiv driver or establish RDK/firmware compatibility.

### Calculation and units

$$
e_{msg}=\max_i|q^{sent}_{i,0}-q^{received}_{i,0}|
$$

First-joint position is rad, timestamp is simulated seconds split into ROS seconds/nanoseconds, and velocity is rad/s. The maximum sent/received error is a transport check, not tracking-to-target error. Worked calculation, not DDS measurement: sending and receiving 0.2 rad gives zero error.

```python
sent_rad, received_rad = 0.2, 0.2
assert abs(sent_rad - received_rad) == 0.0
```

## Code connection

### Source trace

[`src/pai_lab/lessons/ros.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/ros.py)

`examples/sim-enlight-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Change only the sinusoidal simulated input multiplier `variant`; keep seed, sample count and model fixed. Positions may change while message equality remains exact. Do not interpret reliable QoS as a real-time control guarantee.

```bash
pal lesson run sim-enlight-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-enlight-01/comparison-01 --json
pal lesson check sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
pal lesson check sim-enlight-01 --run-dir .local/runs/sim-enlight-01/comparison-01 --json
pal lesson compare sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --comparison-run-dir .local/runs/sim-enlight-01/comparison-01 --output-dir .local/comparisons/sim-enlight-01/comparison-01 --json
```

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

### Check understanding

Why can zero communication error coexist with poor motion? The bridge can faithfully transmit an undesirable state. Does fake hardware test the real Flexiv network? No.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --comparison-run-dir .local/runs/sim-enlight-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-02](./sim-enlight-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
