# Repository Instructions

## Mission

Teach robotics progressively with public robot ecosystems, reproducible code,
tests, persistent outputs, and Korean lesson reports. Use the same repository
state from MacBook to WS2 and then WS1.

## Required order

Read `MACHINE_SEQUENCE.md`, `state/PHASE_GATES.md`, `state/PROGRESS.md`,
`tutorials/INDEX.md`, the active machine runbook, and the selected tutorial.

## Public independence

- This repository must install, test, and run without any private repository.
- Do not add a dependency, import, prerequisite, or runtime lookup for
  `tutorial-robotics-private`.
- Optional plugins are discovered only when already installed; absence is
  normal and silent.
- Vendor repositories are pinned and read-only. If redistribution is not
  permitted, track only source, revision, checksum, and adapter code.

## Execution contract

Each tutorial performs preflight, implementation, an automated test or smoke
test, actual execution, persistent output, a Korean report, and state update.
Do not mark a tutorial complete based only on process exit status.

## Safety

Hardware tutorials start read-only. Motion requires model identity, safety
state, limits, acknowledgement, timeout, stale-command checks, a run card, and
explicit approval for that run. A previous approval never applies to a new run.
