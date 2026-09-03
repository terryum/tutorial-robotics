---
name: run-next-tutorial
description: Select and complete exactly one eligible tutorial from shared progress and local capabilities. Use when asked to continue or run the next lesson.
---

# Run Next Tutorial

Read `AGENTS.md`, `EXECUTION_MODEL.md`, `state/PROGRESS.md`, `tutorials/INDEX.md`, and `.local/HOST_CAPABILITIES.md` when present.

Run `pal tutorial next`, then verify prerequisites, mode, capabilities, assets, and safety gates against the tutorial file. A local mismatch must not change shared progress; record it only under `.local/` and scan for another eligible lesson.

Complete exactly one lesson: preflight, reusable code, thin entry point, tests, actual run, persistent artifacts, Korean report, and shared state update. Inspect numeric and visual artifacts before marking done. Prepare a focused commit, but push only when explicitly requested.
