# Cross-Host Status

This is the canonical, non-secret coordination ledger for public tutorial work
across MacBook, WS2 Windows, WS2 Ubuntu, and WS1 Ubuntu. Read it together with
`state/PROGRESS.md`: progress is authoritative for tutorial completion, while
this file records what each host has actually observed and verified.

## Shared snapshot

- Public tutorial progress: **0/40 done**
- Next prerequisite-eligible tutorial: **T00**
- Canonical branch: `main`
- Large/local state is not synchronized here; see `runbooks/GIT_SYNC.md`.

## Host ledger

| Host ID | OS / mode | Last pulled work base | Local readiness and last verification | Current work / next action | Last reported |
|---|---|---|---|---|---|
| `MACBOOK` | macOS 26.6.2 arm64 / `DEVELOPMENT` | public `e88c618`; private `c44686e`; core `b525d62` | Python 3.12 `.venv` present. Public doctor passed; public tests 3 passed and 12 skipped because the pinned Wuji model has not been fetched; private overlay tests 4 passed and pin preflight passed; core tests 8 passed. Host-local capability file has not been registered. | Run `$bootstrap-host`, keep T00 pending until its full acceptance contract is executed, then commit T00 evidence plus this row. | 2026-09-07 17:19 KST |
| `WS2_WINDOWS` | Windows native / `DEVELOPMENT` | public `5ced2a3`; core `b525d62` | Isaac Sim 6.0.1 distribution, bundled Python 3.12.13 and RTX 5090 driver 616.64 verified by commands; prior compatibility PASSED and Hello World logs inspected. Scoped installer scan found none; no installation restarted. See [verification](../docs/WS2_WINDOWS_INSTALLATION_STATUS.md). | **in-progress**: installed software verified; interactive device setup incomplete. Last success: version/log audit. Next: resume hardware guide and verify connections/calibration. Blocker: user hardware tests deferred. No Ubuntu/WSL2 or tutorial completion claimed. | 2026-09-07 18:05 KST |
| `WS2_UBUNTU` | Ubuntu 24.04.5 native / `DEVELOPMENT` | public `a6b9257`; core `b525d62` | RTX 5090 driver 595.84; locked core, native Jazzy/RViz/MCAP, Docker/NVIDIA runtime, learning, LeRobot, mjlab, and Isaac Sim/Lab environments installed. Public 15 and core 8 tests passed; EGL, ROS record/replay, CUDA tensors, container GPU, and Isaac compatibility passed. See [installation status](../docs/WS2_UBUNTU_INSTALLATION_STATUS.md). | Installation verified. Keep T00 pending. User must accept the Isaac EULA before first launch/example; hardware pairing, isolated robot networking, and motion remain separate gates. | 2026-09-10 KST |
| `WS1_WINDOWS` | Windows native / not audited | not reported | User confirms Windows is installed; no local device or software verification recorded. | Audit installed tools, then independently verify pairing, calibration and input streaming. | user-confirmed plan, 2026-09-08 |
| `WS1_UBUNTU` | Ubuntu 24.04.5 native / offline `DEVELOPMENT` | public `9d314bf`; core `b525d62` | Python 3.12.3, uv 0.12.10 and locked MuJoCo 3.12.0 installed. Public 3 passed/12 asset skips; core 8 passed; dependency checks passed. Deterministic pendulum/EGL, native Jazzy/CycloneDDS communication, RViz and MCAP verified. NVIDIA 595.84 retained. See [installation evidence](../setup/13_UBUNTU_OFFLINE.md). | A0–A7 common installation verified. Keep T00 pending; implement actual capability/mode selection and execute its full acceptance before changing progress. | 2026-09-08 KST |

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
