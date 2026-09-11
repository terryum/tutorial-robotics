# core-aloha-01 — ALOHA simulation and ACT contract

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / aloha` |
| Legacy alias | `T30` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-data-01, core-il-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Run the dual-arm ALOHA model and build an ACT-shaped batch.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-aloha-01 --json
```

## Action

```bash
pal lesson run core-aloha-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-aloha-01/baseline-01 --json
```

## Expected

Inspect act-batch.npz shapes, observation.png and the fourteen action channels. Changing the first target amplitude should change the motion while preserving batch dimensions.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-aloha-01 --run-dir .local/runs/core-aloha-01/baseline-01 --json
```

## How it works

An action chunk contains a sequence of future actions. The model has fourteen actuator targets and the contract uses a sixteen-step horizon. This lesson records real model state and an RGB observation but deliberately does not train ACT.

```text
action batch shape = (samples, 16, 14)
```

## Code connection

`examples/core-aloha-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

First actuator target amplitude: 0.05 → 0.075 rad. Other targets and the 16×14 chunk shape remain fixed.

```bash
pal lesson run core-aloha-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-aloha-01/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-aloha-01 --run-dir .local/runs/core-aloha-01/baseline-01 --comparison-run-dir .local/runs/core-aloha-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-aloha-01 --run-dir .local/runs/core-aloha-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-vla-01](./core-vla-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
