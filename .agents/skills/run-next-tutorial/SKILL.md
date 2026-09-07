---
name: run-next-tutorial
description: Select and complete exactly one eligible tutorial from shared progress and local capabilities. Use when asked to continue or run the next lesson.
---

# Run Next Tutorial

Read `AGENTS.md`, `EXECUTION_MODEL.md`, `state/HOST_STATUS.md`,
`state/PROGRESS.md`, `tutorials/INDEX.md`, and
`.local/HOST_CAPABILITIES.md` when present.

Run `pal tutorial next`, then verify prerequisites, mode, capabilities, assets, and safety gates against the tutorial file. A local mismatch must not change shared progress; record it only under `.local/` and scan for another eligible lesson.

Complete exactly one lesson: preflight, reusable code, thin entry point, tests,
actual run, persistent artifacts, Korean report, shared progress, and the current
host row in `state/HOST_STATUS.md`. Inspect numeric and visual artifacts before
marking done. Commit the lesson evidence and both state updates together. Push
only when explicitly requested; a request that already says to complete and
push authorizes that scoped push.
