# core-fr3-07 — FR3 reach environment without ROS

This lesson checks **FR3 reach environment without ROS** through the `reach-environment` implementation and its `reach-rollout.csv` artifact.

| Field | Value |
|---|---|
| Stage / track | `core` / `fr3` |
| Legacy alias | `T22` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `macos-arm64`, `linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `core-fr3-04` |
| Safety | `simulation` |
| Verification | `ci-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `reach-rollout.csv` produced by `reach-environment`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile core --json
pal lesson check core-fr3-07 --json
```

## Action

```bash
pal lesson run core-fr3-07 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/core-fr3-07/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `reach-rollout.csv`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check core-fr3-07 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile core --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `reach-environment` operation and computes `terminal_distance`. Verification uses the lesson-specific `reach-rollout.csv` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `gymnasium`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run core-fr3-07 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `ci-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [core-fr3-08](./core-fr3-08.md) — PPO on FR3 reach
