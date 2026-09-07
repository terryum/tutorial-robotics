---
name: run-specific-tutorial
description: Run or verify one explicitly named tutorial ID while enforcing prerequisites, capability checks, evidence, and shared-state rules.
---

# Run Specific Tutorial

Locate the ID with `pal tutorial list`. Read `state/HOST_STATUS.md`, its front
matter, and all prerequisites before changing files.

If prerequisites or capabilities are absent, explain the exact gap and do not mark the lesson complete. If it is already done, treat a rerun as local portability verification and do not overwrite canonical evidence.

For an eligible lesson, follow its preflight, implementation, test, execution,
artifact, report, and state-update contract. Update the current host row in
`state/HOST_STATUS.md` and commit it with `state/PROGRESS.md` and the lesson
evidence. Stop after that one ID unless the user explicitly requested more.
