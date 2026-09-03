# v4 Capability-First Audit

## User correction incorporated

- WS2 is treated as a superset of MacBook development capabilities.
- No core lesson is MacBook-only.
- MacBook and WS2 may alternate through the same Git branch and shared progress.
- Tutorial selection uses capability requirements, not machine phases.
- Local capability mismatch does not mutate global status.
- macOS/MPS/RoboStack checks are optional portability validation.
- real hardware remains isolated under `ROBOT_RUNTIME` mode.

## Files materially revised

- `EXECUTION_MODEL.md`, `README.md`, `START_HERE.md`, `AGENTS.md`
- capability-based tutorial front matter and index
- shared progress and milestone gates
- environment model and host bootstrap skills
- bidirectional Git sync and new development/runtime runbooks
- machine-specific filenames are retained as migration aliases where renaming would break links;
  front matter and selection logic are capability-first
