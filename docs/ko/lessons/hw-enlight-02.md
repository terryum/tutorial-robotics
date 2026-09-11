# hw-enlight-02 — Enlight 시스템 식별과 MuJoCo 보정

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `T37A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-01, core-enlight-02` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Learning goals

Enlight 시스템 식별과 MuJoCo 보정에 필요한 관측·선행 조건과 실행별 안전 경계를 검토합니다.

## Preflight

장비 검증 전까지 이 수업은 scaffolded / reader_test_required입니다. 오프라인 후보 검증과 공통 읽기 전용 게이트, 해당 로봇의 선행 시뮬레이션을 확인합니다. 장비 이름이나 네트워크 연결만으로 준비됐다고 판단하지 않습니다.

[하드웨어 안전 절차](../../07_SAFETY.md)를 읽고 로컬 snapshot에서 모델·펌웨어 식별, torque-disabled, 오류·E-stop, 관절/힘 한계, 통신 timeout, timestamp 신선도, 격리 네트워크를 확인합니다. 비공개 serial·IP·보정값은 .local/에만 둡니다.

## Action

```bash
pal lesson check hw-enlight-02 --json
pal lesson run hw-enlight-02 --headless --json
```

현재 entrypoint는 실행 가능한 실물 어댑터가 없어 종료 코드 2를 반환해야 합니다. 이는 완료가 아닙니다. 검증을 위해 모의 성공 기록을 만들지 않습니다.

## Expected

실물 검증 증거가 없다는 구체적인 사유를 읽습니다. 장비가 준비되면 모델 정체성·상태 수신율·단위/축/관절 순서·신선도와 중단 경로를 읽기 전용으로 먼저 측정해야 합니다.

## How it works

```text
offline replay → command sink → read-only → live shadow
→ torque-disabled replay → fresh run card → one explicitly approved action
```

각 단계는 이전 단계의 결과를 소비하지만 다음 단계의 동작 권한을 자동 부여하지 않습니다. contact·실물 평가·시스템 식별·통합 장치 작업은 정확한 로봇과 행동에 대한 새로운 승인이 필요합니다. 두 장치 통합 과제는 각각의 읽기 전용 검증을 모두 요구합니다.

## Code connection

`examples/hw-enlight-02/run.py` → `src/pai_lab/lessons/runner.py`;
`src/pai_lab/hardware/preflight.py` checks supplied read-only snapshots.

## Try it

로컬 snapshot 복사본에서 timestamp 하나만 과거로 바꾸고 stale-state 검사가 거부하는지 확인합니다. 실제 컨트롤러의 시간·한계·watchdog를 바꾸지 않습니다. 읽기 전용 검사의 실패를 숨기지 않습니다.

## Recovery

모델 불일치, enable 상태, fault, 오래된 상태, 격리 실패가 있으면 장치로 명령을 보내지 않고 중단합니다. vendor의 E-stop·복구 절차를 따릅니다. 펌웨어 갱신·torque enable·한계 확대·충돌 검사 우회는 자동 실행하지 않습니다.

## Checkpoint

현재 완료 기준은 충족되지 않았습니다. 실제 어댑터 구현과 새 실행 증거, 필요한 개별 승인이 갖춰지기 전에는 이 수업을 완료 처리하지 않습니다. 개인 상태는 .local/, 공유 출판 증거만 state/PUBLISHING.md에 둡니다.

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-03](./hw-enlight-03.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
