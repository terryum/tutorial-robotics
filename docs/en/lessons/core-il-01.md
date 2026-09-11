# core-il-01 — Behavioral cloning baseline

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / learning` |
| Legacy alias | `T29` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-data-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Fit behavioral cloning to the completed episode dataset.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

```bash
pal host detect --json
pal lesson check core-il-01 --json
```

## Action

```bash
pal lesson run core-il-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-il-01/baseline-01 --json
```

## Expected

Verify the source dataset hash, decreasing train loss, heldout_mse below 0.1, and exact saved-policy reload. variant changes learning rate only.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-il-01 --run-dir .local/runs/core-il-01/baseline-01 --json
```

## How it works

A linear policy regresses demonstrator torque from angle, velocity and bias. Episodes 0–5 train the policy; episodes 6–7 are held out. A small imitation loss does not prove stability under states that the demonstrator never visited.

```text
L_BC = mean ‖Wᵀ[q,qdot,1] − a_demo‖²
```

## Code connection

`examples/core-il-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Regression learning rate: 0.15 → 0.225; use the same saved dataset and episode split.

```bash
pal lesson run core-il-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-il-01/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-il-01 --run-dir .local/runs/core-il-01/baseline-01 --comparison-run-dir .local/runs/core-il-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-il-01 --run-dir .local/runs/core-il-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-aloha-01](./core-aloha-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
