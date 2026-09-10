# hw-enlight-03 — Enlight contact-task shadow and gated evaluation

You will build a reproducible minimum baseline for **Enlight contact-task shadow and gated evaluation** and inspect the flow from reference state to observed state through numeric artifacts.

| Field | Value |
|---|---|
| Stage / track | `hardware` / `enlight` |
| Legacy alias | `T41B` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime`, `isolated-network`, `enlight-hardware`, `read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-01`, `sim-enlight-02` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |

This entry point only exercises an offline/read-only contract. Real motion requires a fresh run card and explicit approval.

## Learning goals

- Check capabilities and prerequisites before execution.
- Produce a seeded trace and record its SHA-256 digest.
- Keep external GPU, ROS 2, and real-hardware evidence separate in the verification badge.

## Preflight

```bash
pal host detect --json
pal setup verify --stage hardware --json
pal lesson check hw-enlight-03 --json
```

## Action

```bash
pal lesson run hw-enlight-03 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/hw-enlight-03/run.py --headless`.

## Expected

Exit code `0` creates `summary.json`, `trace.csv`, and `lesson-report.md`. `metric_value` in `summary.json` must be finite and repeatable for the same seed.

## Recovery

Run `pal lesson check hw-enlight-03 --json` first. If a capability is unavailable, follow the missing list from `pal setup verify --stage hardware --json`; do not auto-install system packages or firmware.

## How it works

The common runner samples normalized reference and observed signals every 20 ms. It computes mean absolute tracking error $E=\frac{1}{N}\sum_i |r_i-y_i|$ and uses the CSV byte-level SHA-256 as a checkpoint. This validates interface and reproducibility plumbing; it is not evidence of real robot accuracy or sensor force.

Source references: `flexiv-rdk`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

Run `pal lesson run hw-enlight-03 --headless --seed 8 --samples 96`. The digest and `changed_metric_value` should change while the artifact schema stays fixed.

## Checkpoint

`pal lesson check` validates mirrored headings, the canonical command, the entry point, and the lesson-specific test. The publication badge is `reader_test_required` and is independent of local completion.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

Next catalog item: [hw-enlight-wuji-01](./hw-enlight-wuji-01.md) — Enlight and Wuji integrated read-only validation
