# core-01 — Deterministic pendulum state and timestep

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `T01` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-00` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Measure pendulum state and numerical energy drift.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

```bash
pal host detect --json
pal lesson check core-01 --json
```

## Action

```bash
pal lesson run core-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-01/baseline-01 --json
```

## Expected

Measured development example. Read both axis units and the reference/measured difference first. Validate your own run separately.

![core-01 measured plot](../../assets/examples/core-01-plot.png)

Compare the measured energy trace with its initial value. The maximum absolute drift must remain below 1e-5 J; inspect q and qdot separately in experiment.json.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-01 --run-dir .local/runs/core-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect core-01 --run-dir .local/runs/core-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/core-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/core-01/baseline-01/experiment.json
```

## How it works

MuJoCo integrates q (rad) and qdot (rad/s). For an unforced rigid pendulum, total kinetic plus potential energy is constant; numerical integration introduces drift. The capsule has distributed mass, so do not substitute a point-mass inertia.

$$
E=K+U,\qquad d=\max_t |E(t)-E(0)|
$$

Symbols, units and assumptions: K,U,E,d: J; t: s; unforced, frictionless model.

Worked calculation (not a measured run result): |1.000003-1.000000|=0.000003 J.

Practical connection: Energy drift detects integration error before controller tuning.

## Code connection

`examples/core-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Integration step: 0.002 → 0.004 s. Fixed sample count also doubles the observed duration; compare energy drift, not equal-time terminal state.

```bash
pal lesson run core-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-01/comparison-01 --variant 2 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare core-01 --run-dir .local/runs/core-01/baseline-01 --comparison-run-dir .local/runs/core-01/comparison-01 --output-dir .local/comparisons/core-01/comparison-01 --json
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
pal lesson review core-01 --run-dir .local/runs/core-01/baseline-01 --comparison-run-dir .local/runs/core-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-01 --run-dir .local/runs/core-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-02](./core-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
