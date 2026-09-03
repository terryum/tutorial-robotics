# Bundle Manifest — v4 Capability-First

- Tutorial specifications are indexed from `tutorials/*/*.md`.
- Python runtime, tests, lockfiles, ROS examples, and public vendor pins are preserved.
- Private robot specifications are excluded and live only in the sibling private overlay.
- Execution model: capability-first, bidirectional Git sync
- Required development machine sequence: none

## Key entry points

- `README.md`
- `START_HERE.md`
- `EXECUTION_MODEL.md`
- `AGENTS.md`
- `COMMANDS.md`
- `tutorials/INDEX.md`
- `runbooks/GIT_SYNC.md`
- `state/HOST_CAPABILITY_MODEL.md`
- `state/PHASE_GATES.md`

## Validation

- all tutorial IDs unique
- every prerequisite ID exists
- every local Markdown link resolves
- every tutorial has mode and requires front matter
- no host-specific shared status
- `python3 scripts/check_public_boundary.py` passes
- `uv sync --group dev --frozen` and the core public tests pass without vendor submodules
