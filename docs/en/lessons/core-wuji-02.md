# core-wuji-02 — Wuji virtual tactile observation

This lesson checks **Wuji virtual tactile observation** through the `virtual-tactile` implementation and its `tactile-grid.csv` artifact.

| Field | Value |
|---|---|
| Stage / track | `core` / `wuji` |
| Legacy alias | `T15` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `macos-arm64`, `linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `core-wuji-01` |
| Safety | `simulation` |
| Verification | `ci-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `tactile-grid.csv` produced by `virtual-tactile`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile core --json
pal lesson check core-wuji-02 --json
```

## Action

```bash
pal lesson run core-wuji-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/core-wuji-02/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `tactile-grid.csv`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check core-wuji-02 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile core --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `virtual-tactile` operation and computes `contact_centroid`. Verification uses the lesson-specific `tactile-grid.csv` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `wuji-description`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run core-wuji-02 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `ci-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [core-dexterity-01](./core-dexterity-01.md) — Wuji and Sharpa model comparison
