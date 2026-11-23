# Bilingual book production verification — 2026-11-23

The approved baseline covered 68 lessons. Synchronizing to public runtime source
`018bbb7a55acf612d56dd1f2b443d5aebfe823c8` preserved four newly added optional
VR/collection lessons, so the final book covers **72 lesson pairs and 11 concept
pairs**. The catalog has 33 Core, 27 Sim and 12 Hardware lessons. No robot-runtime
algorithm, model pin, learner history or hardware authority was changed by this
book work.

## Connected reader experience

English [README](../../README.md) is the default repository entrance; its language
choice leads directly to [README.ko.md](../../README.ko.md). Both lead to the
corresponding learning map, paths, equipment guide, all-lesson goal summaries and
concept chapters. Every lesson preserves its H2 contract and adds source-grounded
explanations, units/frames/shapes, calculations, artifact interpretation,
controlled prediction and comprehension answers.

Reading stages progress from laptop concepts/experiments to GPU simulation,
optional human-data equipment and actual robots last. The bilingual NVIDIA
workbook connects Isaac Sim, Lab, Teleop/Capture, GR00T and deployment exercises.
External official exercises are identified separately from implemented catalog
lessons and local acceptance. Windows/Linux, synthetic/live input, optimizer
execution, independent policy performance and physical readiness remain distinct.

## Production and independent review

Two native workers produced disjoint immutable draft outputs; a separate native
reviewer inspected all 72 bilingual lesson pairs, all 11 concept pairs and the
README-linked guides/tooling. Review used the five reader questions in the book
review skill; it was agent reader-perspective review, not a human learning study.
The runtime exposed general agents, so installed role definitions were supplied
explicitly. Models/effort were inherited; no user-wide settings changed.

The first integrated QA found 11 omitted canonical command strings in scaffold
documentation. The original author added blocked inline explanations without
runnable examples; all 22 affected language files were independently re-reviewed.
A fresh correction run reused four accepted tasks and invalidated only lessons-B,
review and QA. Prior drafts and failed QA evidence remain local and preserved.
A sandbox CoreGraphics failure passed when rerun with required macOS graphics
access, without renderer changes.

## Checks actually performed

| Check | Result | Evidence |
|---|---|---|
| Full test suite | `passed` | 230 passed; 2 optional skips; 8 subtests |
| Post-guard teleop tests | `passed` | 19 passed; missing-source skip and corruption propagation independently checked |
| Generator / scoped Harness tests | `passed` | Authored-body preservation, byte idempotence, objective summaries, missing-input refusal, selective resume |
| Ruff / mypy | `passed` | All checks passed; 77 source files checked by mypy |
| Repository / release / public boundary | `passed` | 72 catalog lessons and bilingual contracts, sources, links and boundaries |
| Strict MkDocs / built-site language checks | `passed` | All paired page identities and both README entrance choices |
| Harness import / skill structure | `passed` | 25 pinned hashes; 5 roles, 12 skills |
| Native Harness completion | `passed` | validate.py --project . --run book-v3 --complete: 0 completion errors |
| Credential guard | `passed` | 777 indexed files scanned before final prose/report; required pre-commit rescans staged bytes |
| GPU / live input / physical acceptance | `not_run` | Existing verification scope retained; no new claims |

The full test suite passed 230 tests with 2 optional skips and 8 subtests. A later
test-only guard for absent pinned Flexiv source was reviewed and the affected
teleop test file rerun. The guard skips only missing files, not hash corruption;
missing optional source is explicitly not executed. This repairs a pre-existing
fresh-cache CI failure without installing models or weakening runtime gates.
CI results for the publication commit are checked separately after push.

Native worker execution and independent review/QA are separate from static Harness
validation. Missing-input dispatch refusal and selective resume were tested with
explicitly synthetic ledger fixtures; the actual correction also demonstrated
selective task reuse. The generated full 167-task production graph was initialized
as a structure-only fixture, not reported as a fully executed native run.
Final local completion used `validate.py --project . --run book-v3 --complete`.
Run outputs and correlated communications stay in ignored local directories.

## Rendering and licensing

Native inspection of built EN/KO representative pages confirmed readable equations,
numeric tables, the historical PD plot and compact navigation. A native EN→한국어
click reached the same lesson. This exposed and fixed raw-HTML language links that
MkDocs did not rewrite; automated built-site checks cover every paired page.
GitHub source links remain branch-relative in Markdown and are converted only for
site rendering.

The project-local Codex Harness import is pinned to
`80f8217b5b6d3f220a31f05f9c0adaf09dac40f4`. All 25 imported skill/role/license/NOTICE
hashes match the pinned material. Full Apache-2.0 text, original attribution and
NOTICE accompany redistribution; both READMEs introduce the use. See
[provenance](../../third_party/codex-harness/PROVENANCE.md) and its manifest.

## Remaining external evidence

GPU/Isaac/Lab/GR00T task performance, live Quest/MANUS/VIVE input, UMI collection
and real robots were **not_run** during book production. Local checks include
synthetic CPU/MuJoCo tests and standalone arithmetic examples. Existing catalog
verification badges and scaffolded states remain unchanged. Simulator agreement,
model import, policy loss or documentation completion supplies no physical action
approval.
