<!-- pal:language:start -->
<p align="right">
  <a href="paths.md" lang="ko">한국어</a> | <a href="../en/paths.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# 로봇 학습 경로

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
