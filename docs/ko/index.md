<!-- pal:language:start -->
<p align="right">
  <a href="index.md" lang="ko">한국어</a> | <a href="../en/index.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 로봇공학 학습 지도

기초 Python을 알고 있다면 이 지도에서 시작하세요. 코드를 실행하고 그래프를 읽는 것과 로봇공학 개념을 함께 배웁니다. 먼저 공통 기초 다섯 수업을 읽고 매니퓰레이터·로봇 손·이동형 로봇 경로를 선택하세요. 각 수업은 직관 → 핵심 수식 → 코드 → 측정 결과 → 한 변수 비교 → 이해 확인을 연결합니다.

## 어디서 시작할까요?

1. [장비·환경 안내](equipment.md)에서 로컬 실행과 원격 실행 범위를 확인합니다.
2. [실행 안내](READER_GUIDE.md)와 [core-00](lessons/core-00.md)에서 최소 환경 계획을 확인합니다.
3. [경로 안내](paths.md)에서 목적·선행 지식·수업 순서·장비 전환점을 확인합니다.
4. 필요한 [공통 개념 장](#공통-개념-11장)을 읽고 개별 수업으로 돌아옵니다.
5. [전체 72개 수업 안내](lessons.md)에서 목표·선행 조건·환경을 비교합니다.

수업 실행만으로 완료되지 않습니다. 산출물을 검사하고 설명·한 변수 비교를 기록해야 합니다. `pal course next --json`이 현재 준비 상태와 진도로 실제 다음 수업을 정합니다. 아래 표는 카탈로그 순서이며 선택한 경로의 학습 순서와 다를 수 있습니다.

## 공통 개념 11장

1. [시뮬레이션과 재현성](concepts/simulation.md)
2. [좌표계·기구학·자코비안](concepts/kinematics.md)
3. [제어와 접촉](concepts/control-contact.md)
4. [강화학습](concepts/reinforcement-learning.md)
5. [데이터와 모방학습](concepts/data-imitation.md)
6. [로봇 손](concepts/robot-hands.md)
7. [이동형 로봇과 모션](concepts/mobile-motion.md)
8. [ROS 통신](concepts/ros.md)
9. [PhysX와 엔진 비교](concepts/physx.md)
10. [비전·언어·행동 프로토콜](concepts/vla.md)
11. [배포와 실물 검증](concepts/deployment-hardware.md)

## 전체 수업 목록

<!-- pal:catalog:start -->
| # | Lesson | Stage | Track | Verification |
|---:|---|---|---|---|
| 1 | [core-00](lessons/core-00.md) — 저장소 시작과 호스트 점검 | `core` | `common` | `maintainer-checked` |
| 2 | [core-01](lessons/core-01.md) — 결정론적 진자 상태와 시간 간격 | `core` | `common` | `maintainer-checked` |
| 3 | [core-02](lessons/core-02.md) — 공개 로봇 소스 고정과 자산 매니페스트 | `core` | `common` | `maintainer-checked` |
| 4 | [core-03](lessons/core-03.md) — 다중 모델 검사와 자산 검증 | `core` | `common` | `maintainer-checked` |
| 5 | [core-04](lessons/core-04.md) — 통합 뷰어와 결정론적 렌더링 | `core` | `common` | `maintainer-checked` |
| 6 | [core-teleop-01](lessons/core-teleop-01.md) — 양손 입력·클러치·재생 | `core` | `common` | `maintainer-checked` |
| 7 | [core-fr3-01](lessons/core-fr3-01.md) — FR3 모델 구조 | `core` | `fr3` | `maintainer-checked` |
| 8 | [core-fr3-02](lessons/core-fr3-02.md) — FR3 관절 공간 PD 제어 | `core` | `fr3` | `maintainer-checked` |
| 9 | [core-fr3-03](lessons/core-fr3-03.md) — FR3 중력 보상과 피드포워드 | `core` | `fr3` | `maintainer-checked` |
| 10 | [core-fr3-04](lessons/core-fr3-04.md) — FR3 기구학, 자코비안과 역기구학 | `core` | `fr3` | `maintainer-checked` |
| 11 | [core-fr3-05](lessons/core-fr3-05.md) — FR3 작업 공간 제어 | `core` | `fr3` | `maintainer-checked` |
| 12 | [core-fr3-06](lessons/core-fr3-06.md) — FR3 접촉과 마찰 실험실 | `core` | `fr3` | `maintainer-checked` |
| 13 | [core-rl-01](lessons/core-rl-01.md) — 최소 연속 행동 PPO | `core` | `learning` | `maintainer-checked` |
| 14 | [core-fr3-07](lessons/core-fr3-07.md) — ROS 없는 FR3 도달 환경 | `core` | `fr3` | `maintainer-checked` |
| 15 | [core-fr3-08](lessons/core-fr3-08.md) — FR3 도달 과제 PPO | `core` | `fr3` | `maintainer-checked` |
| 16 | [core-enlight-01](lessons/core-enlight-01.md) — Enlight 모델, 좌표계와 기구학 | `core` | `enlight` | `maintainer-checked` |
| 17 | [core-enlight-02](lessons/core-enlight-02.md) — Enlight MuJoCo 초안과 형식 간 검증 | `core` | `enlight` | `maintainer-checked` |
| 18 | [core-wuji-01](lessons/core-wuji-01.md) — Wuji Hand 2 Beta 2 관절, 자세와 시너지 | `core` | `wuji` | `maintainer-checked` |
| 19 | [core-wuji-02](lessons/core-wuji-02.md) — Wuji 가상 촉각 관측 | `core` | `wuji` | `maintainer-checked` |
| 20 | [core-dexterity-01](lessons/core-dexterity-01.md) — Wuji와 Sharpa 모델 비교 | `core` | `dexterity` | `maintainer-checked` |
| 21 | [core-data-01](lessons/core-data-01.md) — MuJoCo 에피소드 데이터셋 | `core` | `learning` | `maintainer-checked` |
| 22 | [core-dexterity-02](lessons/core-dexterity-02.md) — 손 리타게팅과 시연 기록 | `core` | `dexterity` | `maintainer-checked` |
| 23 | [core-g1-01](lessons/core-g1-01.md) — Unitree G1 재생과 모션 데이터 | `core` | `g1` | `maintainer-checked` |
| 24 | [core-il-01](lessons/core-il-01.md) — 행동 복제 기준선 | `core` | `learning` | `maintainer-checked` |
| 25 | [core-aloha-01](lessons/core-aloha-01.md) — ALOHA 시뮬레이션과 ACT 계약 | `core` | `aloha` | `maintainer-checked` |
| 26 | [core-vla-01](lessons/core-vla-01.md) — VLA 프로토콜과 모의 정책 클라이언트 | `core` | `vla` | `maintainer-checked` |
| 27 | [sim-ros-01](lessons/sim-ros-01.md) — ROS 2 토픽, QoS, 서비스, 액션과 TF | `sim` | `ros2` | `reader_test_required` |
| 28 | [sim-ros-02](lessons/sim-ros-02.md) — MuJoCo–ROS 2 브리지 | `sim` | `ros2` | `reader_test_required` |
| 29 | [sim-ros-03](lessons/sim-ros-03.md) — rosbag 에피소드 기록과 결정론적 재생 | `sim` | `ros2` | `reader_test_required` |
| 30 | [sim-ros-04](lessons/sim-ros-04.md) — 시뮬레이션과 ROS 2 공통 embodiment API | `sim` | `ros2` | `reader_test_required` |
| 31 | [sim-g1-01](lessons/sim-g1-01.md) — Unitree G1 GPU PPO와 모션 모방 | `sim` | `g1` | `reader_test_required` |
| 32 | [sim-wuji-01](lessons/sim-wuji-01.md) — Wuji GPU 손안 조작 PPO | `sim` | `wuji` | `reader_test_required` |
| 33 | [sim-vla-01](lessons/sim-vla-01.md) — SmolVLA 미세조정과 정책 서버 | `sim` | `vla` | `reader_test_required` |
| 34 | [sim-vla-02](lessons/sim-vla-02.md) — 선택형 원격 VLA 추론 | `sim` | `vla` | `reader_test_required` |
| 35 | [sim-isaac-01](lessons/sim-isaac-01.md) — Isaac Sim 공개 로봇 자산 가져오기 | `sim` | `isaac` | `reader_test_required` |
| 36 | [sim-isaac-02](lessons/sim-isaac-02.md) — Isaac 카메라, 조명과 합성 데이터 | `sim` | `isaac` | `reader_test_required` |
| 37 | [sim-cross-01](lessons/sim-cross-01.md) — MuJoCo–Isaac sim-to-sim 검증 | `sim` | `cross` | `reader_test_required` |
| 38 | [sim-deploy-01](lessons/sim-deploy-01.md) — 후보 배포 번들과 승격 게이트 | `sim` | `deployment` | `maintainer-checked` |
| 39 | [sim-enlight-01](lessons/sim-enlight-01.md) — Enlight ROS 2 가상 하드웨어 | `sim` | `enlight` | `reader_test_required` |
| 40 | [sim-enlight-02](lessons/sim-enlight-02.md) — Enlight 접촉 과제 시뮬레이션과 후보 번들 | `sim` | `enlight` | `reader_test_required` |
| 41 | [sim-wuji-02](lessons/sim-wuji-02.md) — Wuji 정교 조작 후보 번들 | `sim` | `wuji` | `reader_test_required` |
| 42 | [hw-common-01](lessons/hw-common-01.md) — 런타임 시작, 오프라인 재생과 명령 차단 | `hardware` | `common` | `maintainer-checked` |
| 43 | [hw-common-02](lessons/hw-common-02.md) — 실물 하드웨어 읽기 전용 통합 게이트 | `hardware` | `common` | `reader_test_required` |
| 44 | [hw-fr3-01](lessons/hw-fr3-01.md) — FR3 읽기 전용 상태, 섀도와 승인된 저위험 동작 | `hardware` | `fr3` | `reader_test_required` |
| 45 | [hw-wuji-01](lessons/hw-wuji-01.md) — Wuji Beta 2 읽기 전용 어댑터와 촉각 보정 | `hardware` | `wuji` | `reader_test_required` |
| 46 | [hw-wuji-02](lessons/hw-wuji-02.md) — Wuji 섀도와 승인 기반 실물 평가 | `hardware` | `wuji` | `reader_test_required` |
| 47 | [hw-enlight-01](lessons/hw-enlight-01.md) — Enlight 읽기 전용 어댑터와 저위험 검증 | `hardware` | `enlight` | `reader_test_required` |
| 48 | [hw-enlight-02](lessons/hw-enlight-02.md) — Enlight 시스템 식별과 MuJoCo 보정 | `hardware` | `enlight` | `reader_test_required` |
| 49 | [hw-enlight-03](lessons/hw-enlight-03.md) — Enlight 접촉 과제 섀도와 승인 기반 평가 | `hardware` | `enlight` | `reader_test_required` |
| 50 | [hw-enlight-wuji-01](lessons/hw-enlight-wuji-01.md) — Enlight와 Wuji 통합 읽기 전용 검증 | `hardware` | `enlight-wuji` | `reader_test_required` |
| 51 | [core-fr3-09](lessons/core-fr3-09.md) — FR3 관절·TCP 궤적 추종 | `core` | `fr3` | `maintainer-checked` |
| 52 | [core-fr3-10](lessons/core-fr3-10.md) — FR3 시연·BC와 독립 도달 평가 | `core` | `fr3` | `maintainer-checked` |
| 53 | [sim-fr3-01](lessons/sim-fr3-01.md) — FR3 PhysX 관절·TCP 제어 | `sim` | `fr3` | `reader_test_required` |
| 54 | [sim-fr3-02](lessons/sim-fr3-02.md) — FR3 PhysX 시연·BC | `sim` | `fr3` | `reader_test_required` |
| 55 | [sim-fr3-03](lessons/sim-fr3-03.md) — FR3 PhysX PPO와 평가 | `sim` | `fr3` | `reader_test_required` |
| 56 | [sim-fr3-04](lessons/sim-fr3-04.md) — FR3 동일 조건 엔진 증거 비교 | `sim` | `fr3` | `reader_test_required` |
| 57 | [core-enlight-03](lessons/core-enlight-03.md) — Enlight 관절·TCP 궤적 추종 | `core` | `enlight` | `maintainer-checked` |
| 58 | [core-enlight-04](lessons/core-enlight-04.md) — Enlight 시연·BC와 독립 평가 | `core` | `enlight` | `maintainer-checked` |
| 59 | [core-enlight-05](lessons/core-enlight-05.md) — Enlight PPO 후보와 독립 평가 | `core` | `enlight` | `maintainer-checked` |
| 60 | [sim-enlight-03](lessons/sim-enlight-03.md) — Enlight PhysX 관절·TCP 제어 | `sim` | `enlight` | `reader_test_required` |
| 61 | [sim-enlight-04](lessons/sim-enlight-04.md) — Enlight PhysX 시연·BC | `sim` | `enlight` | `reader_test_required` |
| 62 | [sim-enlight-05](lessons/sim-enlight-05.md) — Enlight PhysX PPO와 평가 | `sim` | `enlight` | `reader_test_required` |
| 63 | [core-shadow-01](lessons/core-shadow-01.md) — Shadow Hand 관절·시너지·물체 접촉 | `core` | `shadow` | `maintainer-checked` |
| 64 | [sim-shadow-01](lessons/sim-shadow-01.md) — Shadow Hand PhysX 입문 | `sim` | `shadow` | `reader_test_required` |
| 65 | [core-stretch3-01](lessons/core-stretch3-01.md) — Stretch 3 베이스·팔·협응 도달 | `core` | `stretch3` | `maintainer-checked` |
| 66 | [sim-stretch3-01](lessons/sim-stretch3-01.md) — Stretch 3 PhysX 입문 | `sim` | `stretch3` | `reader_test_required` |
| 67 | [hw-enlight-04](lessons/hw-enlight-04.md) — Enlight 자유공간 관절·TCP 실행 카드 | `hardware` | `enlight` | `reader_test_required` |
| 68 | [hw-enlight-05](lessons/hw-enlight-05.md) — Enlight 프로브 평면 힘 제어 준비 | `hardware` | `enlight` | `reader_test_required` |
| 69 | [hw-enlight-06](lessons/hw-enlight-06.md) — Enlight 그리퍼 집기·이동·놓기 준비 | `hardware` | `enlight` | `reader_test_required` |
| 70 | [sim-teleop-01](lessons/sim-teleop-01.md) — Ubuntu VR 설치와 읽기 전용 입력 | `sim` | `common` | `reader_test_required` |
| 71 | [sim-teleop-02](lessons/sim-teleop-02.md) — 공간 정합과 command sink | `sim` | `common` | `maintainer-checked` |
| 72 | [sim-enlight-06](lessons/sim-enlight-06.md) — Enlight 팔 텔레오퍼레이션과 수집 | `sim` | `enlight` | `maintainer-checked` |
<!-- pal:catalog:end -->

## 장비가 늘어나는 학습 순서

[노트북 → GPU → 선택형 수집 장비 → 마지막 실물](equipment-stages.md) 순서로 읽으세요. [NVIDIA 경험 워크북](nvidia-ecosystem.md)은 Isaac Sim·Lab·Teleop/Capture·GR00T·ROS/배포를 실습과 검증 산출물로 연결합니다. XR·그리퍼·UMI는 필요한 후반 과제에서만 검토합니다.
