# hw-wuji-02 — Wuji shadow and gated real evaluation

This lesson checks **Wuji shadow and gated real evaluation** through the `reader-hardware-gate` implementation and its `no run artifact until the gate is implemented` artifact.

| Field | Value |
|---|---|
| Stage / track | `hardware` / `wuji` |
| Legacy alias | `T42B` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime`, `isolated-network`, `wuji-hardware`, `read-only-preflight-wuji` |
| Prerequisites | `hw-wuji-01`, `sim-wuji-02` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |

This entry point only exercises an offline/read-only contract. Real motion requires a fresh run card and explicit approval.

## Learning goals

- Check capabilities and prerequisites before execution.
- Inspect the `no run artifact until the gate is implemented` produced by `reader-hardware-gate`.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --profile hardware --json
pal lesson check hw-wuji-02 --json
```

## Action

```bash
pal lesson run hw-wuji-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/hw-wuji-02/run.py --headless`.

## Expected

An `implemented` lesson exits `0` and creates `no run artifact until the gate is implemented`, `summary.json`, `trace.csv`, and `lesson-report.md`. A scaffolded lesson exits `2` with `reader_test_required` and does not create a run artifact.

## Recovery

Run `pal lesson check hw-wuji-02 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --profile hardware --json`; do not auto-install system packages or firmware.

## How it works

The runner dispatches this catalog ID to the unique `reader-hardware-gate` operation and computes `not applicable`. Verification uses the lesson-specific `no run artifact until the gate is implemented` schema and SHA-256, not a generic process-success signal. Lessons needing an external runtime cannot complete without its live host probe.

Source references: `wuji-control-guide`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run hw-wuji-02 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [hw-enlight-01](./hw-enlight-01.md) — Enlight read-only adapter and low-risk validation
