# sim-wuji-01 — Wuji in-hand PPO on GPU

This lesson checks **Wuji in-hand PPO on GPU** through the `gpu-inhand-ppo` implementation and its `inhand-learning.csv` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `wuji` |
| Legacy alias | `T27` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-wuji-02`, `core-rl-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `inhand-learning.csv` produced by `gpu-inhand-ppo`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile gpu --json
pal lesson check sim-wuji-01 --json
```

## Action

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-wuji-01/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `inhand-learning.csv`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-wuji-01 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile gpu --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `gpu-inhand-ppo` operation and computes `yaw_gain`. Verification uses the lesson-specific `inhand-learning.csv` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `wuji-description`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-wuji-01 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `inhand-learning.csv`.

## Next lesson

Next catalog item: [sim-vla-01](./sim-vla-01.md) — SmolVLA fine-tuning and policy server
