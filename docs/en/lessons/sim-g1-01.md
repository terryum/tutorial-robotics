# sim-g1-01 — Unitree G1 GPU PPO and motion imitation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / g1` |
| Legacy alias | `T26` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-g1-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Train a G1 motion-imitation PPO task and evaluate its saved checkpoint.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-g1-01 --json
```

## Action

```bash
pal lesson run sim-g1-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-g1-01/baseline-01 --json
```

## Expected

Compare initial.pt and policy.pt tensors, evaluation rewards and evaluation.png. Missing reference motion or CUDA is capability-unavailable. Inspect the task name to prevent confusing velocity tracking with imitation.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-g1-01 --run-dir .local/runs/sim-g1-01/baseline-01 --json
```

## How it works

The pinned Unitree MJLab task uses GPU simulation and RSL-RL. A prepared reference-motion file is mandatory. A small number of optimizer iterations checks mechanics; measured evaluation reward and rendered state do not certify walking performance.

```text
PPO rollout → parameter update → checkpoint reload → GPU evaluation
```

## Code connection

`examples/sim-g1-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/gpu.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Sample budget: 64 → 96. Training lessons derive optimizer iterations from this budget and evaluate for this many steps; candidate-only lessons change evaluation length.

```bash
pal lesson run sim-g1-01 --headless --seed 7 --output-dir .local/runs/sim-g1-01/comparison-01 --samples 96 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review sim-g1-01 --run-dir .local/runs/sim-g1-01/baseline-01 --comparison-run-dir .local/runs/sim-g1-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-g1-01 --run-dir .local/runs/sim-g1-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-wuji-01](./sim-wuji-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
