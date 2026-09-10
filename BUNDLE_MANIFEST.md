# Bundle Manifest — v1 capability-first implementation

- Forty-nine lessons are indexed from `curriculum/catalog.json` and mirrored in
  `docs/en` and `docs/ko`.
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
- `docs/en/index.md` and `docs/ko/index.md`
- `runbooks/GIT_SYNC.md`
- `state/HOST_CAPABILITY_MODEL.md`
- `state/PHASE_GATES.md`

## Validation

- all tutorial IDs unique
- every prerequisite ID exists
- every local Markdown link resolves
- every lesson has a committed entrypoint, deterministic smoke test, expected
  artifacts, safety level, and verification badge
- no host-specific shared status
- `python3 scripts/check_public_boundary.py` passes
- `uv sync --frozen --no-dev` and all 25 Core lessons run without sibling
  repositories or initialized submodules
- Ruff and mypy report zero errors for the public repository
