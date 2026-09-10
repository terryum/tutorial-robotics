# sim-enlight-02 — Enlight contact-task simulation and candidate bundle

This lesson checks **Enlight contact-task simulation and candidate bundle** through the `contact-candidate` implementation and its `contact-candidate.json` artifact.

| Field | Value |
|---|---|
| Stage / track | `sim` / `enlight` |
| Legacy alias | `T41A` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-enlight-02`, `sim-deploy-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `contact-candidate.json` produced by `contact-candidate`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile gpu --json
pal lesson check sim-enlight-02 --json
```

## Action

```bash
pal lesson run sim-enlight-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-enlight-02/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `contact-candidate.json`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check sim-enlight-02 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile gpu --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `contact-candidate` operation and computes `success_ratio`. Verification uses the lesson-specific `contact-candidate.json` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `flexiv-rdk`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run sim-enlight-02 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [sim-wuji-02](./sim-wuji-02.md) — Wuji dexterity candidate bundle
