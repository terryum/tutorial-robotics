# Physical AI Tutorial Codex v4 — Capability-First

> 기준일: 2026-09-03
> 공개 학습 기준: [`references/PUBLIC_CURRICULUM.md`](references/PUBLIC_CURRICULUM.md)
> 실행 원칙: **MacBook과 WS2를 자유롭게 오가며, 현재 capability로 실행 가능한 다음 tutorial을 Git 상태에서 이어서 수행**

이 저장소는 Codex가 Physical AI 튜토리얼 코드를 한 단계씩 생성하고 실제로 실행·테스트·시각화·설명·기록하게 만드는 Markdown 기반 운영 체계다.

## 1. 이번 v4의 핵심 변경

기존 v3의 `MacBook foundation → WS2 GPU phase`라는 machine gate를 제거했다.

```text
MacBook = portable development subset
WS2     = portable subset + Linux/CUDA/Isaac/mjlab full stack
```

따라서 다음이 모두 가능하다.

- 처음부터 WS2에서 T00을 시작해 core와 GPU 튜토리얼을 연속 수행
- WS2에서 하던 작업을 GitHub에 push하고 MacBook에서 가능한 다음 튜토리얼 수행
- MacBook 작업을 다시 push한 뒤 WS2에서 GPU-only branch를 이어서 수행
- 완료된 tutorial을 다른 host에서 local portability verification으로 재실행

장비가 아니라 tutorial front matter의 `requires` capability가 실행 가능 여부를 결정한다. 자세한 규칙은 [`EXECUTION_MODEL.md`](EXECUTION_MODEL.md)다.

## 2. 로봇 포트폴리오

### 공개 학습 기준 모델

- **Franka Research 3 v2** — 7축 제어·IK·임피던스·RL/IL
- **Unitree G1 29-DoF** — humanoid PPO·motion imitation
- **Sharpa Wave** — dexterous/tactile 비교
- **ALOHA** — ACT·양팔 IL·VLA data pipeline

`Unitree H2 Plus`는 watchlist다.

## 3. 권장 tutorial 흐름

학습 내용은 prerequisite DAG를 따른다. 같은 단계라도 어느 host에서 실행할지는 고정하지 않는다.

```text
T00–T10                 bootstrap, MuJoCo, FR3 model/control
T14–T17, T19–T21        public hands, ROS 2, bridge, common API
T22–T30                 Gym/PPO, humanoid learning, datasets, BC/ACT
T32A, T32C–T35A         VLA protocol, GPU scaling, Isaac, sim-to-sim
T35B–T36, T38, T42A/B   isolated public-robot runtime and capstones
```

WS2는 위 개발 tutorial 전체를 수행할 수 있다. MacBook은 capability가 맞는 항목을 수행한다.

## 4. 처음 사용하는 명령

### WS2에서 처음부터 시작

```text
이 컴퓨터는 WS2이며 DEVELOPMENT mode로 사용한다. EXECUTION_MODEL.md, AGENTS.md, references/PUBLIC_CURRICULUM.md, runbooks/FULL_GPU_DEVELOPMENT.md를 읽고 $bootstrap-host로 실제 capability를 등록해줘. WS2를 MacBook 이후 단계로 제한하지 말고 T00부터 현재 capability로 실행 가능한 tutorial 전체의 superset host로 취급해. 우선 T00 하나만 코드·테스트·실행·시각화·한국어 report·state 갱신까지 완료하고 멈춰줘.
```

### MacBook에서 시작 또는 이어서 진행

```text
이 컴퓨터는 MacBook이며 DEVELOPMENT mode로 사용한다. Git 상태를 확인하고 $bootstrap-host로 실제 capability를 등록해줘. shared progress를 그대로 이어받고, CUDA/Isaac/Ubuntu-vendor 전용 tutorial의 status는 바꾸지 말며 현재 MacBook에서 실행 가능한 다음 eligible tutorial 하나만 완료한 뒤 멈춰줘.
```

### 어느 개발 host에서든 반복

```text
현재 host capability와 shared progress를 검사해 실행 가능한 다음 eligible tutorial 하나만 수행해줘. 완료 후 코드·test·output·한국어 report·state를 갱신하고 정확한 Git commit 후보와 다음 후보를 보고한 뒤 멈춰줘.
```

명령 모음은 [`COMMANDS.md`](COMMANDS.md)에 있다.

## 5. Git 동기화

코드, Markdown, config, test, lockfile, small output, manifest와 progress를 Git으로 공유한다. 다음은 Git에 넣지 않는다.

- `.venv`, Pixi/Conda environment
- CUDA/Isaac cache
- `.local/HOST_CAPABILITIES.md`
- 큰 checkpoint/raw dataset/video

큰 artifact는 Git LFS, DVC, NAS 또는 object storage에 두고 hash/manifest를 Git에 기록한다. 자세한 절차는 [`runbooks/GIT_SYNC.md`](runbooks/GIT_SYNC.md)다.

## 6. 완료 정의

- reusable code와 thin tutorial entry point
- automated test/smoke test
- 실제 실행 로그
- PNG/MP4/CSV/JSON 등 결과
- 한국어 lesson report
- shared progress 갱신

설치만 하거나 코드만 생성한 상태는 `done`이 아니다.

## 7. 환경 분리

semantic environment role은 host와 무관하게 유지한다.

- `core-dev`
- `ros2-dev`
- `lerobot-dev`
- `gpu-mjlab`
- `gpu-isaac-vendor`
- `gpu-isaac-modern`
- `gpu-lerobot`
- `robot-runtime`

동일 role이라도 macOS-arm64와 Linux-x86_64 lock은 각각 생성할 수 있으며 virtual environment 자체는 복사하지 않는다.

## 8. 실물 안전

실물 단계에서는 WS1/WS2라는 이름보다 `ROBOT_RUNTIME` mode와 safety capability가 중요하다.

```text
offline replay
→ no-hardware command sink
→ read-only hardware
→ live no-command shadow
→ torque-disabled replay
→ explicit run card
→ one approved low-risk motion
```

명시적 승인 없이 torque, joint/base motion, contact, system-ID excitation, firmware update 또는 limit 변경을 수행하지 않는다.
