# Tutorial Robotics

An action-first bilingual course for readers who know basic Python and are new to robotics. Start with one lesson, inspect the actual state and images, explain the result, compare one variable, then finish it. [English](docs/en/index.md) · [한국어](docs/ko/index.md)

## First start — no Python or pal assumed

```bash
git clone https://github.com/terryum/tutorial-robotics.git
cd tutorial-robotics
sh bootstrap.sh --plan
```

The plan checks OS, architecture, Python, uv and free disk without creating learner state. It prints exactly what would be installed, why, where and which commands would run. Supported Core hosts are macOS arm64 and Linux x86_64.

After reading that plan:

```bash
sh bootstrap.sh --apply
source .venv/bin/activate
pal host detect --json
pal setup verify --profile core --json
pal course init --through core --json
pal course next --json
pal lesson run T00 --headless --output-dir .local/runs/core-00/first --json
pal lesson check T00 --run-dir .local/runs/core-00/first --json
```

Read [T00](docs/en/lessons/core-00.md) or [한국어 T00](docs/ko/lessons/core-00.md) for the explanation, one-variable comparison, review and finish steps. Stop after T00. An execution does not complete a lesson. `course init` preserves earlier completion records; use a fresh run directory for reruns.

Bootstrap reuses the Python 3.12 environment and existing lockfile. If needed, uv is installed into this checkout's .local/bin and managed Python into .local/python. It does not change system Python. ROS, GPU, learning frameworks, Isaac and large pretrained models are prepared only when their lesson needs them. System packages, drivers, firmware and physical actions retain separate approval requirements.

## Four copyable prompts

| Intent | 한국어 | English |
|---|---|---|
| First start | 처음 시작할게. bootstrap 계획을 보여주고 필요한 Core 환경을 준비한 뒤 T00 하나를 실행·검사·설명해줘. | Show the bootstrap plan, prepare the necessary Core environment, then run, inspect and explain only T00. |
| Next lesson | 다음 단계 실행해줘. | Run the next eligible lesson only. |
| Rerun | 다시 실행해줘. | Rerun the current lesson with a fresh execution record. |
| Feedback | [개선점] 여기에 개선할 내용을 적습니다. | [개선점] Describe the improvement here. |

“[개선점] 지금 바로 고쳐줘 …” stores urgent feedback, safely interrupts the software experiment, fixes/reverifies it and resumes the same lesson. Other feedback accumulates and is applied automatically after execution/explanation. Feedback received before starting another lesson belongs to the previous lesson.

Codex and Claude Code follow the same [workflow](agent/workflow.md). Both read the same local feedback queue. You can inspect it directly:

```bash
pal feedback list --json
pal feedback add "[개선점] Explain the plot units" --lesson T00 --json
```

## Evidence and course scope

The catalog retains 49 IDs and legacy aliases: 25 Core lessons, 15 Simulation lessons, one offline runtime lesson and eight device lessons. Real MuJoCo models, measured contact/control, NumPy PPO and BC replace the earlier generic numerical fixtures. ACT and the VLA mock remain explicitly contract lessons.

Mac verification covers Core plus the generated deployment candidate and offline sink. The other 14 software lessons require actual Ubuntu/ROS/GPU/Isaac environments and remain `reader_test_required` until run there. The eight device lessons remain `scaffolded`; no simulation result authorizes physical motion. See [WS1 preparation and verification](setup/WS1_HANDOFF.md).

Read the [measured verification report and reviewed figures](docs/verification/reader-experience.md) for exact results, source revision and remaining external checks.

`lesson check --run-dir` verifies artifact identity/hashes, finite numerical traces and nonblank required images. `lesson review` records a separate one-variable comparison and explanation. `lesson finish` rechecks readiness, evidence and unresolved feedback before recording completion. Short training verification never claims a solved policy.

All learner progress, feedback, datasets, checkpoints and private run details stay in ignored .local/. [state/PUBLISHING.md](state/PUBLISHING.md) holds only shared publication evidence. A separate `PAL_LOCAL_DIR` keeps developer verification independent of the user's learning state.

## Development verification

```bash
uv sync --locked --python 3.12
source .venv/bin/activate
pytest
ruff check .
mypy src
python scripts/validate_repository.py
python scripts/validate_release.py
python scripts/verify_course.py --profile core --local-dir .local/development/course
```

