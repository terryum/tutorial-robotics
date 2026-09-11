# sim-vla-02 — Optional remote VLA inference

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / vla` |
| Legacy alias | `T32D` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `sim-vla-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Validate an explicitly configured optional remote policy response.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-vla-02 --json
```

## Action

```bash
pal lesson run sim-vla-02 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-vla-02/baseline-01 --json
```

## Expected

Check round-trip time, model_identity, finite actions and configured bounds. If the service is unavailable, retain failure evidence and leave this elective incomplete.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-vla-02 --run-dir .local/runs/sim-vla-02/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-vla-02 --run-dir .local/runs/sim-vla-02/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-vla-02/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-vla-02/baseline-01/experiment.json
```

## How it works

Transport, timeout, model identity, action dimension and bounds form the inference contract. Supply a prepared request file and HTTPS endpoint or local test server. The lesson validates and records returned actions without forwarding them to a robot.

$$
\forall i,\quad a_i\in\mathbb R,\quad |a_i|\leq a_{max}
$$

Symbols, units and assumptions: a: normalized action; limit: same units; finite values required.

Worked calculation (not a measured run result): limit 1.0, action 1.2 → reject.

Practical connection: Transport validation does not establish a neural policy is useful.

## Code connection

`examples/sim-vla-02/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/vla.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Seed: 7 → 8. Structural audits, fixed model views and deterministic inference can remain identical. A remote service may vary independently of this local seed; record that limitation.

```bash
pal lesson run sim-vla-02 --headless --samples 64 --output-dir .local/runs/sim-vla-02/comparison-01 --seed 8 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare sim-vla-02 --run-dir .local/runs/sim-vla-02/baseline-01 --comparison-run-dir .local/runs/sim-vla-02/comparison-01 --output-dir .local/comparisons/sim-vla-02/comparison-01 --json
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
pal lesson review sim-vla-02 --run-dir .local/runs/sim-vla-02/baseline-01 --comparison-run-dir .local/runs/sim-vla-02/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-vla-02 --run-dir .local/runs/sim-vla-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-isaac-01](./sim-isaac-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
