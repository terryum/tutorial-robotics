<!-- pal:language:start -->
<p align="right">
  <a href="nvidia-ecosystem.md" lang="ko">한국어</a> | <a href="../en/nvidia-ecosystem.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# NVIDIA 피지컬 AI 경험 워크북

**장면 → 물리/센서 → 시연 → 정책 → 독립 평가 → 배포 후보**를 하나의 근거 흐름으로 경험합니다. 로봇이나 헤드셋 없이 시작합니다. 이 워크북은 카탈로그 수업과 추가 NVIDIA 공식 실습을 연결하며, 외부 실습을 카탈로그 완료로 자동 처리하지 않습니다. 먼저 [장비 단계](equipment-stages.md)와 [PhysX 개념](concepts/physx.md)을 읽으세요.

## 지금 사용하는 계층 구분

| 계층 | 학습자가 바꾸는 것 | 생산하는 근거 | 저장소 상태 |
|---|---|---|---|
| Isaac Sim / OpenUSD / PhysX | 자산·구동기·접촉·카메라·조명 | USD 출처·실제 물리 관측·영상 | 자산/제어/센서 수업, 실제 GPU 실행 필요 |
| Isaac Lab | 병렬 과제·보상·리셋·학습/평가 | 설정·체크포인트·시드·보류 rollout | 별도 고정 환경과 공식 확장 실습, 모든 GPU 수업이 Lab은 아님 |
| Isaac Teleop / Isaac Capture / CloudXR | 입력·리타게팅·세션·기록 | 추적/수신 시각·변환·재생 | 카탈로그는 합성 MuJoCo 계약, 실제 장비 입력은 미검증 |
| GR00T / VLA | 데이터 모달리티/행동 계약·모델별 적응 | 데이터 매니페스트·가중치 식별·추론/평가 | 고정 GR00T 프로필, import smoke는 과제 성능이 아님 |
| ROS 2 / Isaac ROS·배포 | 시점 있는 메시지·정책 인터페이스·runtime 게이트 | 메시지/지연·후보 해시·오프라인 sink | 일반 ROS 수업 있음, Isaac ROS 가속 패키지·Jetson 검증은 별도 |

