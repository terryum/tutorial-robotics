<!-- pal:language:start -->
<p align="right">
  <a href="equipment.md" lang="ko">한국어</a> | <a href="../en/equipment.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 장비와 실행 환경

장비 이름이 아닌 실제 역량으로 실행 위치를 선택합니다. WS1·WS2라는 이름만으로 Ubuntu·ROS·CUDA·Isaac·로봇 런타임이 준비되었다고 판단하지 않습니다. 어느 워크스테이션이든 검증된 역량이 있으면 첫 수업부터 시작할 수 있습니다.

## 맥북에서 독립적으로 배우는 범위

macOS arm64에서 Core 33개와 `sim-deploy-01`, 오프라인 명령 차단 수신기 `hw-common-01`을 포함한 35개 수업을 실행 대상으로 삼습니다. Python 3.12·NumPy·MuJoCo와 고정된 공개 모델 등 각 수업의 역량이 실제로 있어야 합니다. Core 학습도 추가 의존성이 없다는 뜻은 아닙니다. 학습 상태와 실행 근거는 무시되는 `.local/`에 보존합니다.

`sim-fr3-04`는 macOS에서 분석할 수 있지만 독립 실행 대상은 아닙니다. 먼저 별도 호스트에서 실제 PhysX 근거를 생산하고 같은 목표·초기 자세·월드 좌표계·제어 주기로 맞춘 MuJoCo 근거와 비교해야 합니다. MuJoCo 결과를 PhysX 결과로 대체할 수 없습니다.

## 원격 워크스테이션으로 옮기는 시점

| 작업 | 필요한 실제 역량 | 확인할 근거 |
|---|---|---|
| 공통 기초·Core 제어·학습 | Python 3.12, 수업별 라이브러리와 고정 모델 | 산출물 수치와 로컬 check |
| ROS 수업 | 지원 Ubuntu/ROS 환경, 메시지·서비스 런타임 | 토픽·시간·QoS·재생 기록 |
| GPU PPO·VLA | 수업별 CUDA·mjlab/학습·정책 서버 | 실제 실행·평가 산출물 |
| Isaac/PhysX | 지원 Ubuntu, NVIDIA CUDA, Isaac Sim와 호환 모델 | 실제 PhysX 관측·렌더링·결합 검사 |
| 실물 준비 | 격리 네트워크·장비 식별·읽기 전용 점검 | 모델·도구·하중·한계·정지·실행 카드 |

[맥북→WS 원격 개발 안내](setup/remote-development/index.md)는 연결과 재개 방법을 설명합니다. 가상환경을 복사하지 말고 각 호스트에서 잠금 환경을 준비합니다. GPU·실물 근거가 없으면 `capability-unavailable` 또는 `reader_test_required` 상태를 유지합니다. 배지는 공유 공개 검증 상태이며 현재 호스트 실행 근거와 별개입니다.

## 배포와 실물의 경계

전체 72개는 Core 33개·Sim 27개·Hardware 12개입니다. Hardware 중 하나는 오프라인 sink이고 나머지 11개는 `scaffolded`입니다. 문서·시뮬레이션·정책 평가가 물리 동작을 승인하지 않습니다. 읽기 전용부터 시작하고 새로운 정확한 동작마다 별도 승인을 받아야 합니다. [안전 규칙](../07_SAFETY.md)과 [배포·실물 개념](concepts/deployment-hardware.md)을 읽으세요.

[전체 수업별 플랫폼·역량·상태](lessons.md) · [공개 검증 보고](../verification/robot-paths-2026-11-08.md)

## 장비가 늘어나는 학습 순서

[노트북 → GPU → 선택형 수집 장비 → 마지막 실물](equipment-stages.md) 순서로 읽으세요. [NVIDIA 경험 워크북](nvidia-ecosystem.md)은 Isaac Sim·Lab·Teleop/Capture·GR00T·ROS/배포를 실습과 검증 산출물로 연결합니다. XR·그리퍼·UMI는 필요한 후반 과제에서만 검토합니다.
