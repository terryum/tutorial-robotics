<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-cross-01.md" lang="ko">한국어</a> | <a href="sim-cross-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-cross-01 — MuJoCo to Isaac sim-to-sim validation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / cross` |
| Legacy alias | `T35` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `isaac-sim` |
| Prerequisites | `core-fr3-08, sim-isaac-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the prerequisite [concept chapter](../concepts/physx.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which conditions must match before comparing two physics engines? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

Compare two actual engines using matched initial state and the same applied effort.

Which conditions must match before comparing two physics engines?

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-cross-01 --json
```

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-cross-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-cross-01/baseline-01 --json
```

## Expected

Inspect every engine's qpos and aggregate RMSE. The initial acceptance bound is 0.15 rad; exceeding it is a failed experiment requiring diagnosis, not a waived gate.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-cross-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-cross-01/baseline-01/experiment.json
```

### Reading the artifacts

Inspect `experiment.json` → `payload`: `joint_order`, `isaac_joint_indices`, `states`, `state_rmse_rad`, `comparison`, `dt_s` and camera/depth fields. `isaac-observations.json` preserves the same engine payload. `state_parity` requires RMS below 0.15 rad, a teaching acceptance threshold, not hardware tolerance. Read mapped per-joint traces as well as the scalar.

## How it works

### Intuition

Compare two actual engines using matched initial state and the same applied effort. `isaac.run` switches the imported Wuji articulation to effort control, disables MuJoCo actuation, then steps MuJoCo and PhysX once for each sample. Joint names establish the PhysX index mapping; visual similarity cannot establish joint-order parity. This is a dynamics comparison, unlike setting both engines to prescribed poses.

### Calculation and units

$$
e=\sqrt{\frac{1}{Nn}\sum_{i=1}^N\sum_{j=1}^n(q^M_{ij}-q^P_{ij})^2}
$$

`states` has N samples of n named revolute coordinates in rad; the reported scalar is rad. Baseline physics step is 0.002 s, with effort `0.002 * variant * sin(0.1*i)` N m. This root-mean-square averages joints and time; it is not maximum error. Worked calculation, not an engine measurement: differences [0.01, -0.01] rad give RMS 0.01 rad.

```python
import numpy as np
difference_rad = np.array([0.01, -0.01])
assert np.isclose(np.sqrt(np.mean(difference_rad**2)), 0.01)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/isaac.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac.py)

`examples/sim-cross-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

## Try it

### Controlled comparison

Change only `variant`, which scales effort on both engines. Keep seed, imported source, pose and sample count fixed. Larger effort may expose drive or contact differences; it need not improve parity. This comparison needs a real Isaac host; no portable substitution can establish PhysX behavior.

```bash
pal lesson run sim-cross-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-cross-01/comparison-01 --json
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/comparison-01 --json
pal lesson compare sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --comparison-run-dir .local/runs/sim-cross-01/comparison-01 --output-dir .local/comparisons/sim-cross-01/comparison-01 --json
```

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

### Check understanding

Why disable MuJoCo actuation? To avoid an additional actuator controller changing the effort experiment. Does RMS below 0.15 rad make a robot safe? No; it is this simulated comparison's criterion.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --comparison-run-dir .local/runs/sim-cross-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-deploy-01](./sim-deploy-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->


[Isaac 6.0 importer migration](https://docs.isaacsim.omniverse.nvidia.com/latest/migration_guides/isaac_sim_6_0/urdf_mjcf_importer_exporter_pipeline.html). Execution still requires verification on each prepared 5.1/6.0 host.
