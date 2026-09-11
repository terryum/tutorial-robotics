# sim-ros-04 — Common embodiment API for simulation and ROS 2

This lesson checks **Common embodiment API for simulation and ROS 2** through the `embodiment-api` implementation and its `embodiment-contract.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `ros2` |
| Legacy alias | `T21` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `sim-ros-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `embodiment-contract.json` produced by `embodiment-api`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile ros --json
pal lesson check sim-ros-04 --json
```

## Action

```bash
pal lesson run sim-ros-04 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-ros-04/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `embodiment-contract.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-ros-04 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile ros --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `embodiment-api` operation and computes `interface_count`. Verification uses the lesson-specific `embodiment-contract.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `ros2-jazzy`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-ros-04 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `maintainer-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `embodiment-contract.json`.

## Next lesson

Next catalog item: [sim-g1-01](./sim-g1-01.md) — Unitree G1 GPU PPO and motion imitation
