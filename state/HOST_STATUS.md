# Cross-Host Status

This is the canonical, non-secret coordination ledger for public tutorial work
across MacBook, WS2 Windows, WS2 Ubuntu, and WS1 Ubuntu. Read it together with
`state/PROGRESS.md`: progress is authoritative for tutorial completion, while
this file records what each host has actually observed and verified.

## Shared snapshot

- Public curriculum structure: **41 implemented / 8 hardware-scaffolded**
- Learner progress and next lesson: **host-local via `pal course status/next`**
- Canonical branch: `main`
- Large/local state is not synchronized here; see `runbooks/GIT_SYNC.md`.

## Host ledger

The rows below are retained as pre-v1 installation evidence. Their T00 next-step
text is historical; current learner selection comes only from `.local/` and
`pal course next`.

| Host ID | OS / mode | Last pulled work base | Local readiness and last verification | Current work / next action | Last reported |
|---|---|---|---|---|---|
| `MACBOOK` | macOS arm64 / `DEVELOPMENT` | public base `8a7123c`; core pin `b525d62` | Profile detection kept ROS/GPU/Isaac unavailable. All 25 Core lesson-specific operations ran headlessly with one semantic artifact each; deployment bundle and runtime-offline command sink passed with zero command publishers. Public tests, Ruff, strict mypy, repository/release/boundary validators, and strict MkDocs passed. No ROS, GPU, Isaac, device, or hardware result claimed. | Adopt this public revision in the private overlay, then verify ROS/GPU/Isaac on their matching Ubuntu profiles. Keep physical lessons reader-gated. | 2026-09-11 KST |
| `WS2_WINDOWS` | Windows native / `DEVELOPMENT` | public `5ced2a3`; core `b525d62` | Isaac Sim 6.0.1 distribution, bundled Python 3.12.13 and RTX 5090 driver 616.64 verified by commands; prior compatibility PASSED and Hello World logs inspected. Scoped installer scan found none; no installation restarted. See [verification](../docs/WS2_WINDOWS_INSTALLATION_STATUS.md). | **in-progress**: installed software verified; interactive device setup incomplete. Last success: version/log audit. Next: resume hardware guide and verify connections/calibration. Blocker: user hardware tests deferred. No Ubuntu/WSL2 or tutorial completion claimed. | 2026-09-07 18:05 KST |
| `WS2_UBUNTU` | Ubuntu 24.04.5 native / `DEVELOPMENT` | public `a6b9257`; core `b525d62` | RTX 5090 driver 595.84; locked core, native Jazzy/RViz/MCAP, Docker/NVIDIA runtime, learning, LeRobot, mjlab, and Isaac Sim/Lab environments installed. Public 15 and core 8 tests passed; EGL, ROS record/replay, CUDA tensors, container GPU, and Isaac compatibility passed. See [installation status](../docs/WS2_UBUNTU_INSTALLATION_STATUS.md). | Installation verified. Keep T00 pending. User must accept the Isaac EULA before first launch/example; hardware pairing, isolated robot networking, and motion remain separate gates. | 2026-09-10 KST |
| `WS1_WINDOWS` | Windows native / `DEVELOPMENT` | public `0e49749`; core `b525d62` | Python 3.12.10 and locked public environment verified. Windows now preserves exact sample-candidate bytes, so the runtime-offline manifest checksum, deterministic vector, rollback declaration and zero command publishers pass; the isolated public suite passed all 69 tests. No ROS, Isaac, device, pairing, calibration, live-stream or hardware result claimed. | Continue curriculum completion on a supported Linux/macOS host. On Windows, keep the verified offline command sink and wait for a separately requested reader test before installing vendor device stacks or opening hardware discovery. | 2026-09-11 KST |
| `WS1_UBUNTU` | Ubuntu 24.04.5 native / offline `DEVELOPMENT` | public `7c3bd97`; core `b525d62` | Locked Python 3.12.3 / MuJoCo 3.12.0 environment refreshed; public 69 and core 8 tests passed, dependencies compatible. Deterministic pendulum repeat error 0; EGL and native Jazzy/CycloneDDS/RViz/MCAP verified. NVIDIA 595.84 retained. See [current verification](../setup/WS1_UBUNTU_VERIFICATION_2026-09-11.md). | Local branch `ws1-ubuntu/setup-20260911`. `core-00` completed with inspected artifacts in host-local progress; next eligible `core-01`. CUDA compute unverified; learning/Isaac opt-in. No hardware authority. | 2026-09-11 KST |

`Last pulled work base` is the commit checked out before the reported work. The
commit containing this file is the immutable revision of the resulting report;
do not try to place that commit's own hash inside the same commit.

## Mandatory update rule

Update only the current host's row, preserving every other host's newer report,
whenever a push will contain any of the following:

- a completed, retried, or portability-verified tutorial;
- an installed, upgraded, verified, failed, or intentionally deferred semantic
  environment such as `core-dev`, `ros2-dev`, or a GPU stack;
- a model/source fetch that changes tutorial eligibility;
- a meaningful blocker, handoff, execution-mode change, or candidate bundle;
- a change to shared progress, gates, locks, source pins, or reproducibility
  evidence.

For a tutorial result, update `state/PROGRESS.md` and this file in the same
focused commit. For an installation-only result, leave tutorial progress
unchanged and record only a non-secret readiness summary here. Machine-local
paths, hostnames, usernames, IP addresses, serial numbers, credentials, caches,
and environment contents remain under ignored `.local/` or outside Git.

## Pull, commit, and push protocol

Before work:

```bash
git status --short --branch
git pull --rebase
git log -1 --oneline
```

Then read `state/HOST_STATUS.md`, `state/PROGRESS.md`, and the selected tutorial.
If another host has newer work, continue from it rather than recreating or
overwriting it.

Before an authorized push:

```bash
git diff --check
git status --short
git add <work files> state/PROGRESS.md state/HOST_STATUS.md
git commit -m "tutorial(Txx): complete <topic>"  # adapt for setup-only work
git push
git status --short --branch
```

Do not stage `state/PROGRESS.md` when it did not change. A push containing a
tutorial or installation result without the relevant host-row update is
incomplete. Codex must still obtain explicit user authorization for a live
push; when the user has already requested completion and push, the request is
that authorization for the scoped result.

When concurrent host edits conflict, merge by host row. Never resolve a conflict
by replacing the whole ledger with one host's copy.

The current operating plan identifies WS2 Ubuntu as a **native dual-boot installation**,
confirmed by the user. Its older Ubuntu/WSL2 ledger wording above is preserved as a historical
report pending a direct host audit; it is not evidence that native Ubuntu is absent.
