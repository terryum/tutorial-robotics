# Execution Model — Capability-First, Git-Synchronized

> 이 저장소에는 **MacBook → WS2라는 필수 장비 순서가 없다.**
> 학습 순서는 tutorial prerequisite DAG가 결정하고, 실행 가능 여부는 현재 호스트의 capability가 결정한다.

## 1. 핵심 원칙

```text
한 개의 Git repository
+ 한 개의 shared tutorial progress
+ 한 개의 non-secret cross-host status ledger
+ 호스트마다 별도의 local environment/capability
```

- **WS2는 MacBook 학습 경로의 상위 호환**이다. WS2는 core MuJoCo·제어·ROS 2·작은 RL/IL/VLA 튜토리얼과 CUDA/Isaac/mjlab 확장 튜토리얼을 모두 수행할 수 있다.
- **MacBook은 이동형 continuation host**다. 현재 capability로 실행 가능한 튜토리얼을 계속하고, CUDA/Isaac/Ubuntu-vendor 전용 튜토리얼은 shared status를 바꾸지 않은 채 건너뛴다.
- 튜토리얼 완료는 어느 컴퓨터에서 했는지가 아니라 **코드·테스트·실행 결과·리포트가 Git history에 존재하는가**로 판단한다.
- 같은 튜토리얼을 다른 호스트에서 다시 검증하고 싶으면 global progress를 되돌리지 않고 `local verification`으로 실행한다.
- 각 host가 마지막으로 확인한 commit, non-secret readiness, 현재 작업과 다음
  행동은 `state/HOST_STATUS.md`에 기록하고 tutorial/설치 결과를 push할 때
  해당 host 행을 함께 갱신한다.

## 2. 실행 mode와 host capability를 구분한다

### `DEVELOPMENT`

MacBook·WS2와 실물 연결 이전의 WS1 오프라인 checkout에서 사용한다. WS1도 capability가 맞으면 공통 설치·MuJoCo·ROS 검증을 수행한다. 장비 이름은 명령 권한이 아니다.

- model download/inspection
- MuJoCo and control
- ROS 2 fundamentals and bridge
- Gymnasium/PPO
- LeRobot/BC/ACT/VLA
- CUDA/Isaac/mjlab when the host supports them

### `ROBOT_RUNTIME`

WS1 또는 고립된 WS2에서 사용한다.

- vendor driver
- read-only state
- shadow/replay
- calibrated low-risk motion
- real data recording
- inference and gated evaluation

WS2에서 `ROBOT_RUNTIME`으로 전환할 때는 training/Isaac batch를 모두 종료하고 robot NIC·runtime environment·command authority를 분리한다.

## 3. 대표 capability set

| Capability | MacBook M4 Pro | WS2 Ubuntu/NVIDIA | WS1 robot runtime |
|---|---:|---:|---:|
| `dev_core` | yes | yes | possible |
| `mujoco_supported` | yes | yes | possible |
| `rendering_supported` | yes/offscreen | yes | optional |
| `small_ml_supported` | CPU/MPS | CPU/CUDA | optional |
| `lerobot_supported` | small experiments | yes | inference only |
| `ros2_core_supported` | RoboStack 가능 | native Jazzy | native Jazzy |
| `ubuntu_24_04_x86_64` | no | yes | yes |
| `nvidia_cuda` | no | yes | likely yes, but training discouraged |
| `mjlab_supported` | evaluation-limited | yes | no need |
| `isaac_sim_supported` | remote client only | yes | optional/runtime only |
| `robot_runtime_supported` | no | mode 전환 시 yes | yes |

표는 기본 예상치다. 실제 값은 `$bootstrap-host`가 `.local/HOST_CAPABILITIES.md`에 기록한다.

## 4. 다음 튜토리얼 선택

Codex는 `tutorials/INDEX.md` 순서를 보되 다음 조건을 만족하는 첫 tutorial을 선택한다.

1. shared status가 `pending` 또는 `blocked-retry`
2. prerequisite가 모두 완료
3. 현재 execution mode가 허용
4. `requires`가 현재 host capability의 부분집합
5. 실물 단계라면 해당 safety gate와 per-run 승인 충족

현재 호스트가 지원하지 않는 tutorial은 host-specific shared 상태로 바꾸지 않는다. 단지 이번 host의 후보 목록에서 제외한다.

### 예시

```text
WS2에서 T00부터 시작
→ T01, T02 ... core curriculum 실행
→ 같은 호스트에서 T18, T26, T33 등 GPU/Linux 단계까지 계속
```

```text
WS2에서 T24까지 완료 후 Git push
→ 이동 중 MacBook에서 pull
→ T25 또는 T28처럼 현재 capability와 prerequisite가 맞는 tutorial 실행
→ 다시 push
→ 회사에서 WS2가 pull하고 GPU-only tutorial 계속
```

## 5. 교육적 일관성

WS2에서 core tutorial을 실행할 때도 GPU/vendor example로 바로 건너뛰지 않는다.

```text
작은 deterministic baseline
→ 수식·상태·제어 흐름 이해
→ 테스트와 시각화
→ 필요할 때 GPU scale-up
```

즉 WS2의 성능은 기초 단계를 생략하기 위한 것이 아니라 같은 코드를 더 크게 실험하기 위한 것이다.

## 6. MacBook에서만 의미가 있는 항목

필수 curriculum에는 없다. 다음은 선택적 portability 검증이다.

- macOS arm64 package compatibility
- MPS fallback/성능 확인
- RoboStack ROS 2 동작 확인
- 배터리·메모리 제약에서 작은 workload 실행
- SSH/WebRTC/dashboard cockpit

이 항목들은 `setup/12_MACOS_PORTABILITY_CHECK.md`에 있으며 GPU curriculum의 prerequisite가 아니다.

## 7. 실물 로봇 권장 위치

- 공개 로봇 실험은 격리된 runtime host를 권장한다.
- 비공개 하드웨어 배치와 통합 규칙은 private overlay에서만 정의한다.
- 기술적으로는 capability와 safety 조건을 충족한 host에서만 실행한다.

로봇 하나에는 active command authority가 하나만 존재해야 한다.
