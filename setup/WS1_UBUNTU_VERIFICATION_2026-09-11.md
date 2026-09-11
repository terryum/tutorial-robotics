# WS1 Ubuntu verification — 2026-09-11

Native Ubuntu 24.04.5, offline DEVELOPMENT. Work uses the local
`ws1-ubuntu/setup-20260911` branch, based on public `7c3bd97` and core
`b525d62`. Other hosts' reports are preserved; only sanitized results are published.

## Installation and checks

Python 3.12.3, uv 0.12.10, MuJoCo 3.12.0 and the locked core environment are
verified. The editable public package was updated from 0.1.0 to 1.0.0.dev0.
Dependency checks passed. Public tests: **69 passed**; the pinned shared backend
suite in an environment containing that backend: **8 passed**.

The host already has native ROS 2 Jazzy desktop, CycloneDDS, RViz, MCAP and
colcon. No APT reinstall was needed. RTX 5090 driver 595.84 was retained.
EGL rendering and native ROS communication/record/replay were exercised. CUDA
framework arithmetic remains unverified because this core environment has no
torch; Isaac Sim and a separate learning environment remain opt-in.

The deterministic pendulum produced 1,000 finite states over 2 seconds. Repeat
error was 0; changing the timestep from 2 ms to 1 ms changed the angle by at most
0.0015375537058700886 rad. Three invalid inputs were rejected.
See [numeric evidence](../docs/evidence/ws1-ubuntu-20260911/pendulum-summary.json).

## Local course result

`pal course next` selected `core-00`. Its check and both runs passed with seed 7 /
64 samples and seed 8 / 96 samples. All four artifacts were inspected and the
host-audit SHA-256 was recomputed. Both runs found six capabilities in the core
shell and the same digest. This is correct for an unchanged host audit; the
English and Korean Try it paragraphs now explain that behavior.
See [run summaries](../docs/evidence/ws1-ubuntu-20260911/core-00-summary.json).

The data flow is host probes → capability evidence → host-audit.json → digest,
summary and local progress. Sourcing native Jazzy adds ROS capabilities to that
shell; an unsourced core-shell report is not evidence that ROS is uninstalled.

Only `core-00` is completed locally. The next eligible lesson is `core-01`.
Progress stays in ignored `.local/progress.json`; the shared progress pointer
is unchanged. This installation pass grants no hardware authority.

## Local evidence

Full public artifacts are under `.local/installation/ws1-ubuntu-20260911-verified/`
and `.local/runs/core-00/ws1-20260911-seed7` / `ws1-20260911-seed8`.
Only sanitized summaries are tracked. The pre-v1 September 8 report is historical.
