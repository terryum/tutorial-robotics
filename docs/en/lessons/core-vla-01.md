# core-vla-01 — VLA protocol and mock policy client

This lesson checks **VLA protocol and mock policy client** through the `vla-protocol` implementation and its `vla-request-response.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `core` / `vla` |
| Legacy alias | `T32A` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `macos-arm64`, `linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `core-data-01` |
| Safety | `simulation` |
| Verification | `ci-checked` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `vla-request-response.json` produced by `vla-protocol`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile core --json
pal lesson check core-vla-01 --json
```

## Action

```bash
pal lesson run core-vla-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/core-vla-01/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `vla-request-response.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check core-vla-01 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile core --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `vla-protocol` operation and computes `schema_fields`. Verification uses the lesson-specific `vla-request-response.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `lerobot`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run core-vla-01 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `ci-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `vla-request-response.json`.

## Next lesson

Next catalog item: [sim-ros-01](./sim-ros-01.md) — ROS 2 topics, QoS, services, actions, and TF
