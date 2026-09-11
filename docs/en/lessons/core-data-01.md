# core-data-01 — Episode dataset from MuJoCo

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / learning` |
| Legacy alias | `T28` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Record real MuJoCo state/action/next-state transitions.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

```bash
pal host detect --json
pal lesson check core-data-01 --json
```

## Action

```bash
pal lesson run core-data-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-data-01/baseline-01 --json
```

## Expected

Measured development example. Read both axis units and the reference/measured difference first. Validate your own run separately.

![core-data-01 measured plot](../../assets/examples/core-data-01-plot.png)

There should be 8×samples transitions with rad/rad/s observations and Nm actions. Inspect episode boundaries and verify that next states actually change.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-data-01 --run-dir .local/runs/core-data-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect core-data-01 --run-dir .local/runs/core-data-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/core-data-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/core-data-01/baseline-01/experiment.json
```

## How it works

Eight pendulum episodes use a bounded PD demonstrator. The dataset stores state before action and state after stepping, episode/step IDs, and truncation. Split by episode for BC so adjacent correlated frames do not leak into evaluation.

$$
d_t=(s_t,a_t,s_{t+1},terminated_t,truncated_t)
$$

Symbols, units and assumptions: s=[q(rad), velocity(rad/s)]; a: bounded Nm; timestamps s.

Worked calculation (not a measured run result): 8 episodes × 64 transitions = 512 transitions.

Practical connection: Split by episode to keep correlated adjacent frames out of held-out evaluation.

## Code connection

`examples/core-data-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Demonstrator proportional gain: 2 → 3 Nm/rad; derivative gain and the ±3 Nm torque bound remain fixed.

```bash
pal lesson run core-data-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-data-01/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare core-data-01 --run-dir .local/runs/core-data-01/baseline-01 --comparison-run-dir .local/runs/core-data-01/comparison-01 --output-dir .local/comparisons/core-data-01/comparison-01 --json
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
pal lesson review core-data-01 --run-dir .local/runs/core-data-01/baseline-01 --comparison-run-dir .local/runs/core-data-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-data-01 --run-dir .local/runs/core-data-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-dexterity-02](./core-dexterity-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
