# core-enlight-02 — Enlight MuJoCo draft and cross-format validation

This lesson checks **Enlight MuJoCo draft and cross-format validation** through the `cross-format-validation` implementation and its `cross-format.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `core` / `enlight` |
| Legacy alias | `T10A` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `macos-arm64`, `linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `core-enlight-01` |
| Safety | `simulation` |
| Verification | `ci-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `cross-format.json` produced by `cross-format-validation`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile core --json
pal lesson check core-enlight-02 --json
```

## Action

```bash
pal lesson run core-enlight-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/core-enlight-02/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `cross-format.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check core-enlight-02 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile core --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `cross-format-validation` operation and computes `joint_match_ratio`. Verification uses the lesson-specific `cross-format.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `flexiv-description`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run core-enlight-02 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `ci-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `cross-format.json`.

## Next lesson

Next catalog item: [core-wuji-01](./core-wuji-01.md) — Wuji Hand 2 Beta 2 joints, poses, and synergies
