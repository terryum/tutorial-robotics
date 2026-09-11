# sim-ros-04 — Common embodiment API for simulation and ROS 2

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / ros2` |
| Legacy alias | `T21` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `sim-ros-02` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Inspect a common reset/observe/act/close interface over simulation and ROS.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-ros-04 --json
```

## Action

```bash
pal lesson run sim-ros-04 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-ros-04/baseline-01 --json
```

## Expected

Read embodiment-contract.json and compare the operation counts with the trace. Check cleanup after a failed communication attempt.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --json
```

## How it works

An embodiment interface specifies lifecycle, units and ordering. The reset service acts on MuJoCo, observe reads the subscriber, act changes only simulation input, and finally destroys ROS entities. Hardware adapters need their own approval gates.

```text
reset → observe → act → observe → close
```

## Code connection

`examples/sim-ros-04/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/ros.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Sinusoidal simulation control amplitude: 0.1 → 0.15 in the actuator contract; message count and QoS stay fixed.

```bash
pal lesson run sim-ros-04 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-ros-04/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --comparison-run-dir .local/runs/sim-ros-04/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-g1-01](./sim-g1-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
