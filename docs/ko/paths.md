<!-- pal:language:start -->
<p align="right">
  <a href="paths.md" lang="ko">한국어</a> | <a href="../en/paths.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 로봇 학습 경로

환경 준비가 끝나면 경로도 Codex/Claude Code에 프롬프트로 선택합니다.

```text
매니퓰레이터 튜토리얼을 내 진도를 보존하면서 실행 가능한 수업 하나씩 안내해줘.
```

다른 경로는 “로봇 손 튜토리얼을 안내해줘.” 또는 “이동형 로봇 튜토리얼을 안내해줘.”라고 요청합니다. 에이전트가 경로·저장 상태를 읽고 아래의 참조 명령을 처리하며, 수업 하나 뒤에 멈춥니다. 독자가 직접 `pal` 명령을 입력할 필요는 없습니다.

기존 수업 ID·별칭·완료 이력은 보존합니다. `curriculum/paths.json`에서 세 경로를 따로 정의합니다. 경로 선택 시 모든 필수 단계를 포함하며, 기존 경로 미선택 과정은 `--through`와 선택 수업 필터를 계속 사용합니다.

| 경로 | 시작 모델 | 필수 흐름 | 후속 경로 |
|---|---|---|---|
| manipulator | FR3 | MuJoCo 관절·TCP → PhysX → PPO·BC → 동일 조건 엔진 비교 → Enlight에서 별도 학습 → 실물 준비 | 프로브 평면 힘 제어, 그리퍼 집기·이동·놓기 각각 툴 검토 |
| dexterous-hand | Shadow Hand | MuJoCo 개별 관절·시너지·접촉 → PhysX | Wuji Hand 2 Beta 2 → Enlight 결합 |
| mobile-manipulator | Stretch 3 | MuJoCo 베이스·팔·협응 움직임 → PhysX | 비공개 Friday provider, 공개 인터페이스는 base/arm/gripper 그룹 |

```bash
pal course paths --json
pal course init --path manipulator --json
pal course next --json
pal course summary --json
pal course pause --json
pal course resume --json
pal lesson run core-fr3-09 --resume-from BASE --json
```

“매니퓰레이터 튜토리얼 실행해줘”라고 요청하면 기존 완료 이력을 보존하며 경로 선택 → 저장 상태 확인 → 현재 언어의 GitHub 수업 열기 → 한 수업의 기준·비교 실행 → 수치 설명·검증 → 저장 순서로 진행합니다. 다음 수업은 계속 요청할 때 실행합니다. 필수 Isaac 수업이 막히면 필요한 호스트·환경을 안내하며 건너뛰어 완료 처리하지 않습니다.

중단은 설명·실행·매개변수·비교 기록을 보존합니다. 재개는 저장 단계와 다음 행동을 먼저 반환하고 로봇 명령을 보내지 않습니다. 짧은 시뮬레이션은 새 run에서 시작하고, 완료된 산출물은 검토를 이어갈 수 있습니다. 피드백·개인 진도 동기화의 기존 경계도 유지합니다.

## 학습 중단·재개와 호스트 이동

긴 학습은 짧은 수업과 별도로 실행합니다. FR3 가중치를 Enlight 후보로 쓰지 말고 해당 모델에서 다시 학습·평가하세요. 위치 증분 정책은 시뮬레이션용이며 접촉은 별도 검증 제어기가 필요합니다.

```bash
pal train run --model fr3 --algorithm bc --epochs 64 --output-dir .local/train/fr3-bc --json
pal train run --model fr3 --algorithm bc --epochs 128 --resume-from .local/train/fr3-bc --output-dir .local/train/fr3-bc-resumed --json
pal train export --source .local/train/fr3-bc-resumed --destination .local/fr3-training.json --json
# 이 파일만 다른 호스트로 옮긴 뒤:
pal train import --source .local/fr3-training.json --destination .local/imported-fr3 --json
```

