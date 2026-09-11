---
name: tutorial-robotics
description: Run the public capability-first Tutorial Robotics curriculum safely.
---

# Tutorial Robotics common learner workflow

Read curriculum/catalog.json, this workflow, the selected bilingual lesson, and local state in that order. The catalog order and pal are authoritative for both Codex and Claude Code.

1. Before Python or pal is available, run `sh bootstrap.sh --plan`. Show OS, architecture, free disk, missing tools, installation purpose, location and commands. For a readiness-only request do not apply or write state.
2. On an authorized setup request, apply only the smallest shown Core plan with `sh bootstrap.sh --apply`. Reuse the local environment and lockfile. Never automatically install system packages, drivers, CUDA, ROS distributions, Isaac Sim, firmware or large models.
3. After activation, use `pal host detect --json` and `pal setup verify --profile core --json`. These checks are read-only. `pal course init` preserves completed records.
4. Read `.local/session.json`, `.local/progress.json` and `pal feedback list --json` to resume. `PAL_LOCAL_DIR` can select an independent ignored development session; never mix its results into learner progress.
5. For “다음 단계 실행해줘” / “next”, select exactly one eligible lesson with `pal course next --json`. For “다시 실행해줘” / “rerun”, use the current session lesson and a fresh run directory, preserving earlier evidence.
6. Read the lesson goals and preflight. Check platform, imported dependencies, pinned model identity/hashes, prerequisites and implementation status. Missing capability means capability-unavailable, never success. A publication badge is independent of local evidence.
7. Run the baseline. `pal lesson run` records execution, not completion. Inspect the actual JSON/CSV/NPZ values and plots/renderings, then run `pal lesson check ID --run-dir PATH --json`.
8. Explain the measured values, axes, units, data flow and equation to a reader with basic Python. Execute the documented one-variable comparison; explain invariance honestly when applicable.
9. Immediately persist every “[개선점] …” using `pal feedback add 'original text' --lesson ID --json`. Preserve original text, lesson, receipt time, urgency and status. Feedback after completion but before another lesson starts belongs to the previous session lesson.
10. For “[개선점] 지금 바로 고쳐줘”, store it with `--urgent`, safely interrupt the current software experiment, preserve its interrupted run, fix and reverify, then resume the same lesson in a fresh run. Never interrupt or command physical hardware through an improvised path.
11. After execution/explanation, collect all pending feedback automatically. Batch compatible fixes. Rerun affected experiments for behavior changes; verify bilingual meaning, instructions and links for document changes. Resolve each item with `pal feedback resolve ID --evidence 'specific change and verification'`. Do not hide unresolved issues as completion.
12. Record the concrete explanation and comparison using `pal lesson review ID --run-dir BASELINE --comparison-run-dir COMPARISON --notes 'observations and interpretation'`. Then use `pal lesson finish ID --run-dir BASELINE --json`. Finish rechecks readiness, artifacts, code identity, review and unresolved feedback.
13. Stop after this one learner lesson. A broader explicit development/batch request may run more lessons in an isolated development state.
14. Physical lessons remain scaffolded / reader_test_required until device evidence exists. Read docs/07_SAFETY.md. Follow offline replay → sink → read-only → shadow → torque-disabled replay → fresh run card → one explicitly approved action. Each real command requires new per-run approval.
15. Learner state, runs, checkpoints, raw data and device details stay under ignored .local/. state/PUBLISHING.md holds shared publication evidence only. Do not automatically commit learner progress or push. Development commits follow the user's explicit development scope.
