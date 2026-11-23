<!-- pal:language:start -->
<p align="right">
  <a href="README.ko.md" lang="ko">한국어</a> | <a href="README.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Tutorial Robotics — 로봇공학 교재

기초 Python 독자가 코드·수식·측정 결과를 함께 배우는 한영 로봇공학 교재입니다.
한 수업의 직관 → 핵심 수식 → 코드 → 측정 결과 → 한 변수 비교 → 이해 확인을
연결합니다. [한국어 학습 지도](docs/ko/index.md)에서 시작하세요.

## 학습 경로 선택

먼저 공통 기초 `core-00`–`core-04`를 읽고 목적에 맞는 경로를 선택합니다.
필요한 수학은 [공통 개념 11장](docs/ko/index.md#공통-개념-11장)에서 예제와 함께 설명합니다.

| 목표 | 경로 | 첫 전문화 | 장비 전환점 |
|---|---|---|---|
| 팔 제어와 학습 | [매니퓰레이터](docs/ko/paths.md) | FR3 → 별도 학습한 Enlight | 실제 PhysX 후 별도로 승인하는 실물 준비 |
| 정교한 손 조작 이해 | [로봇 손](docs/ko/paths.md) | Shadow Hand → Wuji | PhysX 후 장비 후속 단계 |
| 베이스·팔 협응 | [이동형 매니퓰레이터](docs/ko/paths.md) | Stretch 3 | 로컬 MuJoCo 후 PhysX |

[장비·환경 안내](docs/ko/equipment.md)는 맥북 로컬 실행과 WS 원격 실행을 나눕니다.
맥북 독립 실행 대상은 Core 33개와 배포·오프라인 sink 2개입니다. 엔진 비교는
별도로 생산한 실제 PhysX 근거가 필요합니다. WS1·WS2라는 이름이 아닌 실제
Ubuntu·ROS·CUDA·Isaac·로봇 런타임 역량으로 실행 가능 여부를 판단합니다.
[전체 72개 수업 안내](docs/ko/lessons.md)에서 목표·선행 조건·환경을 확인할 수 있습니다.

## 처음 시작하기

[실행 안내](docs/ko/READER_GUIDE.md)는 명령 의미, 새 터미널, 결과 열기와 재개를 설명합니다.
처음에는 다음 계획을 확인합니다.

```bash
git clone https://github.com/terryum/tutorial-robotics.git
cd tutorial-robotics
sh bootstrap.sh --plan
```

계획에는 OS·아키텍처·Python·uv·디스크와 설치할 위치·명령이 표시됩니다.
계획을 확인한 뒤 최소 Core 환경을 준비합니다.

```bash
sh bootstrap.sh --apply
source .venv/bin/activate
pal host detect --json
pal setup verify --profile core --json
pal course init --through core --json
pal course next --json
pal lesson run core-00 --headless --output-dir .local/runs/core-00/first --json
pal lesson check core-00 --run-dir .local/runs/core-00/first --json
```

[첫 수업 core-00](docs/ko/lessons/core-00.md)의 설명·비교·검토·완료 절차를 이어갑니다.
실행만으로 수업이 완료되지 않습니다. 기존 실행 디렉터리를 덮어쓰지 말고 새 경로를
사용하세요. 환경 준비는 기존 Python 3.12와 잠금 파일을 재사용하며, 시스템 패키지·
드라이버·ROS·Isaac·펌웨어·대형 모델은 자동 설치하지 않습니다.

에이전트 학습은 현재 언어의 GitHub 수업을 열고 같은 탭을 재사용합니다.
우측 상단의 한국어/영어 선택은 대응 문서로 이동합니다. README 언어 선택은 해당
언어의 README로, 교재 안의 언어 선택은 같은 개념·수업으로 이동합니다.
브라우저에서 선택한 언어를 다음 수업에서도 유지합니다.

## 바로 사용할 요청

| 목적 | 요청 |
|---|---|
| 처음 | 처음 시작할게. bootstrap 계획을 보여주고 필요한 Core 환경을 준비한 뒤 T00 하나를 실행·검사·설명해줘. |
| 다음 | 다음 단계 실행해줘. |
| 다시 | 다시 실행해줘. |
| 경로 | 매니퓰레이터 튜토리얼 실행해줘. |
| 개선 | [개선점] 그래프 단위를 더 설명해줘. |

“[개선점] 지금 바로 고쳐줘 …”는 개선 요청을 저장하고, 진행 중인 소프트웨어 실험을
안전하게 중단한 뒤 수정·재검증하고 같은 수업을 새 실행으로 재개합니다.
Codex와 Claude Code는 같은 [학습 워크플로](agent/workflow.md)를 사용합니다.

## 저장된 진도와 원격 개발

진도·세션·피드백·원시 실행 근거는 무시되는 `.local/`에 남습니다. 같은 체크아웃에서
가상환경을 활성화하고 `pal course list/status/next --json`으로 재개합니다.
`course init`은 완료 이력을 보존합니다. 새 복제본은 빈 진도로 시작합니다.
명시적으로 등록한 개인 helper만 최소 메타데이터를 별도 비공개 저장소에 동기화하며,
원시 실행·장비 정보·승인은 동기화하지 않습니다. [개인 진도 안내](docs/PERSONAL_PROGRESS.md)를 읽으세요.

[맥북→WS 원격 개발 가이드](docs/ko/setup/remote-development/index.md)는 기존 환경 확인,
RustDesk·Tailscale·SSH/VS Code, tmux·체크포인트와 호스트별 검증을 설명합니다.
가상환경을 호스트 사이에 복사하지 않습니다. 맥북 선행 완료는 WS 학습의 필수 조건이 아닙니다.
[최신 환경 설치·업데이트 안내](setup/LATEST_ROBOTICS_UPDATE.md)는 별도 범위입니다.

## 근거와 완료의 범위

전체는 Core 33개·Sim 27개·Hardware 12개입니다. Hardware 중 하나는 오프라인 sink이고
나머지 11개는 골격만 구현되어 있습니다. `implemented`는 호스트 준비·정책 성능·실물
승인을 뜻하지 않습니다. ACT 계약·VLA mock·최적화 실행·독립 평가·실물 준비를 구별합니다.
필요한 외부 환경이 없으면 `capability-unavailable` 또는 기존 검증 배지를 유지합니다.

[측정 검증 보고](docs/verification/reader-experience.md)와
[로봇 경로 검증](docs/verification/robot-paths-2026-11-08.md)은 근거와 남은 검사를 구분합니다.
공유 공개 검증 상태는 [state/PUBLISHING.md](state/PUBLISHING.md)에 있습니다.
어떤 문서·시뮬레이션 결과도 실물 동작을 승인하지 않습니다. [안전 규칙](docs/07_SAFETY.md)을 따릅니다.

## 개발 검증

```bash
uv sync --locked --python 3.12
source .venv/bin/activate
pytest
ruff check .
mypy src
python scripts/validate_repository.py
python scripts/validate_release.py
mkdocs build --strict
```

개발 실험은 `PAL_LOCAL_DIR`로 학습 상태와 분리합니다. 메타데이터 생성기
`python scripts/generate_curriculum.py`는 관리 블록만 갱신하고 저술 본문을 보존합니다.
수업 명세는 `python scripts/book_spec.py`로 갱신합니다.

## 장비 단계와 NVIDIA 경험

노트북부터 시작해 검증된 GPU 워크스테이션, 필요할 때만 선택형 Quest 3/MANUS/VIVE·UMI 수집 장비를 더하고, 실제 FR3/Enlight 동작은 마지막에 배웁니다. [장비 단계 안내](docs/ko/equipment-stages.md)와 [NVIDIA 경험 워크북](docs/ko/nvidia-ecosystem.md)은 Isaac Sim·Lab·Teleop/Capture·GR00T·배포 실습을 연결합니다. 기존 VR 없는 경로도 유지합니다.

## Codex Harness를 사용하는 교재 제작

이 저장소는 [Codex Harness](https://github.com/revfactory/codex-harness)
리비전 `80f8217b5b6d3f220a31f05f9c0adaf09dac40f4`의 프로젝트 로컬 사본으로
저술·독립 검토·실행 QA를 조율합니다. 세 가지 교재 제작 스킬은 구현·산출물·개념 장과
한영 수업을 연결합니다. 교재 제작 자체로 학습 실행이나 장비 동작을 시작하지 않습니다.

가져온 스킬·기본 역할 5개는 Apache-2.0입니다. 재배포에 필요한
[라이선스 전문](third_party/codex-harness/LICENSE), 원저작자 표시를 포함한
[NOTICE](third_party/codex-harness/NOTICE), [출처·로컬 추가 내역](third_party/codex-harness/PROVENANCE.md)을
함께 제공합니다. 원저작자 표시는 유지하며 공식 보증을 의미하지 않습니다.
로봇 자산은 개별 라이선스를 유지합니다. 제작 진입점은
[교재 오케스트레이터](.agents/skills/robotics-book-orchestrator/SKILL.md)입니다.
재사용 스킬·템플릿·검사는 Git으로 관리하고 실행 출력과 통신 기록은 제외합니다.

## 전체 수업 목차

<!-- pal:toc:start -->
| # | ID / alias | English | 한국어 |
|---:|---|---|---|
| 1 | core-00 / T00 | [Repository bootstrap and host audit](docs/en/lessons/core-00.md) | [저장소 시작과 호스트 점검](docs/ko/lessons/core-00.md) |
| 2 | core-01 / T01 | [Deterministic pendulum state and timestep](docs/en/lessons/core-01.md) | [결정론적 진자 상태와 시간 간격](docs/ko/lessons/core-01.md) |
| 3 | core-02 / T02 | [Pinned public robot sources](docs/en/lessons/core-02.md) | [공개 로봇 소스 고정과 자산 매니페스트](docs/ko/lessons/core-02.md) |
| 4 | core-03 / T03 | [Multi-model inspection and asset validation](docs/en/lessons/core-03.md) | [다중 모델 검사와 자산 검증](docs/ko/lessons/core-03.md) |
| 5 | core-04 / T04 | [Unified viewer and deterministic rendering](docs/en/lessons/core-04.md) | [통합 뷰어와 결정론적 렌더링](docs/ko/lessons/core-04.md) |
| 6 | core-teleop-01 /  | [Bimanual input, clutch and replay](docs/en/lessons/core-teleop-01.md) | [양손 입력·클러치·재생](docs/ko/lessons/core-teleop-01.md) |
| 7 | core-fr3-01 / T05 | [FR3 model anatomy](docs/en/lessons/core-fr3-01.md) | [FR3 모델 구조](docs/ko/lessons/core-fr3-01.md) |
| 8 | core-fr3-02 / T06 | [FR3 joint-space PD control](docs/en/lessons/core-fr3-02.md) | [FR3 관절 공간 PD 제어](docs/ko/lessons/core-fr3-02.md) |
| 9 | core-fr3-03 / T07 | [FR3 gravity compensation and feedforward](docs/en/lessons/core-fr3-03.md) | [FR3 중력 보상과 피드포워드](docs/ko/lessons/core-fr3-03.md) |
| 10 | core-fr3-04 / T08 | [FR3 kinematics, Jacobian, and inverse kinematics](docs/en/lessons/core-fr3-04.md) | [FR3 기구학, 자코비안과 역기구학](docs/ko/lessons/core-fr3-04.md) |
| 11 | core-fr3-05 / T09 | [FR3 operational-space control](docs/en/lessons/core-fr3-05.md) | [FR3 작업 공간 제어](docs/ko/lessons/core-fr3-05.md) |
| 12 | core-fr3-06 / T10 | [FR3 contact and friction laboratory](docs/en/lessons/core-fr3-06.md) | [FR3 접촉과 마찰 실험실](docs/ko/lessons/core-fr3-06.md) |
| 13 | core-rl-01 / T23 | [Minimal continuous-action PPO](docs/en/lessons/core-rl-01.md) | [최소 연속 행동 PPO](docs/ko/lessons/core-rl-01.md) |
| 14 | core-fr3-07 / T22 | [FR3 reach environment without ROS](docs/en/lessons/core-fr3-07.md) | [ROS 없는 FR3 도달 환경](docs/ko/lessons/core-fr3-07.md) |
| 15 | core-fr3-08 / T24 | [PPO on FR3 reach](docs/en/lessons/core-fr3-08.md) | [FR3 도달 과제 PPO](docs/ko/lessons/core-fr3-08.md) |
| 16 | core-enlight-01 / T08A | [Enlight description, frames, and kinematics](docs/en/lessons/core-enlight-01.md) | [Enlight 모델, 좌표계와 기구학](docs/ko/lessons/core-enlight-01.md) |
| 17 | core-enlight-02 / T10A | [Enlight MuJoCo draft and cross-format validation](docs/en/lessons/core-enlight-02.md) | [Enlight MuJoCo 초안과 형식 간 검증](docs/ko/lessons/core-enlight-02.md) |
| 18 | core-wuji-01 / T14 | [Wuji Hand 2 Beta 2 joints, poses, and synergies](docs/en/lessons/core-wuji-01.md) | [Wuji Hand 2 Beta 2 관절, 자세와 시너지](docs/ko/lessons/core-wuji-01.md) |
| 19 | core-wuji-02 / T15 | [Wuji virtual tactile observation](docs/en/lessons/core-wuji-02.md) | [Wuji 가상 촉각 관측](docs/ko/lessons/core-wuji-02.md) |
| 20 | core-dexterity-01 / T16 | [Wuji and Sharpa model comparison](docs/en/lessons/core-dexterity-01.md) | [Wuji와 Sharpa 모델 비교](docs/ko/lessons/core-dexterity-01.md) |
| 21 | core-data-01 / T28 | [Episode dataset from MuJoCo](docs/en/lessons/core-data-01.md) | [MuJoCo 에피소드 데이터셋](docs/ko/lessons/core-data-01.md) |
| 22 | core-dexterity-02 / T16A | [Hand retargeting and demonstration recording](docs/en/lessons/core-dexterity-02.md) | [손 리타게팅과 시연 기록](docs/ko/lessons/core-dexterity-02.md) |
| 23 | core-g1-01 / T25 | [Unitree G1 playback and motion data](docs/en/lessons/core-g1-01.md) | [Unitree G1 재생과 모션 데이터](docs/ko/lessons/core-g1-01.md) |
| 24 | core-il-01 / T29 | [Behavioral cloning baseline](docs/en/lessons/core-il-01.md) | [행동 복제 기준선](docs/ko/lessons/core-il-01.md) |
| 25 | core-aloha-01 / T30 | [ALOHA simulation and ACT contract](docs/en/lessons/core-aloha-01.md) | [ALOHA 시뮬레이션과 ACT 계약](docs/ko/lessons/core-aloha-01.md) |
| 26 | core-vla-01 / T32A | [VLA protocol and mock policy client](docs/en/lessons/core-vla-01.md) | [VLA 프로토콜과 모의 정책 클라이언트](docs/ko/lessons/core-vla-01.md) |
| 27 | sim-ros-01 / T17 | [ROS 2 topics, QoS, services, actions, and TF](docs/en/lessons/sim-ros-01.md) | [ROS 2 토픽, QoS, 서비스, 액션과 TF](docs/ko/lessons/sim-ros-01.md) |
| 28 | sim-ros-02 / T19 | [MuJoCo to ROS 2 bridge](docs/en/lessons/sim-ros-02.md) | [MuJoCo–ROS 2 브리지](docs/ko/lessons/sim-ros-02.md) |
| 29 | sim-ros-03 / T20 | [Rosbag episode recording and deterministic replay](docs/en/lessons/sim-ros-03.md) | [rosbag 에피소드 기록과 결정론적 재생](docs/ko/lessons/sim-ros-03.md) |
| 30 | sim-ros-04 / T21 | [Common embodiment API for simulation and ROS 2](docs/en/lessons/sim-ros-04.md) | [시뮬레이션과 ROS 2 공통 embodiment API](docs/ko/lessons/sim-ros-04.md) |
| 31 | sim-g1-01 / T26 | [Unitree G1 GPU PPO and motion imitation](docs/en/lessons/sim-g1-01.md) | [Unitree G1 GPU PPO와 모션 모방](docs/ko/lessons/sim-g1-01.md) |
| 32 | sim-wuji-01 / T27 | [Wuji in-hand PPO on GPU](docs/en/lessons/sim-wuji-01.md) | [Wuji GPU 손안 조작 PPO](docs/ko/lessons/sim-wuji-01.md) |
| 33 | sim-vla-01 / T32C | [SmolVLA fine-tuning and policy server](docs/en/lessons/sim-vla-01.md) | [SmolVLA 미세조정과 정책 서버](docs/ko/lessons/sim-vla-01.md) |
| 34 | sim-vla-02 / T32D | [Optional remote VLA inference](docs/en/lessons/sim-vla-02.md) | [선택형 원격 VLA 추론](docs/ko/lessons/sim-vla-02.md) |
| 35 | sim-isaac-01 / T33 | [Import public robot assets into Isaac Sim](docs/en/lessons/sim-isaac-01.md) | [Isaac Sim 공개 로봇 자산 가져오기](docs/ko/lessons/sim-isaac-01.md) |
| 36 | sim-isaac-02 / T34 | [Isaac camera, lighting, and synthetic data](docs/en/lessons/sim-isaac-02.md) | [Isaac 카메라, 조명과 합성 데이터](docs/ko/lessons/sim-isaac-02.md) |
| 37 | sim-cross-01 / T35 | [MuJoCo to Isaac sim-to-sim validation](docs/en/lessons/sim-cross-01.md) | [MuJoCo–Isaac sim-to-sim 검증](docs/ko/lessons/sim-cross-01.md) |
| 38 | sim-deploy-01 / T35A | [Candidate deployment bundle and promotion gate](docs/en/lessons/sim-deploy-01.md) | [후보 배포 번들과 승격 게이트](docs/ko/lessons/sim-deploy-01.md) |
| 39 | sim-enlight-01 / T18 | [Enlight ROS 2 fake hardware](docs/en/lessons/sim-enlight-01.md) | [Enlight ROS 2 가상 하드웨어](docs/ko/lessons/sim-enlight-01.md) |
| 40 | sim-enlight-02 / T41A | [Enlight contact-task simulation and candidate bundle](docs/en/lessons/sim-enlight-02.md) | [Enlight 접촉 과제 시뮬레이션과 후보 번들](docs/ko/lessons/sim-enlight-02.md) |
| 41 | sim-wuji-02 / T42A | [Wuji dexterity candidate bundle](docs/en/lessons/sim-wuji-02.md) | [Wuji 정교 조작 후보 번들](docs/ko/lessons/sim-wuji-02.md) |
| 42 | hw-common-01 / T35B | [Runtime bootstrap, offline replay, and command sink](docs/en/lessons/hw-common-01.md) | [런타임 시작, 오프라인 재생과 명령 차단](docs/ko/lessons/hw-common-01.md) |
| 43 | hw-common-02 / T36 | [Real-hardware read-only integration gate](docs/en/lessons/hw-common-02.md) | [실물 하드웨어 읽기 전용 통합 게이트](docs/ko/lessons/hw-common-02.md) |
| 44 | hw-fr3-01 /  | [FR3 read-only state, shadow, and approved low-risk motion](docs/en/lessons/hw-fr3-01.md) | [FR3 읽기 전용 상태, 섀도와 승인된 저위험 동작](docs/ko/lessons/hw-fr3-01.md) |
| 45 | hw-wuji-01 / T38 | [Wuji Beta 2 read-only adapter and tactile calibration](docs/en/lessons/hw-wuji-01.md) | [Wuji Beta 2 읽기 전용 어댑터와 촉각 보정](docs/ko/lessons/hw-wuji-01.md) |
| 46 | hw-wuji-02 / T42B | [Wuji shadow and gated real evaluation](docs/en/lessons/hw-wuji-02.md) | [Wuji 섀도와 승인 기반 실물 평가](docs/ko/lessons/hw-wuji-02.md) |
| 47 | hw-enlight-01 / T37 | [Enlight read-only adapter and low-risk validation](docs/en/lessons/hw-enlight-01.md) | [Enlight 읽기 전용 어댑터와 저위험 검증](docs/ko/lessons/hw-enlight-01.md) |
| 48 | hw-enlight-02 / T37A | [Enlight system identification and MuJoCo calibration](docs/en/lessons/hw-enlight-02.md) | [Enlight 시스템 식별과 MuJoCo 보정](docs/ko/lessons/hw-enlight-02.md) |
| 49 | hw-enlight-03 / T41B | [Enlight contact-task shadow and gated evaluation](docs/en/lessons/hw-enlight-03.md) | [Enlight 접촉 과제 섀도와 승인 기반 평가](docs/ko/lessons/hw-enlight-03.md) |
| 50 | hw-enlight-wuji-01 / T38A | [Enlight and Wuji integrated read-only validation](docs/en/lessons/hw-enlight-wuji-01.md) | [Enlight와 Wuji 통합 읽기 전용 검증](docs/ko/lessons/hw-enlight-wuji-01.md) |
| 51 | core-fr3-09 /  | [FR3 joint and TCP trajectory tracking](docs/en/lessons/core-fr3-09.md) | [FR3 관절·TCP 궤적 추종](docs/ko/lessons/core-fr3-09.md) |
| 52 | core-fr3-10 /  | [FR3 demonstrations, BC and independent reach evaluation](docs/en/lessons/core-fr3-10.md) | [FR3 시연·BC와 독립 도달 평가](docs/ko/lessons/core-fr3-10.md) |
| 53 | sim-fr3-01 /  | [FR3 PhysX joint and TCP control](docs/en/lessons/sim-fr3-01.md) | [FR3 PhysX 관절·TCP 제어](docs/ko/lessons/sim-fr3-01.md) |
| 54 | sim-fr3-02 /  | [FR3 PhysX demonstrations and BC](docs/en/lessons/sim-fr3-02.md) | [FR3 PhysX 시연·BC](docs/ko/lessons/sim-fr3-02.md) |
| 55 | sim-fr3-03 /  | [FR3 PhysX PPO and evaluation](docs/en/lessons/sim-fr3-03.md) | [FR3 PhysX PPO와 평가](docs/ko/lessons/sim-fr3-03.md) |
| 56 | sim-fr3-04 /  | [FR3 matched-engine evidence comparison](docs/en/lessons/sim-fr3-04.md) | [FR3 동일 조건 엔진 증거 비교](docs/ko/lessons/sim-fr3-04.md) |
| 57 | core-enlight-03 /  | [Enlight joint and TCP trajectory tracking](docs/en/lessons/core-enlight-03.md) | [Enlight 관절·TCP 궤적 추종](docs/ko/lessons/core-enlight-03.md) |
| 58 | core-enlight-04 /  | [Enlight demonstrations, BC and independent evaluation](docs/en/lessons/core-enlight-04.md) | [Enlight 시연·BC와 독립 평가](docs/ko/lessons/core-enlight-04.md) |
| 59 | core-enlight-05 /  | [Enlight PPO candidate and independent evaluation](docs/en/lessons/core-enlight-05.md) | [Enlight PPO 후보와 독립 평가](docs/ko/lessons/core-enlight-05.md) |
| 60 | sim-enlight-03 /  | [Enlight PhysX joint and TCP control](docs/en/lessons/sim-enlight-03.md) | [Enlight PhysX 관절·TCP 제어](docs/ko/lessons/sim-enlight-03.md) |
| 61 | sim-enlight-04 /  | [Enlight PhysX demonstrations and BC](docs/en/lessons/sim-enlight-04.md) | [Enlight PhysX 시연·BC](docs/ko/lessons/sim-enlight-04.md) |
| 62 | sim-enlight-05 /  | [Enlight PhysX PPO and evaluation](docs/en/lessons/sim-enlight-05.md) | [Enlight PhysX PPO와 평가](docs/ko/lessons/sim-enlight-05.md) |
| 63 | core-shadow-01 /  | [Shadow Hand joints, synergies and object contact](docs/en/lessons/core-shadow-01.md) | [Shadow Hand 관절·시너지·물체 접촉](docs/ko/lessons/core-shadow-01.md) |
| 64 | sim-shadow-01 /  | [Shadow Hand PhysX introduction](docs/en/lessons/sim-shadow-01.md) | [Shadow Hand PhysX 입문](docs/ko/lessons/sim-shadow-01.md) |
| 65 | core-stretch3-01 /  | [Stretch 3 base, arm and coordinated reach](docs/en/lessons/core-stretch3-01.md) | [Stretch 3 베이스·팔·협응 도달](docs/ko/lessons/core-stretch3-01.md) |
| 66 | sim-stretch3-01 /  | [Stretch 3 PhysX introduction](docs/en/lessons/sim-stretch3-01.md) | [Stretch 3 PhysX 입문](docs/ko/lessons/sim-stretch3-01.md) |
| 67 | hw-enlight-04 /  | [Enlight free-space joint and TCP execution cards](docs/en/lessons/hw-enlight-04.md) | [Enlight 자유공간 관절·TCP 실행 카드](docs/ko/lessons/hw-enlight-04.md) |
| 68 | hw-enlight-05 /  | [Enlight probe plane-force preparation](docs/en/lessons/hw-enlight-05.md) | [Enlight 프로브 평면 힘 제어 준비](docs/ko/lessons/hw-enlight-05.md) |
| 69 | hw-enlight-06 /  | [Enlight gripper pick-transfer-place preparation](docs/en/lessons/hw-enlight-06.md) | [Enlight 그리퍼 집기·이동·놓기 준비](docs/ko/lessons/hw-enlight-06.md) |
| 70 | sim-teleop-01 /  | [Ubuntu VR installation and read-only input](docs/en/lessons/sim-teleop-01.md) | [Ubuntu VR 설치와 읽기 전용 입력](docs/ko/lessons/sim-teleop-01.md) |
| 71 | sim-teleop-02 /  | [Spatial alignment and command sink](docs/en/lessons/sim-teleop-02.md) | [공간 정합과 command sink](docs/ko/lessons/sim-teleop-02.md) |
| 72 | sim-enlight-06 /  | [Enlight arm teleoperation and collection](docs/en/lessons/sim-enlight-06.md) | [Enlight 팔 텔레오퍼레이션과 수집](docs/ko/lessons/sim-enlight-06.md) |
<!-- pal:toc:end -->

[교재 제작 검증과 남은 외부 환경 검사](docs/verification/book-production-2026-11-23.md).