`--algorithm ppo`는 실제 팔 rollout을 사용합니다. 업데이트/에포크 경계마다 모델·optimizer·고정 정규화·RNG·진도를 원자적으로 저장합니다. SIGINT/SIGTERM은 다음 경계에서 중단합니다. 강제 종료 후 디렉터리 재개는 마지막 정상 체크포인트를 찾습니다. 코드·모델·데이터·엔진·환경 lock·seed·학습률이 바뀌면 재개를 거부하며 총 에포크 증가는 허용합니다. export는 해시가 있는 학습 상태·시연 데이터만 포함하고 장비 설정·자격증명·실물 승인·개인 진도는 포함하지 않습니다. 대상 호스트도 같은 소스와 소프트웨어 lock을 사용해야 합니다.

BC는 에피소드 단위로 20/5/5를 학습/검증/평가로 분리합니다. 별도 목표 20개에서 16개 이상이 10 mm 이내를 연속 10 제어 단계 유지해야 성능 게이트를 통과합니다. optimizer 검사가 통과해도 `evaluation.json`을 확인하세요. 짧은 BC/PPO는 이 게이트에 실패할 수 있습니다. 실물 허용 오차로 사용하지 않습니다.

## 모델·그리퍼·실물 게이트

FR3의 기존 pin은 유지합니다. Shadow Hand·Stretch 3·Robotiq 2F-85는 별도 Menagerie 커밋·파일 해시·모델 라이선스로 고정합니다. Isaac은 고정 소스를 실행 폴더의 USD로 변환하고 PhysX를 사용합니다. 관절·구동기·연동·자유 베이스·접촉·관측·렌더링을 실제 GPU에서 검증해야 합니다. 연동 관계가 확인되지 않으면 차단합니다. MuJoCo 계산으로 PhysX 검증을 대체하지 않습니다.

