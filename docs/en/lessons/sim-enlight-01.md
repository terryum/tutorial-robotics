# sim-enlight-01 — Enlight ROS 2 fake hardware

This lesson checks **Enlight ROS 2 fake hardware** through the `ros-fake-hardware` implementation and its `fake-hardware.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `enlight` |
| Legacy alias | `T18` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `core-enlight-01`, `sim-ros-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `fake-hardware.json` produced by `ros-fake-hardware`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile ros --json
pal lesson check sim-enlight-01 --json
```

## Action

```bash
pal lesson run sim-enlight-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-enlight-01/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `fake-hardware.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-enlight-01 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile ros --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `ros-fake-hardware` operation and computes `interface_count`. Verification uses the lesson-specific `fake-hardware.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `flexiv-ros2`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-enlight-01 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `fake-hardware.json`.

## Next lesson

Next catalog item: [sim-enlight-02](./sim-enlight-02.md) — Enlight contact-task simulation and candidate bundle
