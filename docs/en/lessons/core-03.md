# core-03 — Multi-model inspection and asset validation

You will build a reproducible minimum baseline for **Multi-model inspection and asset validation** and inspect the flow from reference state to observed state through numeric artifacts.

| Field | Value |
|---|---|
| Stage / track | `core` / `common` |
| Legacy alias | `T03` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `macos-arm64`, `linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `core-01`, `core-02` |
| Safety | `simulation` |
| Verification | `ci-checked` |

This lesson never emits a hardware command.

## Learning goals

- Check capabilities and prerequisites before execution.
- Produce a seeded trace and record its SHA-256 digest.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --stage core --json
pal lesson check core-03 --json
```

## Action

```bash
pal lesson run core-03 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/core-03/run.py --headless`.

## Expected

Exit code `0` creates `summary.json`, `trace.csv`, and `lesson-report.md`. `metric_value` in `summary.json` must be finite and repeatable for the same seed.

## Recovery

Run `pal lesson check core-03 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --stage core --json`; do not auto-install system packages or firmware.

## How it works

The common runner samples normalized reference and observed signals every 20 ms. It computes mean absolute tracking error $E=\frac{1}{N}\sum_i |r_i-y_i|$ and uses the CSV byte-level SHA-256 as a checkpoint. This validates interface and reproducibility plumbing; it is not evidence of real robot accuracy or sensor force.

Source references: `sources-manifest`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run core-03 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `ci-checked` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [core-04](./core-04.md) — Unified viewer and deterministic rendering
