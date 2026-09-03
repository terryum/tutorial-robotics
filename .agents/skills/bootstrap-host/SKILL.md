---
name: bootstrap-host
description: Audit a tutorial host, check or provision one explicitly requested environment role, and preserve tutorial progress. Use for Mac, WSL2, or Ubuntu readiness checks before T00.
---

# Bootstrap Host

Read `EXECUTION_MODEL.md`, `setup/00_HOST_AUDIT.md`, `setup/01_REPO_BOOTSTRAP.md`, and the relevant host runbook.

1. Start with read-only OS, architecture, disk, compiler, Python, Git, display, GPU, ROS, and package-manager checks.
2. Distinguish `supported` from `installed` and `verified`.
3. If the user requests readiness-only, do not create `.local/`, tutorial outputs, reports, or shared state. Never mark T00 done.
4. Otherwise, write only machine-local facts under `.local/`; never commit them.
5. Install only the named semantic environment role. Do not install ROS, CUDA, Isaac, LeRobot, drivers, or vendor SDKs implicitly.
6. Never change system Python. Prefer repository lockfiles and sibling repository paths.
7. Report exact verification commands, deferred capabilities, and whether T00 remains pending.

On Windows, treat native Windows setup and WSL2 Ubuntu setup as separate approval steps. Keep repositories in the Linux home directory, not `/mnt/c`.
