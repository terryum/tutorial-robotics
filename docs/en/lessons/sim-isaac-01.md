# sim-isaac-01 — Import public robot assets into Isaac Sim

This lesson checks **Import public robot assets into Isaac Sim** through the `isaac-import` implementation and its `import-contract.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `isaac` |
| Legacy alias | `T33` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `isaac-sim` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `import-contract.json` produced by `isaac-import`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile isaac --json
pal lesson check sim-isaac-01 --json
```

## Action

```bash
pal lesson run sim-isaac-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-isaac-01/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `import-contract.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-isaac-01 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile isaac --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `isaac-import` operation and computes `joint_match_ratio`. Verification uses the lesson-specific `import-contract.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `isaac-sim-ws`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-isaac-01 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `import-contract.json`.

## Next lesson

Next catalog item: [sim-isaac-02](./sim-isaac-02.md) — Isaac camera, lighting, and synthetic data