공식 출처: [Isaac Sim 문서](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html), [Isaac Lab](https://developer.nvidia.com/isaac/lab), [Isaac Capture](https://nvidia.github.io/IsaacCapture/main/), [GR00T](https://developer.nvidia.com/isaac/gr00t). 최신 문서는 참고 자료이며 설치 환경을 교체하라는 지시가 아닙니다.

## 0. 재현 가능한 환경 계획 기록

저장소의 활성화된 Core 환경에서 설치 없이 확인합니다.

```bash
pal stack plan --profile isaac-modern --json
pal stack plan --profile groot --json
pal stack plan --profile pi05 --json
```

[stack-lock.json](../../setup/stack-lock.json)과 [두 스택 전략](../../setup/08_ISAAC_STACKS.md)을 읽습니다. 벤더 호환 Isaac과 최신 Isaac Lab 환경을 격리합니다. 네이티브 OS·GPU/드라이버/VRAM·Python·소스 리비전·확장·라이선스 동의를 별도로 기록합니다. 교재 읽기 때문에 환경 적용이나 가중치 다운로드를 시작하지 않습니다. 런타임이 없으면 사용 불가 상태를 유지합니다.

확인한 공식 [Teleop quick start](https://nvidia.github.io/IsaacCapture/main/teleop/quick_start.html)는 현재 `isaaccapture`를 사용하며 `isaacteleop`에서 이름이 바뀌었음을 설명합니다. 구형 설치와 패키지/import·예제가 다를 수 있습니다. 새 명령은 호환되는 체크아웃과 패키지를 함께 고정한 별도 환경에서 사용합니다. [Lab/Sim 연동 페이지](https://nvidia.github.io/IsaacCapture/main/integrations/isaac_lab_sim.html)는 준비 중으로 표시되어 있으므로 이 저장소에서 검증한 절차로 취급하지 않습니다.

## 1. 로봇을 가져오고 물리를 점검

준비된 호스트에서 [sim-isaac-01](lessons/sim-isaac-01.md) 후 [sim-fr3-01](lessons/sim-fr3-01.md) 또는 [sim-enlight-03](lessons/sim-enlight-03.md)을 진행합니다. 관절 이름·축·한계·충돌체·관성·구동기·텐던/mimic을 확인합니다. 소스 해시/가져오기 옵션과 파생 USD는 실행 경로에 저장합니다. 문서의 기준 실행 후 실제 `physx-observations.json`과 `isaac-frame.png`를 검사합니다.

한 변수 실습: 문서가 지원하는 제어 매개변수 하나 또는 별도로 보존한 공식 예제의 구동기 설정 하나만 바꾸고 자세/목표/주기를 고정합니다. 명령과 측정 관절/TCP 상태를 구별합니다. 빈 화면이 아니라고 관절 대응·접촉이 맞는 것은 아닙니다.

이해 확인: 외형은 맞지만 물리가 틀릴 수 있는 속성 세 가지는? 관성·구동 의미·충돌/결합 등이 있습니다.

## 2. RTX 카메라와 합성 관측 경험

[sim-isaac-02](lessons/sim-isaac-02.md)를 따릅니다. RGB와 사용 가능한 주석/깊이 출력에 영상 크기·카메라 내부/외부 매개변수·단위·촬영 시점을 연결합니다. 전경 구도와 라벨을 확인하고 다른 미리보기 영상을 대신 쓰지 않습니다. 확장 실습은 설치 릴리스에 맞는 공식 센서/무작위화 예제로 진행합니다.

장면/시드를 고정하고 조명 또는 카메라 자세 하나만 바꿉니다. 가시성·라벨 정합을 비교하고 정책이 받는 관측 변화를 설명합니다. 픽셀 변화가 정책 강건성 향상을 뜻하지는 않습니다. API 이관이 있으므로 확장/API 버전을 기록합니다.

## 3. 학습 규모를 늘리기 전 엔진 비교

문서의 동일 조건 계약으로 [core-fr3-09](lessons/core-fr3-09.md)와 실제 [sim-fr3-01](lessons/sim-fr3-01.md)을 실행한 뒤 [sim-fr3-04](lessons/sim-fr3-04.md)를 진행합니다. 스칼라 오차 차이를 읽기 전에 목표·초기 자세·좌표계·주기를 확인합니다. 같은 오차 크기가 반대 방향 위치 오차를 숨길 수 있습니다. Newton이나 MuJoCo-Warp는 별도 백엔드 선택이며 독립 PhysX 근거로 바꾸어 부르지 않습니다.

## 4. Isaac Lab에서 학습과 독립 평가

격리한 Lab 환경에서 공식 기본 예제가 통과한 뒤 설치 릴리스의 과제 목록과 [Isaac Lab 학습 자료](https://developer.nvidia.com/isaac/lab)를 사용합니다. 지원되는 작은 시뮬레이션 과제로 시작합니다. 과제 ID·관측/행동 크기·보상 항·리셋/종료·환경 수·시드·설정·체크포인트를 저장합니다. 별도 평가에서 보류 조건으로 정책을 재생합니다.

한 변수 실험: 학습 예산의 정의를 명시한 채 환경 수만 늘립니다. 초당 전이 수·메모리·평가 return을 비교합니다. 실제 시간 속도와 표본 효율은 다릅니다. 이 외부 Lab 실습은 기존 MJLab 기반 G1/Wuji 수업과 다르며 검증된 FR3/Enlight Lab 과제가 자동으로 되지 않습니다. 새 로봇/과제에는 별도 대응·검증이 필요합니다. 저장소의 구현된 팔 흐름은 [PhysX PPO](lessons/sim-fr3-03.md)를 따릅니다.

## 5. XR 장비 없이 먼저 시뮬레이션 목표 조작

합성 계약 [core-teleop-01](lessons/core-teleop-01.md)과 오프라인 [sim-teleop-02](lessons/sim-teleop-02.md)를 먼저 진행합니다. SI 단위·xyzw·좌우 식별·보정·수신 시각·클러치/데드맨·100 ms stale 차단·명시적 로컬 재무장을 확인합니다. 카탈로그 입력은 합성이며 소프트웨어 성공이 사람/장비 검증은 아닙니다.

외부 NVIDIA 실습으로 공식 quick start의 데스크톱 브라우저 에뮬레이터와 터미널 전용 그리퍼 리타게터를 경험합니다. 벤더 설정/동의를 검토한 호환 Capture 별도 환경에서 로봇 transport를 연결하지 않고 사용하는 공식 예제는 다음입니다.

```bash
python -m isaaccapture_examples.teleop.gripper_retargeting_example_simple --duration 20
```

이진 열기/닫기 값을 출력하므로 실물 그리퍼는 필요하지 않습니다. 다른 입력을 고정하고 임계값 바로 아래/위 트리거를 비교합니다. 연속 입력이 왜 이진 출력이 되는지 설명합니다. 소프트웨어 버전과 정상 종료 결과를 보존합니다. 예제는 CloudXR 서비스를 시작하거나 EULA 동의를 요청할 수 있어 선택형 실행 작업이며 자동 교재 생성에 포함되지 않습니다. 데스크톱 에뮬레이터는 Quest 검증이 아닙니다.

## 6. 필요할 때 Quest·MANUS·VIVE 추가

[sim-teleop-01](lessons/sim-teleop-01.md)과 [고정 Ubuntu VR 설정](setup/vr-teleop.md)을 따릅니다. 읽기 전용에서 스트림 하나씩, 그다음 동시 입력을 확인합니다. 헤드셋/컨트롤러·손가락·손목은 별도 신호입니다. 보정 변환과 신선도를 각각 확인하며 SDK 이름·쿼터니언 규약을 혼용하지 않습니다. 최신 [Capture 생태계](https://nvidia.github.io/IsaacCapture/main/overview/ecosystem.html)의 플러그인 지원이 현재 장비/펌웨어 조합을 검증하지는 않습니다.

각 스트림과 동시 입력을 최소 60초 기록하여 주기/최대 공백·유효성·가림·해제·timeout·재연결을 확인합니다. 정지 자세와 알려진 움직임 하나를 비교합니다. 햅틱 출력이나 로봇 명령 transport를 활성화하지 않습니다. 저장소의 Hub/SDK 프로토콜 경계를 보존하며 최신 플러그인이 기록된 불일치를 없애주지는 않습니다. [공개 VR 기록](../verification/vr-teleop-2026-11-13.md)에 실제 사람 입력 통과 근거는 없습니다.

## 7. 수집·증강·학습·평가 연결

[sim-enlight-06](lessons/sim-enlight-06.md)에서 시뮬레이션 카메라/상태/행동 에피소드를 배웁니다. saved/discarded/aborted 출처·해시·에피소드 분리를 확인한 뒤 [BC](lessons/core-enlight-04.md)와 비교합니다. 합성 세 에피소드는 계약 예제이며 실제 학습에 충분한 데이터가 아닙니다.

외부 Isaac Lab Mimic/Teleop 실습은 공식 quick start가 연결한 해당 릴리스 안내를 따릅니다. 시뮬레이션 시연 기록 → 리셋/성공 검증 → 시연 증강 → 학습 → 별도 시드/장면 평가로 진행합니다. 원본과 생성 에피소드의 출처를 분리하고 생성 개수뿐 아니라 수락/거부·보류 과제 성공률을 측정합니다. 다른 로봇의 공식 예제가 Enlight 어댑터가 되지는 않습니다.

GR00T는 고정된 [설치·데이터 인계](../../setup/LATEST_ROBOTICS_UPDATE.md)와 [VLA 개념](concepts/vla.md)을 따릅니다. 영상/상태/언어 모달리티·행동 단위/시간 범위·정규화·로봇 embodiment·가중치/라이선스·에피소드 분리를 확인합니다. 고정 평가에서 적응 또는 추론 변수 하나만 비교합니다. 지연·잘못된 응답·성공률·실패 사례를 분리합니다. `core-vla-01`은 mock이며 import와 배열 크기 일치가 GR00T pick-and-place 성능은 아닙니다. 2지 그리퍼·UMI는 [후반 과제별 선택지](equipment-stages.md)이며 입문 필수품이 아닙니다.

## 8. 후보와 오프라인 runtime으로 마무리

[ROS 수업](lessons/sim-ros-01.md)·[배포 후보](lessons/sim-deploy-01.md)·[오프라인 명령 차단](lessons/hw-common-01.md)으로 정책/상태/영상 시각을 연결합니다. Isaac ROS나 Jetson 확장은 별도 플랫폼/패키지/라이선스·지연 검증이 필요하며 앞선 GPU 경험을 위해 Jetson을 먼저 살 필요는 없습니다. 모델/데이터/환경 해시를 고정하고 재생 목표를 저장 행동 스키마와 비교합니다. 그다음 마지막 실물 준비를 [별도 안전 게이트](../07_SAFETY.md)로 공부합니다.

## 경험을 정확하게 기록

실습마다 입력/설정 리비전·산출물·수치·한 변수 비교·해석·한계·다음을 기록합니다. `passed`·`failed`·`not_run`을 쓰고 계획·설치·소프트웨어 테스트·GPU 실행·사람 입력 검증·실물 검증을 구별합니다. 이 워크북은 문서로 저술·검사했으며 교재 제작 중 위 외부 NVIDIA 런타임을 실행했다는 주장이 아닙니다.
