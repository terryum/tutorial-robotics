---
name: robotics-book-orchestrator
description: Coordinate bilingual robotics textbook creation, scoped updates and resume using project-local Harness; do not start learner lessons.
---

# robotics-book-orchestrator

Read `agent/book-contract.md`, catalog, workflow and the approved task scope. Use the project Harness runtime guide for initialization, immutable output fingerprints, communication and lifecycle. Before each run confirm earlier authors are actually idle/stopped; one book-production run at a time.

Build/update the lesson specification with `python scripts/book_spec.py`; inspect questions, objectives, prerequisite concepts, dispatch source, artifacts and catalog environment/status. Use [production contract](references/production.md) to split work. Parent owns shared contracts, README, generator, integration and completion. Workers own separate run output folders. Read role definitions; if custom role selection is unavailable supply that definition to a general native agent and record the fallback. Inherit model/effort. Parent plus at most three children; no recursive delegation.

Start with core-fr3-02, core-fr3-04, core-fr3-08, sim-fr3-04 and hw-enlight-05; review before expansion. Korean draft → technical/reader review → correction → English → bilingual review → integration → actual final-page QA. Independent Reviewer never edits product files. QA runs checks and returns fixes to authors. Default correction limit two; unresolved required defects prevent completion.

Worker artifacts become immutable at result registration. Integrate only reviewed drafts. Refresh only generator-managed blocks. Validate the actual linked book, not just draft outputs. Use Harness resume with a new run ID; lesson updates invalidate translation/summary/review consumers, shared concepts invalidate all linked consumers. Preserve prior runs.

Final checks: generator preservation/idempotence, all catalog lessons, 11 concept pairs, links and language continuity, catalog/path/release validation, strict MkDocs, changed-Python checks, credential/public boundary, rendered table/formula/image/navigation review. Native checks require two real workers and independent QA, missing-input refusal, selective resume, and `validate.py --project . --run <id> --complete`. Separate passed/failed/not_run; never replace native evidence with static validation. No runtime algorithm changes, heavy installs, hardware, learner state changes or automatic push. Honor explicit session authorization for commit/push.

For a reusable full plan, run `python scripts/book_plan.py --run-id <new-id> --output .harness/plans/<new-id>.json`. For a scoped update add `--changed-lesson <id>` or `--changed-concept <slug>`; the latter includes linked lesson consumers. Initialize with the Harness CLI and dispatch only ready packets. Each lesson task includes translation/summary; parent refreshes the catalog-managed goal summary after integration. Keep prior receipts and unrelated content unchanged. Native resume tests and scoped-plan selection tests are in `tests/test_book_harness.py`. For a failed review, create a fresh correction output/run and preserve the rejected draft instead of modifying registered artifacts.

The approved baseline covered 68 lessons; the synchronized catalog added four optional VR/collection lessons. Always derive current counts/platforms/status from the catalog. Reading order increases equipment: laptop → verified GPU → optional XR/glove/tracker/UMI collection → actual robot last. Preserve VR-free routes and Windows/Linux support distinctions. Include `docs/{en,ko}/nvidia-ecosystem.md` in relevant review; external NVIDIA exercises are not automatically verified catalog lessons.
