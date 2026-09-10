# sim-ros-02 — MuJoCo to ROS 2 bridge

This lesson checks **MuJoCo to ROS 2 bridge** through the `ros-joint-bridge` implementation and its `joint-state-bridge.csv` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `ros2` |
| Legacy alias | `T19` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `core-04`, `sim-ros-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `joint-state-bridge.csv` produced by `ros-joint-bridge`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile ros --json
pal lesson check sim-ros-02 --json
```

## Action

```bash
pal lesson run sim-ros-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-ros-02/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `joint-state-bridge.csv`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-ros-02 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile ros --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `ros-joint-bridge` operation and computes `timestamp_error`. Verification uses the lesson-specific `joint-state-bridge.csv` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `ros2-jazzy`, `mujoco-ros2-core`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-ros-02 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `maintainer-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [sim-ros-03](./sim-ros-03.md) — Rosbag episode recording and deterministic replay
