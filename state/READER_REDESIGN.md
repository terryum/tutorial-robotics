# GitHub reader redesign — 2026-09-11

This is development verification, not learner completion. The original improvement guide remains at [the dated guide](../docs/TUTORIAL_IMPROVEMENT_GUIDE_2026-09-11.md). No push or hardware operation was performed.

## Implemented

- All 49 lesson IDs and aliases retained; all 98 English/Korean lesson bodies updated in place, preserving generated metadata/navigation boundaries.
- [Reader guide](../docs/en/READER_GUIDE.md) and [한국어 안내](../docs/ko/READER_GUIDE.md): first installation, new terminal, resume, capability checks, result opening, camera/replay and question-to-fix evidence.
- GitHub LaTeX blocks with units, assumptions, numerical examples and implementation connections; optional extensions. MkDocs retains mathematical rendering through arithmatex/MathJax.
- `lesson inspect`, `lesson compare`, `lesson view`, named `--param` inputs; PD gain-only and coupled damping experiments distinguished. Exact pre-step torque records and saved model/state replay; camera experiments retain their azimuth during replay.
- Schema 3 evidence fingerprints use selected implementation branches, reachable helpers, relevant model pins, runtime dependency locks and consumed input receipts. Documentation/unrelated literal lesson branches do not invalidate completion. Unknown branches/shared modules are conservatively dependencies. Legacy evidence is preserved under its original verification rules.
- Provider execution options/validation and feedback integration; installation/source audits do not fabricate numerical comparisons.
- Measured figures for all 27 portable lessons; generic optional ALOHA ACT backend and version-dispatched Isaac 5.1/6.0 import adapter. External engine implementation is distinct from host execution verification.

## Executed on macOS arm64

| Check | Result |
|---|---|
| Public pytest | 93 passed |
| Ruff / strict mypy | Passed |
| Core + portable deployment/offline | 25 + 2 lessons, separate developer progress |
| Repository / release / public boundary | Passed |
| MkDocs strict | Passed |
| Figures | Measured PNGs exported only after evidence validation; plot contact sheet and model frames inspected |

Reproduce from the repository root after bootstrap and pinned model preparation:

```bash
.venv/bin/pytest
```

```bash
bash scripts/verify_reader.sh
```

```bash
.venv/bin/python scripts/export_reader_examples.py
```

The batch is sequential, reuses still-valid evidence and writes new run directories when dependencies change. Its manifest is `.local/reader-redesign/course/verification.json`; full log is `.local/reader-redesign/core-verification.log`. User `.local/progress.json` is unchanged. Developer review notes never substitute for the reader explaining observations.

The exact PD CLI sequence (`inspect`, `compare`, offscreen `view`) passed. At 64 samples, kp 120 → 180 with kd held at 21.9089023 changed final whole-arm error from 0.3376263 to 0.2124105 rad. This is one simulated configuration, not a general gain recommendation.

## Remaining host and reader verification

On prepared external hosts, run `scripts/verify_course.py --profile ros`, `--profile gpu` or `--profile isaac` with a dedicated `--local-dir`. Read the matching lesson for its expected artifacts and installation contract. ROS, CUDA and Isaac execution was unavailable on this Mac; no external success badge was added. Device lessons retain their gates.

GitHub rendering was not visually verified: the in-app browser reported no available browser instance. Strict MkDocs build and Markdown/link checks passed, but these do not prove the browser's GitHub MathJax, Mermaid or table rendering. A reader must still open the bilingual pages on GitHub and complete the observation/explanation workflow.

The common software paths are implemented and locally verified to the extent above. The full multi-host and learner acceptance criteria remain open; short training is never policy-performance evidence.
