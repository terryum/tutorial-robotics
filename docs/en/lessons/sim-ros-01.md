# sim-ros-01 — ROS 2 topics, QoS, services, actions, and TF

This lesson checks **ROS 2 topics, QoS, services, actions, and TF** through the `ros-graph-qos-tf` implementation and its `ros-graph.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `ros2` |
| Legacy alias | `T17` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `core-00`, `core-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `ros-graph.json` produced by `ros-graph-qos-tf`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile ros --json
pal lesson check sim-ros-01 --json
```

## Action

```bash
pal lesson run sim-ros-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-ros-01/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `ros-graph.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-ros-01 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile ros --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `ros-graph-qos-tf` operation and computes `graph_entity_count`. Verification uses the lesson-specific `ros-graph.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `ros2-jazzy`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-ros-01 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `maintainer-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `ros-graph.json`.

## Next lesson

Next catalog item: [sim-ros-02](./sim-ros-02.md) — MuJoCo to ROS 2 bridge
