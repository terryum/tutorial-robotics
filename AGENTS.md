# Repository Instructions for Codex

## Mission

FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, ALOHA의 공개 생태계로 제어·RL·IL·VLA를 단계적으로 학습한다. 비공개 로봇과 조직별 통합 내용은 sibling private overlay에서만 다룬다.

## Authoritative documents

항상 다음을 먼저 읽는다.

1. `EXECUTION_MODEL.md` — capability-first 실행, Git continuity, runtime mode
2. `references/PUBLIC_CURRICULUM.md` — 공개 범위의 교육 기준
3. `docs/11_SOURCE_CURRICULUM_ALIGNMENT.md`
4. `.local/HOST_CAPABILITIES.md` if present
5. `state/HOST_CAPABILITY_MODEL.md`
6. `state/HOST_STATUS.md`
7. `state/PHASE_GATES.md`
8. `state/PROGRESS.md`
9. `state/CURRENT_TUTORIAL.md`
10. `tutorials/INDEX.md`
11. current mode runbook

## No mandatory MacBook → WS2 sequence

- MacBook and WS2 use the same `DEVELOPMENT` mode.
- WS2 is a superset host and may execute every portable/core lesson plus CUDA/Isaac/mjlab lessons.
- MacBook executes every lesson whose `requires` list is satisfied.
- Completing a lesson on either host marks it globally complete.
- macOS-specific compatibility checks are optional and never gate GPU work.

## Skill routing

- host audit/registration → `$bootstrap-host`
- “다음 tutorial”, “계속” → `$run-next-tutorial`
- specific ID → `$run-specific-tutorial`
- explanation/rerun/one-variable experiment → `$explain-and-visualize`
- upstream audit → `$update-upstreams`
- candidate deployment bundle → `$promote-deployment-bundle`
- real hardware/torque/motion/firmware → `$hardware-gate`

## Host identity and capabilities

Do not infer permission from the name WS1/WS2. Detect and record actual OS, architecture, GPU, ROS, display, network and hardware access in `.local/HOST_CAPABILITIES.md`. `.local/` is never committed.

Execution modes:

- `DEVELOPMENT`: simulation, code, learning, training; MacBook or WS2
- `ROBOT_RUNTIME`: isolated real-robot runtime; WS1 or isolated WS2

Changing a WS2 checkout from `DEVELOPMENT` to `ROBOT_RUNTIME` requires process, environment, NIC and command-authority audit.

## Tutorial selection

Select the first row in `tutorials/INDEX.md` satisfying all of the following.

1. shared status is `pending` or `blocked-retry`
2. prerequisites are done
3. tutorial `mode` matches current execution mode
4. every item in tutorial `requires` exists in local capabilities
5. required assets/environment can be reconstructed from committed pins
6. hardware safety gates and per-run approvals are satisfied

A local capability mismatch **must not mutate shared progress**. Do not create a host-specific shared status. Record the mismatch under `.local/` and continue scanning for another eligible tutorial. If no tutorial is eligible, list missing capabilities and the host that could supply them.

`T36` is repeatable per physical robot even if its shared tutorial row is already done.

## Teach-first, scale-second

On WS2, do not replace an educational implementation with an opaque GPU/vendor shortcut. First execute the small deterministic baseline and explain state, units, frames and data flow. Then add CUDA/vectorization/Isaac scaling as a separate configuration.

## Execution contract

Every tutorial must include:

1. capability/environment/model preflight
2. reusable module plus thin entry point
3. type hints, SI units, frame/quaternion convention
4. `--help`, `--seed`, `--output-dir`, and `--headless` when applicable
5. automated test or smoke test
6. actual execution
7. persistent output
8. Korean lesson report
9. shared state update

Process exit alone is not success; inspect numeric and visual artifacts.

## Cross-host portability

- No hard-coded home directory or absolute machine path.
- Keep platform-specific install logic outside reusable robotics code.
- Use dependency markers/lockfiles per OS and architecture.
- A done tutorial may be rerun as `local portability verification`; do not overwrite canonical evidence or change shared status.
- Machine-local readiness and paths belong only in `.local/`.

## Git continuity

Before editing:

1. inspect `git status`
2. pull/rebase the current branch when the worktree is clean
3. read `state/HOST_STATUS.md`; preserve every other host's newer row
4. do not overwrite uncommitted work
5. confirm shared progress and source pins

After one tutorial:

- prepare a focused commit containing code, tests, small artifacts, report and shared state
- update the current host's row in `state/HOST_STATUS.md` whenever a tutorial,
  installation/environment result, portability verification, blocker, handoff,
  mode change, lock, or source pin will be pushed
- for a tutorial result, commit `state/PROGRESS.md` and `state/HOST_STATUS.md`
  with the implementation and evidence; installation-only work updates host
  status without falsely changing tutorial progress
- do not auto-push unless explicitly requested
- never commit virtual environments, caches, secrets or large raw artifacts
- large checkpoints/datasets use Git LFS, DVC, NAS or object storage; commit manifest and SHA-256
- one active writer per shared branch is the default
- after an authorized push, verify the branch is clean and not ahead/behind its upstream

## Real hardware safety

Without a new explicit per-run approval, never:

- enable torque or control
- publish joint/base/Cartesian/hand motion
- execute contact or system-identification excitation
- update firmware
- increase or bypass limits
- disable watchdog, collision or E-stop paths

Order:

```text
offline replay → command sink → read-only → live shadow → torque-disabled replay → run card → one approved action
```