Fetch the public model bundles listed in T02 before full Core integration. Unit tests check state preservation, corrupt evidence rejection and unavailable capabilities; integration commands exercise real models and policies. Missing capabilities never become completed lessons.

The metadata generator preserves authored lesson bodies, entrypoints and tests. Refresh with `python scripts/generate_curriculum.py`. The course is Apache-2.0; public vendor assets retain their individual licenses and exact file hashes in [assets/model-lock.json](assets/model-lock.json). Never edit vendor checkouts.

## Complete lesson contents

<!-- pal:toc:start -->
| # | ID / alias | English | 한국어 |
|---:|---|---|---|
| 1 | core-00 / T00 | [Repository bootstrap and host audit](docs/en/lessons/core-00.md) | [저장소 시작과 호스트 점검](docs/ko/lessons/core-00.md) |
| 2 | core-01 / T01 | [Deterministic pendulum state and timestep](docs/en/lessons/core-01.md) | [결정론적 진자 상태와 시간 간격](docs/ko/lessons/core-01.md) |
| 3 | core-02 / T02 | [Pinned public robot sources](docs/en/lessons/core-02.md) | [공개 로봇 소스 고정과 자산 매니페스트](docs/ko/lessons/core-02.md) |
| 4 | core-03 / T03 | [Multi-model inspection and asset validation](docs/en/lessons/core-03.md) | [다중 모델 검사와 자산 검증](docs/ko/lessons/core-03.md) |
| 5 | core-04 / T04 | [Unified viewer and deterministic rendering](docs/en/lessons/core-04.md) | [통합 뷰어와 결정론적 렌더링](docs/ko/lessons/core-04.md) |
| 6 | core-fr3-01 / T05 | [FR3 model anatomy](docs/en/lessons/core-fr3-01.md) | [FR3 모델 구조](docs/ko/lessons/core-fr3-01.md) |
| 7 | core-fr3-02 / T06 | [FR3 joint-space PD control](docs/en/lessons/core-fr3-02.md) | [FR3 관절 공간 PD 제어](docs/ko/lessons/core-fr3-02.md) |
| 8 | core-fr3-03 / T07 | [FR3 gravity compensation and feedforward](docs/en/lessons/core-fr3-03.md) | [FR3 중력 보상과 피드포워드](docs/ko/lessons/core-fr3-03.md) |
| 9 | core-fr3-04 / T08 | [FR3 kinematics, Jacobian, and inverse kinematics](docs/en/lessons/core-fr3-04.md) | [FR3 기구학, 자코비안과 역기구학](docs/ko/lessons/core-fr3-04.md) |
| 10 | core-fr3-05 / T09 | [FR3 operational-space control](docs/en/lessons/core-fr3-05.md) | [FR3 작업 공간 제어](docs/ko/lessons/core-fr3-05.md) |
| 11 | core-fr3-06 / T10 | [FR3 contact and friction laboratory](docs/en/lessons/core-fr3-06.md) | [FR3 접촉과 마찰 실험실](docs/ko/lessons/core-fr3-06.md) |
| 12 | core-rl-01 / T23 | [Minimal continuous-action PPO](docs/en/lessons/core-rl-01.md) | [최소 연속 행동 PPO](docs/ko/lessons/core-rl-01.md) |
| 13 | core-fr3-07 / T22 | [FR3 reach environment without ROS](docs/en/lessons/core-fr3-07.md) | [ROS 없는 FR3 도달 환경](docs/ko/lessons/core-fr3-07.md) |
| 14 | core-fr3-08 / T24 | [PPO on FR3 reach](docs/en/lessons/core-fr3-08.md) | [FR3 도달 과제 PPO](docs/ko/lessons/core-fr3-08.md) |
| 15 | core-enlight-01 / T08A | [Enlight description, frames, and kinematics](docs/en/lessons/core-enlight-01.md) | [Enlight 모델, 좌표계와 기구학](docs/ko/lessons/core-enlight-01.md) |
| 16 | core-enlight-02 / T10A | [Enlight MuJoCo draft and cross-format validation](docs/en/lessons/core-enlight-02.md) | [Enlight MuJoCo 초안과 형식 간 검증](docs/ko/lessons/core-enlight-02.md) |
| 17 | core-wuji-01 / T14 | [Wuji Hand 2 Beta 2 joints, poses, and synergies](docs/en/lessons/core-wuji-01.md) | [Wuji Hand 2 Beta 2 관절, 자세와 시너지](docs/ko/lessons/core-wuji-01.md) |
| 18 | core-wuji-02 / T15 | [Wuji virtual tactile observation](docs/en/lessons/core-wuji-02.md) | [Wuji 가상 촉각 관측](docs/ko/lessons/core-wuji-02.md) |
| 19 | core-dexterity-01 / T16 | [Wuji and Sharpa model comparison](docs/en/lessons/core-dexterity-01.md) | [Wuji와 Sharpa 모델 비교](docs/ko/lessons/core-dexterity-01.md) |
| 20 | core-data-01 / T28 | [Episode dataset from MuJoCo](docs/en/lessons/core-data-01.md) | [MuJoCo 에피소드 데이터셋](docs/ko/lessons/core-data-01.md) |
| 21 | core-dexterity-02 / T16A | [Hand retargeting and demonstration recording](docs/en/lessons/core-dexterity-02.md) | [손 리타게팅과 시연 기록](docs/ko/lessons/core-dexterity-02.md) |
| 22 | core-g1-01 / T25 | [Unitree G1 playback and motion data](docs/en/lessons/core-g1-01.md) | [Unitree G1 재생과 모션 데이터](docs/ko/lessons/core-g1-01.md) |
| 23 | core-il-01 / T29 | [Behavioral cloning baseline](docs/en/lessons/core-il-01.md) | [행동 복제 기준선](docs/ko/lessons/core-il-01.md) |
| 24 | core-aloha-01 / T30 | [ALOHA simulation and ACT contract](docs/en/lessons/core-aloha-01.md) | [ALOHA 시뮬레이션과 ACT 계약](docs/ko/lessons/core-aloha-01.md) |
| 25 | core-vla-01 / T32A | [VLA protocol and mock policy client](docs/en/lessons/core-vla-01.md) | [VLA 프로토콜과 모의 정책 클라이언트](docs/ko/lessons/core-vla-01.md) |
| 26 | sim-ros-01 / T17 | [ROS 2 topics, QoS, services, actions, and TF](docs/en/lessons/sim-ros-01.md) | [ROS 2 토픽, QoS, 서비스, 액션과 TF](docs/ko/lessons/sim-ros-01.md) |
| 27 | sim-ros-02 / T19 | [MuJoCo to ROS 2 bridge](docs/en/lessons/sim-ros-02.md) | [MuJoCo–ROS 2 브리지](docs/ko/lessons/sim-ros-02.md) |
| 28 | sim-ros-03 / T20 | [Rosbag episode recording and deterministic replay](docs/en/lessons/sim-ros-03.md) | [rosbag 에피소드 기록과 결정론적 재생](docs/ko/lessons/sim-ros-03.md) |
| 29 | sim-ros-04 / T21 | [Common embodiment API for simulation and ROS 2](docs/en/lessons/sim-ros-04.md) | [시뮬레이션과 ROS 2 공통 embodiment API](docs/ko/lessons/sim-ros-04.md) |
| 30 | sim-g1-01 / T26 | [Unitree G1 GPU PPO and motion imitation](docs/en/lessons/sim-g1-01.md) | [Unitree G1 GPU PPO와 모션 모방](docs/ko/lessons/sim-g1-01.md) |
| 31 | sim-wuji-01 / T27 | [Wuji in-hand PPO on GPU](docs/en/lessons/sim-wuji-01.md) | [Wuji GPU 손안 조작 PPO](docs/ko/lessons/sim-wuji-01.md) |
| 32 | sim-vla-01 / T32C | [SmolVLA fine-tuning and policy server](docs/en/lessons/sim-vla-01.md) | [SmolVLA 미세조정과 정책 서버](docs/ko/lessons/sim-vla-01.md) |
| 33 | sim-vla-02 / T32D | [Optional remote VLA inference](docs/en/lessons/sim-vla-02.md) | [선택형 원격 VLA 추론](docs/ko/lessons/sim-vla-02.md) |
| 34 | sim-isaac-01 / T33 | [Import public robot assets into Isaac Sim](docs/en/lessons/sim-isaac-01.md) | [Isaac Sim 공개 로봇 자산 가져오기](docs/ko/lessons/sim-isaac-01.md) |
| 35 | sim-isaac-02 / T34 | [Isaac camera, lighting, and synthetic data](docs/en/lessons/sim-isaac-02.md) | [Isaac 카메라, 조명과 합성 데이터](docs/ko/lessons/sim-isaac-02.md) |
| 36 | sim-cross-01 / T35 | [MuJoCo to Isaac sim-to-sim validation](docs/en/lessons/sim-cross-01.md) | [MuJoCo–Isaac sim-to-sim 검증](docs/ko/lessons/sim-cross-01.md) |
| 37 | sim-deploy-01 / T35A | [Candidate deployment bundle and promotion gate](docs/en/lessons/sim-deploy-01.md) | [후보 배포 번들과 승격 게이트](docs/ko/lessons/sim-deploy-01.md) |
| 38 | sim-enlight-01 / T18 | [Enlight ROS 2 fake hardware](docs/en/lessons/sim-enlight-01.md) | [Enlight ROS 2 가상 하드웨어](docs/ko/lessons/sim-enlight-01.md) |
| 39 | sim-enlight-02 / T41A | [Enlight contact-task simulation and candidate bundle](docs/en/lessons/sim-enlight-02.md) | [Enlight 접촉 과제 시뮬레이션과 후보 번들](docs/ko/lessons/sim-enlight-02.md) |
| 40 | sim-wuji-02 / T42A | [Wuji dexterity candidate bundle](docs/en/lessons/sim-wuji-02.md) | [Wuji 정교 조작 후보 번들](docs/ko/lessons/sim-wuji-02.md) |
| 41 | hw-common-01 / T35B | [Runtime bootstrap, offline replay, and command sink](docs/en/lessons/hw-common-01.md) | [런타임 시작, 오프라인 재생과 명령 차단](docs/ko/lessons/hw-common-01.md) |
| 42 | hw-common-02 / T36 | [Real-hardware read-only integration gate](docs/en/lessons/hw-common-02.md) | [실물 하드웨어 읽기 전용 통합 게이트](docs/ko/lessons/hw-common-02.md) |
| 43 | hw-fr3-01 /  | [FR3 read-only state, shadow, and approved low-risk motion](docs/en/lessons/hw-fr3-01.md) | [FR3 읽기 전용 상태, 섀도와 승인된 저위험 동작](docs/ko/lessons/hw-fr3-01.md) |
| 44 | hw-wuji-01 / T38 | [Wuji Beta 2 read-only adapter and tactile calibration](docs/en/lessons/hw-wuji-01.md) | [Wuji Beta 2 읽기 전용 어댑터와 촉각 보정](docs/ko/lessons/hw-wuji-01.md) |
| 45 | hw-wuji-02 / T42B | [Wuji shadow and gated real evaluation](docs/en/lessons/hw-wuji-02.md) | [Wuji 섀도와 승인 기반 실물 평가](docs/ko/lessons/hw-wuji-02.md) |
| 46 | hw-enlight-01 / T37 | [Enlight read-only adapter and low-risk validation](docs/en/lessons/hw-enlight-01.md) | [Enlight 읽기 전용 어댑터와 저위험 검증](docs/ko/lessons/hw-enlight-01.md) |
| 47 | hw-enlight-02 / T37A | [Enlight system identification and MuJoCo calibration](docs/en/lessons/hw-enlight-02.md) | [Enlight 시스템 식별과 MuJoCo 보정](docs/ko/lessons/hw-enlight-02.md) |
| 48 | hw-enlight-03 / T41B | [Enlight contact-task shadow and gated evaluation](docs/en/lessons/hw-enlight-03.md) | [Enlight 접촉 과제 섀도와 승인 기반 평가](docs/ko/lessons/hw-enlight-03.md) |
| 49 | hw-enlight-wuji-01 / T38A | [Enlight and Wuji integrated read-only validation](docs/en/lessons/hw-enlight-wuji-01.md) | [Enlight와 Wuji 통합 읽기 전용 검증](docs/ko/lessons/hw-enlight-wuji-01.md) |
<!-- pal:toc:end -->
