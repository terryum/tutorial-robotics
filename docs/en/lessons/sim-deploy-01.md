# sim-deploy-01 — Candidate deployment bundle and promotion gate

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / deployment` |
| Legacy alias | `T35A` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `core-fr3-08` |
| Safety | `offline` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Assemble a candidate from the actual FR3 PPO policy and its evidence.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

```bash
pal host detect --json
pal lesson check sim-deploy-01 --json
```

## Action

```bash
pal lesson run sim-deploy-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-deploy-01/baseline-01 --json
```

## Expected

Measured development example. Read both axis units and the reference/measured difference first. Validate your own run separately.

![sim-deploy-01 measured plot](../../assets/examples/sim-deploy-01-plot.png)

Open sample_candidate/manifest.json and compare its policy hash with the completed core-fr3-08 run. Execute every deterministic test vector. No promotion or hardware authority follows.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-deploy-01 --run-dir .local/runs/sim-deploy-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-deploy-01 --run-dir .local/runs/sim-deploy-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-deploy-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-deploy-01/baseline-01/experiment.json
```

## How it works

A reproducible bundle includes policy bytes, observation/action semantics, processor contract, lock hash, test vectors and rollback. The bundle remains candidate-only because optimizer smoke is not task-performance validation.

$$
e=\|\pi_{loaded}(o)-a_{expected}\|_{\infty}
$$

Symbols, units and assumptions: o and a use saved policy contract; normalized output unless declared otherwise.

Worked calculation (not a measured run result): expected [0.1,0.2], loaded [0.1,0.2] → e=0.

Practical connection: Checksum, input order and test vectors must refer to the same checkpoint.

## Code connection

`examples/sim-deploy-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/deployment.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Seed: 7 → 8. Structural audits, fixed model views and deterministic inference can remain identical. A remote service may vary independently of this local seed; record that limitation.

```bash
pal lesson run sim-deploy-01 --headless --samples 64 --output-dir .local/runs/sim-deploy-01/comparison-01 --seed 8 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare sim-deploy-01 --run-dir .local/runs/sim-deploy-01/baseline-01 --comparison-run-dir .local/runs/sim-deploy-01/comparison-01 --output-dir .local/comparisons/sim-deploy-01/comparison-01 --json
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
pal lesson review sim-deploy-01 --run-dir .local/runs/sim-deploy-01/baseline-01 --comparison-run-dir .local/runs/sim-deploy-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-deploy-01 --run-dir .local/runs/sim-deploy-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-01](./sim-enlight-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
