# core-fr3-06 — FR3 contact and friction laboratory

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `T10` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-05` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Measure probe/table contact force and vary friction.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-fr3-06 --json
```

## Action

```bash
pal lesson run core-fr3-06 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-06/baseline-01 --json
```

## Expected

Measured development example. Read both axis units and the reference/measured difference first. Validate your own run separately.

![core-fr3-06 measured plot](../../assets/examples/core-fr3-06-plot.png)

Check actual probe/table contacts and positive measured force. Change only table friction from 0.6 to 0.9 using variant 1.5; inspect the force trace and image.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-fr3-06 --run-dir .local/runs/core-fr3-06/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect core-fr3-06 --run-dir .local/runs/core-fr3-06/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/core-fr3-06/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/core-fr3-06/baseline-01/experiment.json
```

## How it works

A small sphere is attached to the real FR3 tool link in a local derived scene. mj_contactForce reports contact-frame forces. The normal force is not simply the commanded downward force because transient motion and constraints contribute.

$$
\|f_t\|\leq\mu f_n
$$

Symbols, units and assumptions: ft,fn: contact-frame N; μ: dimensionless; ideal Coulomb friction cone.

Worked calculation (not a measured run result): μ=0.5, fn=10 N → tangential limit 5 N.

Practical connection: Measured contact force depends on solver, friction and tool calibration.

## Code connection

`examples/core-fr3-06/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Sliding friction coefficient: 0.6 → 0.9 (dimensionless). Purely normal loading may show little change; this is not a friction-identification test.

```bash
pal lesson run core-fr3-06 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-06/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare core-fr3-06 --run-dir .local/runs/core-fr3-06/baseline-01 --comparison-run-dir .local/runs/core-fr3-06/comparison-01 --output-dir .local/comparisons/core-fr3-06/comparison-01 --json
```

<details>
<summary>Optional: what changes when the assumptions fail?</summary>

Choose one input in the equation and write its units. Inspect whether doubling it doubles the output or whether clipping, normalization or coordinate transforms change that relationship. Changing another assumption or model at the same time needs a separate experiment.

</details>

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-fr3-06 --run-dir .local/runs/core-fr3-06/baseline-01 --comparison-run-dir .local/runs/core-fr3-06/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-fr3-06 --run-dir .local/runs/core-fr3-06/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-rl-01](./core-rl-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
