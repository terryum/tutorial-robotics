<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-03.md" lang="ko">한국어</a> | <a href="core-03.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-03 — Multi-model inspection and asset validation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `T03` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-01, core-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the [simulation concept chapter](../concepts/simulation.md), then locate this lesson in the [equipment progression](../equipment-stages.md).

## Learning goals

Load six robot models and inspect their actual dimensions.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch mujoco-menagerie
pal assets fetch wuji-description-beta2
pal assets fetch flexiv-description
```

```bash
pal host detect --json
pal lesson check core-03 --json
```

## Action

```bash
pal lesson run core-03 --headless --seed 7 --samples 64 --output-dir .local/runs/core-03/baseline-01 --json
```

## Expected

Measured development example. Read both axis units and the reference/measured difference first. Validate your own run separately.

![core-03 measured plot](../../assets/examples/core-03-plot.png)

Read joint names, limits, total mass and nq/nv/nu for FR3, Enlight, Wuji, Sharpa, G1 and ALOHA. Enlight's local draft is derived from pinned vendor parameters.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-03 --run-dir .local/runs/core-03/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect core-03 --run-dir .local/runs/core-03/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/core-03/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/core-03/baseline-01/experiment.json
```

## How it works

nq counts configuration coordinates; nv counts velocity coordinates. A free joint has seven position coordinates but six velocity coordinates. nu counts actuators, so it need not equal either nq or nv.

$$
n_q=7,\quad n_v=6\quad\text{(one free joint)}
$$

Symbols, units and assumptions: Counts are dimensionless; quaternion has unit norm.

Worked calculation (not a measured run result): 3 position + 4 quaternion = 7; 3 linear + 3 angular = 6.

Practical connection: Do not index velocities using configuration addresses.

### From input to observation

Assuming every Python state-array length equals joint count fails for floating bases and multi-coordinate joints. nq counts configuration coordinates, nv velocity degrees of freedom, and nu actuator inputs. This lesson reads those distinctions from six compiled models. Equal counts do not establish equal action semantics.

## Code connection

`examples/core-03/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

### Read the actual producer and artifacts

Compare [`physics.py`](../../../src/pai_lab/lessons/physics.py) with dispatch in [`runner.py`](../../../src/pai_lab/lessons/runner.py).

`physics.run` uses `models.load` and `inventory` to save nq, nv, nu, joint_names, joint_ranges, site_names and mass_kg. `model-inventory.json` is keyed by model name. Distinguish qpos shape=(nq,), qvel shape=(nv,) and ctrl shape=(nu,). A free joint has 7 versus 6 because four quaternion values represent rotation. The graph compares nv; the scalar metric is the fraction of models with positive mass. Those are different summaries.

## Try it

This is an environment or structure audit. A seed change is not required. Compare names, units, prerequisites and the actual artifact; record specific findings in the review notes.

<details>
<summary>Optional: what changes when the assumptions fail?</summary>

Choose one input in the equation and write its units. Inspect whether doubling it doubles the output or whether clipping, normalization or coordinate transforms change that relationship. Changing another assumption or model at the same time needs a separate experiment.

</details>

### Predict before changing a value

For a one-variable calculation, adding only a free base adds 7 configuration and 6 velocity coordinates. The actual audit keeps pinned models fixed, so seed changes should leave dimensions unchanged. Do not alter vendor models to make an existing hash check pass.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-03 --run-dir .local/runs/core-03/baseline-01 --notes "Replace with inspected names, units, structure, limits and concrete evidence." --json
pal lesson finish core-03 --run-dir .local/runs/core-03/baseline-01 --json
```

### Check understanding and answer guide

Question: May you assume nu=nq? Answer: Read actuator semantics first. Question: Do positive mass and successful compilation prove contact or hardware calibration? Answer: They establish structural checks only. Record one model-specific array shape and name mapping.

This structural audit is explicitly exempted by `evidence.comparison_errors` from a separate comparison run. The review command above passes only the baseline. Record actual audit evidence in notes; do not represent a paper calculation as an executed comparison artifact.

<!-- pal:navigation:start -->
## Next lesson

[core-04](./core-04.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
