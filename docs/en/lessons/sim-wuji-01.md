# sim-wuji-01 — Wuji in-hand PPO on GPU

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / wuji` |
| Legacy alias | `T27` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-wuji-02, core-rl-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Train and evaluate the pinned Wuji MJLab reorientation task.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-wuji-01 --json
```

## Action

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-wuji-01/baseline-01 --json
```

## Expected

Require changed policy tensors, finite evaluation rewards and a nonblank image. Short-run success remains distinct from successful in-hand manipulation.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

## How it works

The vendor task registers its own hand, object, reward and PPO runner. Use its supported Pixi environment, prepared assets and a separate local output directory. The vendor training embodiment is not automatically a calibrated Beta 2 hardware model.

```text
evaluation = saved policy(observation) in the registered GPU task
```

## Code connection

`examples/sim-wuji-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/gpu.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Sample budget: 64 → 96. Training lessons derive optimizer iterations from this budget and evaluate for this many steps; candidate-only lessons change evaluation length.

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --output-dir .local/runs/sim-wuji-01/comparison-01 --samples 96 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --comparison-run-dir .local/runs/sim-wuji-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-vla-01](./sim-vla-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
