# Tutorial Robotics

An open, capability-first course for robot control, simulation, learning, and safely gated hardware integration. English is the default; the complete [한국어 과정](docs/ko/index.md) uses the same commands and code.

There is no MacBook → workstation → robot-computer sequence. Start at Stage 1 on any supported macOS or Linux host, add Stage 2 capabilities on Ubuntu/NVIDIA, and enter only the hardware tracks for robots you own.

| Path | Start here | What you need |
|---|---|---|
| Core learner | [25 Core lessons](docs/en/index.md) | Python 3.12 on macOS arm64 or Linux |
| Simulation learner | Core, then 15 Simulation lessons | Ubuntu 24.04 x86_64; ROS 2/GPU/Isaac only for matching tracks |
| Hardware learner | Core + selected Simulation prerequisites, then common safety lessons and one robot track | isolated Ubuntu runtime and explicit per-run approval |

## Two-minute quickstart

```bash
git clone https://github.com/terryum/tutorial-robotics.git
cd tutorial-robotics
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

pal host detect --json
pal setup plan --profile core --out .local/setup-plan.json --json
pal setup verify --profile core --json
pal course runnable --without-hardware --json
pal course init --through core --json
pal course next --json
pal lesson check core-00 --json
pal lesson run core-00 --headless --json
```

The run writes learner-owned evidence to `.local/runs/` and progress to `.local/progress.json`; both are ignored by Git. Setup is profile-scoped (`core`, `ros`, `gpu`, `isaac`, `runtime-offline`, or `hardware`). `pal setup apply` installs only selected Python extras into an active virtual environment. It never installs system packages, drivers, ROS, Isaac Sim, firmware, or large models.

## Curriculum

- Stage 1 — Core: 25 portable lessons covering deterministic simulation, FR3 control, Enlight and Wuji models, dexterity, RL, datasets, IL, ALOHA, and a VLA protocol.
- Stage 2 — Simulation: 15 Ubuntu lessons covering ROS 2, GPU learning, VLA, Isaac, deployment bundles, and robot-specific simulation.
- Stage 3 — Hardware: 9 isolated-runtime lessons. Run `hw-common-01/02`, then only a robot track you own. Enlight+Wuji integration requires both devices.

The machine-readable [curriculum catalog](curriculum/catalog.json) is authoritative. All 49 lessons have matching bilingual pages and thin entry points. Forty software lessons plus the offline command-sink lesson have lesson-specific implementations; the eight device-dependent lessons remain explicitly `scaffolded` until reader/hardware evidence exists. Legacy T IDs remain CLI and URL aliases throughout v1.x; see the [migration table](migration/tutorial-id-map.csv).

## Copyable agent prompts

English:

> Inspect this host with `pal host detect --json`. Show me the smallest setup plan before applying it. Start at Stage 1 and run, inspect, and explain one eligible lesson at a time. Treat unavailable capabilities honestly, and ask before system changes or any hardware motion. Never install drivers, CUDA, ROS, Isaac Sim, firmware, or large models automatically.

한국어:

> `pal host detect --json`으로 이 호스트를 검사하고, 적용 전에 가장 작은 설치 계획을 보여줘. Stage 1부터 실행 가능한 수업을 한 번에 하나씩 실행·검사·설명해줘. 없는 capability는 그대로 보고하고, 시스템 변경이나 하드웨어 motion 전에는 반드시 승인을 요청해. driver, CUDA, ROS, Isaac Sim, firmware, 대형 모델은 자동 설치하지 마.

Codex reads [AGENTS.md](AGENTS.md) and the repository skill; Claude Code reads [CLAUDE.md](CLAUDE.md) and an equivalent generated skill. `pal`, not the wrapper, owns capability, selection, execution, and safety decisions.

## Verification and release status

`ci-checked` means the dependency-light contract runs in CI. `maintainer-checked` requires recorded stack evidence. `reader_test_required` is deliberately not presented as verified hardware/GPU behavior. Publication state is separate from learner progress in [state/PUBLISHING.md](state/PUBLISHING.md).

```bash
python scripts/validate_repository.py
python scripts/validate_release.py
pytest
ruff check .
mypy src
```

The repository is Apache-2.0. Vendor sources remain pinned, read-only, on-demand dependencies. Assets without confirmed redistribution permission are represented only by source/version/license manifests and adapters.
