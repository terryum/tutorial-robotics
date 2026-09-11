# sim-cross-01 — MuJoCo to Isaac sim-to-sim validation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / cross` |
| Legacy alias | `T35` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `isaac-sim` |
| Prerequisites | `core-fr3-08, sim-isaac-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Compare MuJoCo and PhysX joint trajectories under matching input.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-cross-01 --json
```

## Action

```bash
pal lesson run sim-cross-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-cross-01/baseline-01 --json
```

## Expected

Inspect every engine's qpos and aggregate RMSE. The initial acceptance bound is 0.15 rad; exceeding it is a failed experiment requiring diagnosis, not a waived gate.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

## How it works

The same public Wuji hand starts from matched joint positions and velocities. Name-based mapping applies the same efforts at 2 ms steps. Different contact, drive and solver semantics may create drift. This test measures parity; it does not assert a learned policy transfers safely.

```text
RMSE = sqrt(mean((q_MuJoCo − q_PhysX)²))
```

## Code connection

`examples/sim-cross-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/isaac.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

```bash
pal lesson run sim-cross-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-cross-01/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --comparison-run-dir .local/runs/sim-cross-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-deploy-01](./sim-deploy-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
