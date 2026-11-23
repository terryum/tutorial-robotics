<!-- pal:language:start -->
<p align="right">
  <a href="lessons.md" lang="ko">한국어</a> | <a href="../en/lessons.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 전체 72개 수업 안내

목표 요약은 각 수업의 `Learning goals` 첫 문단에서 가져옵니다. 환경·선행 수업·구현 상태는 카탈로그가 기준입니다. 검증 배지는 [학습 지도](index.md)의 표에서 확인하세요. `implemented`는 현재 호스트 실행 성공이나 정책 성능 통과를 뜻하지 않습니다. `scaffolded` 수업은 준비 교재이며 장비 근거가 없으면 차단 상태입니다.

[장비 안내](equipment.md) · [학습 경로](paths.md) · [개념 장](index.md#공통-개념-11장)

<!-- pal:goals:start -->
| Lesson | Learning goal | Prerequisites | Platforms / capabilities | Implementation |
|---|---|---|---|---|
| [core-00](lessons/core-00.md) | 호스트 준비 상태, 로컬 실행 기록, 학습 완료를 구분합니다. | — | macos-arm64, linux-x86_64; python-3.12 | `implemented` |
| [core-01](lessons/core-01.md) | 진자 상태와 수치 적분의 에너지 오차를 측정합니다. | core-00 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-02](lessons/core-02.md) | 불변 소스 커밋과 실제 모델 파일의 바이트를 검증합니다. | core-00 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-03](lessons/core-03.md) | 여섯 로봇 모델을 로드하고 실제 차원을 검사합니다. | core-01, core-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-04](lessons/core-04.md) | 실제 FR3 장면을 렌더링하고 카메라 결과를 확인합니다. | core-03 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-teleop-01](lessons/core-teleop-01.md) | 헤드셋 구매 없이 양손 데이터 계약을 배운다. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-01](lessons/core-fr3-01.md) | FR3 관절·링크·구동기와 말단 사이트를 연결합니다. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-02](lessons/core-fr3-02.md) | FR3 동역학에 제한된 관절 PD 토크를 적용합니다. | core-fr3-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-03](lessons/core-fr3-03.md) | 중력 피드포워드가 추종 오차를 어떻게 바꾸는지 측정합니다. | core-fr3-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-04](lessons/core-fr3-04.md) | 기하 자코비안을 검증하고 작은 변위의 IK를 풉니다. | core-fr3-03 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-05](lessons/core-fr3-05.md) | 작업 공간 관성을 사용해 월드 좌표의 말단 위치를 제어합니다. | core-fr3-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-06](lessons/core-fr3-06.md) | 말단 탐침과 테이블의 접촉력을 측정하고 마찰을 바꿉니다. | core-fr3-05 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-rl-01](lessons/core-rl-01.md) | 최소 연속 행동 PPO의 전체 갱신 과정을 따라갑니다. | core-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-07](lessons/core-fr3-07.md) | FR3 도달 과제의 reset·관측·행동·보상·에피소드 경계를 사용합니다. | core-fr3-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-08](lessons/core-fr3-08.md) | 실제 FR3 도달 환경에서 PPO를 학습·저장·재로딩합니다. | core-fr3-07, core-rl-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-01](lessons/core-enlight-01.md) | 공개 vendor 파라미터로 Enlight-L 좌표계를 구성합니다. | core-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-02](lessons/core-enlight-02.md) | 독립적인 vendor 순기구학과 컴파일된 MJCF를 비교합니다. | core-enlight-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-wuji-01](lessons/core-wuji-01.md) | 손 시너지로 제한된 open·half·closed 자세를 만듭니다. | core-02, core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-wuji-02](lessons/core-wuji-02.md) | Wuji 손끝의 가상 접촉력을 읽습니다. | core-wuji-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-dexterity-01](lessons/core-dexterity-01.md) | 측정된 모델 속성으로 Wuji와 Sharpa를 비교합니다. | core-wuji-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-data-01](lessons/core-data-01.md) | 실제 MuJoCo 상태·행동·다음 상태 전이를 기록합니다. | core-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-dexterity-02](lessons/core-dexterity-02.md) | 관측한 손끝 변위를 리타게팅하고 결과를 기록합니다. | core-dexterity-01, core-data-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-g1-01](lessons/core-g1-01.md) | 제한된 G1 관절 모션 주기를 기록하고 재생합니다. | core-03, core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-il-01](lessons/core-il-01.md) | 완료한 에피소드 데이터셋으로 행동 복제를 학습합니다. | core-data-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-aloha-01](lessons/core-aloha-01.md) | 양팔 ALOHA 모델을 실행하고 ACT 형식의 batch를 만듭니다. | core-data-01, core-il-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-vla-01](lessons/core-vla-01.md) | 명시적인 모의 VLA 프로토콜을 장치 없이 왕복시킵니다. | core-data-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-ros-01](lessons/sim-ros-01.md) | 격리된 도메인에서 실제 ROS 토픽·서비스·액션·TF를 교환합니다. | core-00, core-02 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-ros-02](lessons/sim-ros-02.md) | 측정된 MuJoCo 상태를 ROS JointState 메시지로 연결합니다. | core-04, sim-ros-01 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-ros-03](lessons/sim-ros-03.md) | 실제 ROS 메시지를 기록하고 rosbag2 데이터베이스를 재생합니다. | sim-ros-02 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-ros-04](lessons/sim-ros-04.md) | 시뮬레이션과 ROS의 공통 reset·observe·act·close 인터페이스를 확인합니다. | sim-ros-02 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-g1-01](lessons/sim-g1-01.md) | G1 모션 모방 PPO를 학습하고 저장 checkpoint를 평가합니다. | core-g1-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-wuji-01](lessons/sim-wuji-01.md) | 고정된 Wuji MJLab 재배향 과제를 학습·평가합니다. | core-wuji-02, core-rl-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-vla-01](lessons/sim-vla-01.md) | 준비된 SmolVLA 가중치를 실제 로컬 데이터로 미세조정하고 추론 서버를 실행합니다. | core-vla-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-vla-02](lessons/sim-vla-02.md) | 명시적으로 설정한 선택형 원격 정책 응답을 검증합니다. | sim-vla-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-isaac-01](lessons/sim-isaac-01.md) | 고정된 공개 Wuji URDF를 실제 Isaac articulation으로 가져옵니다. | core-04 | ubuntu-24.04-x86_64; isaac-sim | `implemented` |
| [sim-isaac-02](lessons/sim-isaac-02.md) | 조명 세기를 바꾸며 RGB·깊이 관측을 측정합니다. | sim-isaac-01 | ubuntu-24.04-x86_64; isaac-sim | `implemented` |
| [sim-cross-01](lessons/sim-cross-01.md) | 같은 초기 상태와 적용 힘으로 실제 엔진 두 개를 비교한다. | core-fr3-08, sim-isaac-01 | ubuntu-24.04-x86_64; isaac-sim | `implemented` |
| [sim-deploy-01](lessons/sim-deploy-01.md) | 패키징은 프로세스 경계를 넘어 학습 숫자의 뜻을 보존한다. | core-fr3-08 | macos-arm64, linux-x86_64; python-3.12 | `implemented` |
| [sim-enlight-01](lessons/sim-enlight-01.md) | Fake hardware는 통신과 실물 권한을 분리한다. | core-enlight-01, sim-ros-01 | ubuntu-24.04-x86_64; ros2-jazzy | `implemented` |
| [sim-enlight-02](lessons/sim-enlight-02.md) | 이 후보는 학습 정책이 아니라 알려진 제어기다. | core-enlight-02, sim-deploy-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [sim-wuji-02](lessons/sim-wuji-02.md) | 정교 조작 후보는 완료된 실제 `sim-wuji-01` 체크포인트를 읽고 동일한 고정 벤더 과제를 play 모드로 구성해 평가한 뒤 정확한 정책 바이트를 복사한다. | sim-wuji-01, sim-deploy-01 | ubuntu-24.04-x86_64; nvidia-cuda | `implemented` |
| [hw-common-01](lessons/hw-common-01.md) | 추론 sink는 출력 경계를 드러내며 정책을 실행한다. | sim-deploy-01 | macos-arm64, linux-x86_64; python-3.12 | `implemented` |
| [hw-common-02](lessons/hw-common-02.md) | 읽기 전용 스냅샷은 관측 상태가 일관되고 최신이며 비활성인지 답한다. | hw-common-01 | ubuntu-24.04-x86_64; robot-runtime, isolated-network | `scaffolded` |
| [hw-fr3-01](lessons/hw-fr3-01.md) | FR3 시뮬레이션·오프라인 재생은 소프트웨어 동작을 확인하며 실물의 관절 순서·부호·단위·정지 경계는 읽기 전용 상태로 별도 확인해야 한다. | hw-common-02, core-fr3-06 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, fr3-hardware, read-only-preflight-fr3 | `scaffolded` |
| [hw-wuji-01](lessons/hw-wuji-01.md) | 실물 촉각에는 접촉 모양 숫자뿐 아니라 센서 식별·보정이 필요하다. | hw-common-02, core-wuji-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, wuji-hardware, read-only-preflight-wuji | `scaffolded` |
| [hw-wuji-02](lessons/hw-wuji-02.md) | 벤더 시뮬레이션 과제에서 평가한 정교 조작 체크포인트는 후보다. | hw-wuji-01, sim-wuji-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, wuji-hardware, read-only-preflight-wuji | `scaffolded` |
| [hw-enlight-01](lessons/hw-enlight-01.md) | Enlight 읽기 전용 준비는 MJCF 라벨이 아니라 물리 제어기 식별에서 시작한다. | hw-common-02, sim-enlight-01 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-02](lessons/hw-enlight-02.md) | 시스템 식별은 어떤 모델 파라미터가 측정 운동·힘을 설명하는지 묻는다. | hw-enlight-01, core-enlight-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-03](lessons/hw-enlight-03.md) | 접촉 과제 shadow는 구동 권한 없이 후보 해석과 읽기 전용 장치 관측을 비교한다. | hw-enlight-01, sim-enlight-02 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-wuji-01](lessons/hw-enlight-wuji-01.md) | 팔과 손 결합에는 동기화·정지 경계가 추가되며 개별 배지 두 개가 통합 시스템을 증명하지 않는다. | hw-enlight-01, hw-wuji-01 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight, wuji-hardware, read-only-preflight-wuji | `scaffolded` |
| [core-fr3-09](lessons/core-fr3-09.md) | 관절 궤적과 직교 좌표 궤적은 다른 질문이다. | core-fr3-06 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-fr3-10](lessons/core-fr3-10.md) | 행동 복제는 FR3 자체 MuJoCo 환경에서 생성한 시연으로 관측·행동 대응을 배운다. | core-fr3-09 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-fr3-01](lessons/sim-fr3-01.md) | 관절 궤적과 직교 좌표 궤적은 다른 질문이다. | core-fr3-09 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-fr3-02](lessons/sim-fr3-02.md) | 행동 복제는 FR3 자체 PhysX 환경에서 생성한 시연으로 관측·행동 대응을 배운다. | sim-fr3-01, core-fr3-10 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-fr3-03](lessons/sim-fr3-03.md) | PPO는 미리 만든 보상 숫자가 아니라 실제 PhysX 롤아웃으로 FR3 정책을 조정한다. | sim-fr3-02, core-fr3-08 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-fr3-04](lessons/sim-fr3-04.md) | 완료한 두 실행에서 목표 배열·초기 자세·월드 좌표계·제어 주기를 일치시킨 뒤 TCP 오차 RMS 차이, 관절 오차와 측정 접촉력을 비교합니다. 값이 다를 때 import·구동기·물리 엔진 원인을 구분하며 실물 안전성을 추론하지 않습니다. | sim-fr3-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-03](lessons/core-enlight-03.md) | 관절 궤적과 직교 좌표 궤적은 다른 질문이다. | core-enlight-02 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-04](lessons/core-enlight-04.md) | 행동 복제는 Enlight 자체 MuJoCo 환경에서 생성한 시연으로 관측·행동 대응을 배운다. | core-enlight-03 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [core-enlight-05](lessons/core-enlight-05.md) | PPO는 미리 만든 보상 숫자가 아니라 실제 MuJoCo 롤아웃으로 Enlight 정책을 조정한다. | core-enlight-04, core-rl-01 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-enlight-03](lessons/sim-enlight-03.md) | 관절 궤적과 직교 좌표 궤적은 다른 질문이다. | core-enlight-03 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-enlight-04](lessons/sim-enlight-04.md) | 행동 복제는 Enlight 자체 PhysX 환경에서 생성한 시연으로 관측·행동 대응을 배운다. | sim-enlight-03, core-enlight-04 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [sim-enlight-05](lessons/sim-enlight-05.md) | PPO는 미리 만든 보상 숫자가 아니라 실제 PhysX 롤아웃으로 Enlight 정책을 조정한다. | sim-enlight-04, core-enlight-05 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [core-shadow-01](lessons/core-shadow-01.md) | 입문은 손목을 고정하고 손가락 하나를 움직인 뒤 공유 손가락 시너지로 닫고 연다. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-shadow-01](lessons/sim-shadow-01.md) | PhysX 입문은 가져온 Shadow의 관절 이름·드라이브 의미·결합·실제 물체 접촉을 보존해야 한다. | core-shadow-01 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [core-stretch3-01](lessons/core-stretch3-01.md) | 이동형 매니퓰레이터는 베이스와 팔을 함께 써 도구 오차를 줄일 수 있다. | core-04 | macos-arm64, linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-stretch3-01](lessons/sim-stretch3-01.md) | PhysX 가져오기 뒤 Stretch는 자유 베이스와 이름 있는 바퀴·리프트·신축 관절 제어를 보존해야 한다. | core-stretch3-01 | ubuntu-24.04-x86_64; python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda | `implemented` |
| [hw-enlight-04](lessons/hw-enlight-04.md) | 정확한 행동 카드는 검토한 장치·행동 하나를 최신 상태·한도·일회 승인에 연결한다. | hw-enlight-02, sim-enlight-05 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-05](lessons/hw-enlight-05.md) | 프로브의 툴 좌표계·하중·허용력·평면 보정을 검토해야 합니다. 학습 정책 토크를 실물에 직접 보내지 않습니다. 검증한 별도 힘 제어기가 필요합니다. | hw-enlight-04 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [hw-enlight-06](lessons/hw-enlight-06.md) | 집기·이동·놓기에는 폭 기반 그리퍼 계약·검증된 장착/도구/하중·과제별 정지/복구가 필요하다. | hw-enlight-04 | ubuntu-24.04-x86_64; robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight | `scaffolded` |
| [sim-teleop-01](lessons/sim-teleop-01.md) | 읽기 전용 입력 검증에는 실제 Quest·MANUS·VIVE 식별·펌웨어/SDK 호환·보정·동시 스트림 측정이 필요하다. | core-teleop-01 | linux-x86_64; python-3.12, numpy, mujoco | `scaffolded` |
| [sim-teleop-02](lessons/sim-teleop-02.md) | 공간 정합은 명시적인 변환 체인이며 자세 배열 복사가 아니다. | core-teleop-01 | linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
| [sim-enlight-06](lessons/sim-enlight-06.md) | 수집은 시뮬레이션 데이터 루프를 잇는다. | core-enlight-05, sim-teleop-02 | linux-x86_64; python-3.12, numpy, mujoco | `implemented` |
<!-- pal:goals:end -->
