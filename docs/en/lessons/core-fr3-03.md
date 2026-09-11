# core-fr3-03 — FR3 gravity compensation and feedforward

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `T07` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Measure how gravity feedforward changes tracking error.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-fr3-03 --json
```

## Action

```bash
pal lesson run core-fr3-03 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-03/baseline-01 --json
```

## Expected

Reviewed maintainer example from the pinned public model; your local run must be checked separately.

![core-fr3-03 frame.png](../../assets/examples/core-fr3-03-frame.png)

![core-fr3-03 plot.png](../../assets/examples/core-fr3-03-plot.png)

Read without_compensation_error and final_error. Compensation must reduce the measured norm. Torque arrays are in Nm; the reported tracking metric is in rad.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-fr3-03 --run-dir .local/runs/core-fr3-03/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect core-fr3-03 --run-dir .local/runs/core-fr3-03/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/core-fr3-03/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/core-fr3-03/baseline-01/experiment.json
```

## How it works

qfrc_bias contains gravity and velocity-dependent bias forces. The lesson compares identical PD gains with and without this term. Compensation uses the simulated model, so it is not evidence that a physical robot's payload is correct.

$$
M(q)\ddot q+c(q,\dot q)+g(q)=\tau+J^Tf_{ext}
$$

Symbols, units and assumptions: M: kg m²; qddot: rad/s²; c,g,torque: Nm; J: m/rad; f: N.

Worked calculation (not a measured run result): 21.6 Nm PD + 4 Nm bias = 25.6 Nm before clipping.

Practical connection: qfrc_bias includes velocity terms as well as gravity; incorrect payload breaks compensation.

## Code connection

`examples/core-fr3-03/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

PD gain: kp 120 → 180 Nm/rad, with kd determined by the same rule. Both compensation branches use identical gains.

```bash
pal lesson run core-fr3-03 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-03/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare core-fr3-03 --run-dir .local/runs/core-fr3-03/baseline-01 --comparison-run-dir .local/runs/core-fr3-03/comparison-01 --output-dir .local/comparisons/core-fr3-03/comparison-01 --json
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
pal lesson review core-fr3-03 --run-dir .local/runs/core-fr3-03/baseline-01 --comparison-run-dir .local/runs/core-fr3-03/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-fr3-03 --run-dir .local/runs/core-fr3-03/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-04](./core-fr3-04.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