그리퍼 시뮬레이션 기준은 Robotiq 2F-85입니다. [제조사 Isaac 자산](https://github.com/robotiq/isaacsim_assets)은 별도 manifest에 고정합니다. PhysX variant를 사용하며 Newton/MuJoCo-Warp를 두 엔진 비교로 쓰지 않습니다. 교체 제품은 재사용 라이선스, 충돌·관성, mimic·폐루프·개폐 폭 변환, 상태·timeout·정지 API, 플랜지·전원·통신·하중 호환성을 확인해야 합니다. 공개 `Gripper` protocol로 인터페이스를 분리하며 구매는 포함하지 않습니다.

Enlight 실물 기준은 RDK 2.1 / v3E.1입니다. description의 v4 표기와 실물 호환성은 미확인 게이트입니다. Elements 검토 → 오프라인 재생 → sink → 읽기 전용 → live shadow → torque-disabled replay → 정확한 일회성 실행 카드 순으로 진행합니다. 일반 수업은 실물 명령을 보내지 않습니다. run-card executor에는 제조사 연결·enable API가 없으며 현장 어댑터에서 watchdog·timeout·정지·장비 식별·한계·툴 하중을 검증해야 합니다. 프로브·그리퍼가 없거나 검토되지 않으면 해당 실습은 대기합니다. [안전 지침](../07_SAFETY.md)을 따릅니다.

설치된 Isaac 호스트에서는 `pal train run --engine physx --model fr3 --algorithm bc --epochs 64 --output-dir .local/train/physx-fr3 --json`을 사용합니다. 동일 엔진에서만 체크포인트를 재개합니다. [환경별 검증 결과](../verification/robot-paths-2026-11-08.md)를 확인하세요.

## 경로를 읽는 방법

공통 기초 다섯 수업에서 재현성·모델·상태·렌더링을 익힙니다. 매니퓰레이터는 관절/좌표계 이해에서 제어·학습·독립 평가로, 손 경로는 관절/시너지에서 접촉으로, 이동형 경로는 베이스와 팔의 좌표 합성으로 이어집니다. 각 수업의 선행 조건을 먼저 읽고 필요한 [개념 장](index.md#공통-개념-11장)으로 돌아오세요.

Mac→WS 전환은 첫 필수 PhysX·ROS·GPU 수업의 실제 역량 요구에서 일어납니다. 경로를 끝내기 위해 필수 Isaac 수업을 건너뛸 수 없습니다. 실물 단계는 별도 도구·하중·안전 검토와 새로운 실행별 승인을 요구합니다. [장비 안내](equipment.md)를 먼저 확인하세요.

아래는 `curriculum/paths.json`의 필수 순서입니다. 이는 카탈로그 전체 순서와 다를 수 있습니다. 실제 선택은 `pal course next --json`으로 확인하세요.

### manipulator

[core-00](lessons/core-00.md) → [core-01](lessons/core-01.md) → [core-02](lessons/core-02.md) → [core-03](lessons/core-03.md) → [core-04](lessons/core-04.md) → [core-fr3-01](lessons/core-fr3-01.md) → [core-fr3-02](lessons/core-fr3-02.md) → [core-fr3-03](lessons/core-fr3-03.md) → [core-fr3-04](lessons/core-fr3-04.md) → [core-fr3-05](lessons/core-fr3-05.md) → [core-fr3-06](lessons/core-fr3-06.md) → [core-fr3-09](lessons/core-fr3-09.md) → [sim-fr3-01](lessons/sim-fr3-01.md) → [core-rl-01](lessons/core-rl-01.md) → [core-fr3-07](lessons/core-fr3-07.md) → [core-fr3-08](lessons/core-fr3-08.md) → [core-fr3-10](lessons/core-fr3-10.md) → [sim-fr3-02](lessons/sim-fr3-02.md) → [sim-fr3-03](lessons/sim-fr3-03.md) → [sim-fr3-04](lessons/sim-fr3-04.md) → [core-enlight-01](lessons/core-enlight-01.md) → [core-enlight-02](lessons/core-enlight-02.md) → [core-enlight-03](lessons/core-enlight-03.md) → [core-enlight-04](lessons/core-enlight-04.md) → [core-enlight-05](lessons/core-enlight-05.md) → [sim-enlight-03](lessons/sim-enlight-03.md) → [sim-enlight-04](lessons/sim-enlight-04.md) → [sim-enlight-05](lessons/sim-enlight-05.md) → [sim-deploy-01](lessons/sim-deploy-01.md) → [hw-common-01](lessons/hw-common-01.md) → [hw-common-02](lessons/hw-common-02.md) → [sim-ros-01](lessons/sim-ros-01.md) → [sim-enlight-01](lessons/sim-enlight-01.md) → [hw-enlight-01](lessons/hw-enlight-01.md) → [hw-enlight-02](lessons/hw-enlight-02.md) → [hw-enlight-04](lessons/hw-enlight-04.md) → [hw-enlight-05](lessons/hw-enlight-05.md) → [hw-enlight-06](lessons/hw-enlight-06.md)

### dexterous-hand

[core-00](lessons/core-00.md) → [core-01](lessons/core-01.md) → [core-02](lessons/core-02.md) → [core-03](lessons/core-03.md) → [core-04](lessons/core-04.md) → [core-shadow-01](lessons/core-shadow-01.md) → [sim-shadow-01](lessons/sim-shadow-01.md)

### mobile-manipulator

[core-00](lessons/core-00.md) → [core-01](lessons/core-01.md) → [core-02](lessons/core-02.md) → [core-03](lessons/core-03.md) → [core-04](lessons/core-04.md) → [core-stretch3-01](lessons/core-stretch3-01.md) → [sim-stretch3-01](lessons/sim-stretch3-01.md)


## 장비가 늘어나는 학습 순서

[노트북 → GPU → 선택형 수집 장비 → 마지막 실물](equipment-stages.md) 순서로 읽으세요. [NVIDIA 경험 워크북](nvidia-ecosystem.md)은 Isaac Sim·Lab·Teleop/Capture·GR00T·ROS/배포를 실습과 검증 산출물로 연결합니다. XR·그리퍼·UMI는 필요한 후반 과제에서만 검토합니다.
