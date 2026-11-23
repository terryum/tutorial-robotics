<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-enlight-02.md" lang="ko">한국어</a> | <a href="sim-enlight-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-02 — Enlight contact-task simulation and candidate bundle

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `T41A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-enlight-02, sim-deploy-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the prerequisite [concept chapter](../concepts/deployment-hardware.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Why does a contact-task bundle remain a candidate until gated evaluation? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

This candidate is a known controller, not a learned policy.

Why does a contact-task bundle remain a candidate until gated evaluation?

## Preflight

Device setup and manual references: [Enlight](../setup/enlight.md).

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-enlight-02 --json
```

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-enlight-02 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-enlight-02/baseline-01 --json
```

## Expected

Require actual probe/table force, finite bounded control and rendered geometry. Inspect candidate-controller.json and contact-actions.npz; keep hardware_compatible false.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-enlight-02/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-enlight-02/baseline-01/experiment.json
```

### Reading the artifacts

`contact-actions.npz` stores actual clipped commands. `candidate-controller.json` and `experiment.json` → `payload` report gains, `mean_normal_force_N`, `candidate_only=True`, `hardware_compatible=False` and rollback. The normal-force scalar averages sampled sums for the named probe/table pair; it is neither a learned checkpoint nor calibrated hardware force.

## How it works

### Intuition

This candidate is a known controller, not a learned policy. `enlight_contact` creates a derived probe/table scene from the Enlight model. MuJoCo integrates dynamics while Torch computes a 28-value controller input on CUDA. GPU arithmetic here is not PhysX simulation or Isaac Lab training.

### Calculation and units

$$
\tau=\operatorname{clip}(80(q^*-q)-12\dot q+b+J^T[0,0,-2v]^T,\tau_{min},\tau_{max})
$$

Seven position errors, seven velocities, seven bias terms and seven Jacobian-force terms form 28 inputs. Angles use rad, velocities rad/s, bias/torque N m and force world-frame N; v is dimensionless `variant`. Worked calculation, not measured contact: 80×0.01−12×0.02=0.56 N m before bias and force terms.

```python
import numpy as np
raw_nm = 80 * 0.01 - 12 * 0.02
assert np.isclose(raw_nm, 0.56)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/gpu.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/gpu.py)

`examples/sim-enlight-02/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Change only `variant` from 1 to 1.5: requested downward world force changes 2→3 N while PD gains remain 80 and 12. Compare measured force and applied torque; saturation or geometry may prevent a proportional response. Missing CUDA remains unavailable even though dynamics use MuJoCo.

```bash
pal lesson run sim-enlight-02 --headless --seed 7 --samples 64 --variant 1.5 --output-dir .local/runs/sim-enlight-02/comparison-01 --json
pal lesson check sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
pal lesson check sim-enlight-02 --run-dir .local/runs/sim-enlight-02/comparison-01 --json
pal lesson compare sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --comparison-run-dir .local/runs/sim-enlight-02/comparison-01 --output-dir .local/comparisons/sim-enlight-02/comparison-01 --json
```

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

### Check understanding

What was trained? Nothing in this path; gains are fixed. What does positive contact prove? Simulated named probe/table contact occurred, not safe physical force control.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --comparison-run-dir .local/runs/sim-enlight-02/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-wuji-02](./sim-wuji-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
