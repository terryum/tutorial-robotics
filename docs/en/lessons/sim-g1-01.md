# sim-g1-01 — Unitree G1 GPU PPO and motion imitation

This lesson checks **Unitree G1 GPU PPO and motion imitation** through the `gpu-motion-imitation` implementation and its `motion-imitation.csv` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `g1` |
| Legacy alias | `T26` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-g1-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `motion-imitation.csv` produced by `gpu-motion-imitation`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile gpu --json
pal lesson check sim-g1-01 --json
```

## Action

```bash
pal lesson run sim-g1-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-g1-01/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `motion-imitation.csv`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-g1-01 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile gpu --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `gpu-motion-imitation` operation and computes `reward_gain`. Verification uses the lesson-specific `motion-imitation.csv` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `unitree-g1`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-g1-01 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `motion-imitation.csv`.

## Next lesson

Next catalog item: [sim-wuji-01](./sim-wuji-01.md) — Wuji in-hand PPO on GPU
