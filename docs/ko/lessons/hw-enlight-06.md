<!-- pal:language:start -->
<p align="right">
  <a href="hw-enlight-06.md" lang="ko">한국어</a> | <a href="../../en/lessons/hw-enlight-06.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-06 — Enlight 그리퍼 집기·이동·놓기 준비

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-04` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

이 단계는 장비 증거가 없어 대기 상태입니다. 일반 수업 명령은 실물 명령을 보내지 않습니다.

선행 [개념 장](../concepts/deployment-hardware.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 실물 집기·이동·놓기에서 어떤 도구·하중 검사가 동작을 차단하는가?

## Learning goals

집기·이동·놓기에는 폭 기반 그리퍼 계약·검증된 장착/도구/하중·과제별 정지/복구가 필요하다.

실물 집기·이동·놓기에서 어떤 도구·하중 검사가 동작을 차단하는가?

## Preflight

선행 수업: hw-enlight-04. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

[하드웨어 안전](../../07_SAFETY.md)을 읽는다. 이 장은 근거를 준비하며 장치 동작을 요청·허가하지 않는다.

## Action

정식 명령 `pal lesson run hw-enlight-06`는 의도적으로 사용할 수 없다. runner는 준비 검사·출력 생성 전에 이 scaffold를 거부한다. 실행하지 않는다.

준비 교재다. 카탈로그·준비 보고서를 확인한다. 현재 runner는 이 scaffold에 `NotImplementedError`를 반환하며 성공 장치 실행을 만들지 않는다. 준비·계약 검사는 실물 실행이나 수업 완료가 아니다.

```bash
pal lesson check hw-enlight-06 --json
```

## Expected

실행은 차단된다. 이 scaffold에서 성공 실행 폴더·수치 장치 근거를 기대하지 않는다.

### 산출물 읽기

이 scaffold는 성공 실행 산출물을 약속하지 않는다. 무시되는 로컬 근거 목록에 정확한 모델·좌우·펌웨어/SDK, `positions_rad`, `position_limits_rad`, `joint_group`, `timestamp`, `previous_timestamp`, `stale_after_s`, `enabled=False`, `error=False`, `estop_ready=True`, `command_authority_count=0`, 네트워크, 독립 stop/watchdog/timeout 시험을 준비한다. `ready`, `errors`, `valid_until_s`는 데이터 검사 결과이며 실행 허가가 아니다. 비공개 장치 식별·보정을 게시하지 않는다.

## How it works

### 직관

집기·이동·놓기에는 폭 기반 그리퍼 계약·검증된 장착/도구/하중·과제별 정지/복구가 필요하다. `Gripper`는 벤더 구현 없이 상태·폭/속도/힘 한도/timeout 명령·stop 인터페이스를 정의한다. Robotiq 2F-85는 시뮬레이션 기준이며 Enlight의 전기·기계 호환성을 증명하지 않는다. 프로브 승인이나 팔 관절 카드로 물체에 그리퍼를 닫을 수 없다.

### 계산과 단위

$$
t_{age}=t_{now}-t_{snapshot},\qquad 0\leq t_{age}\leq t_{stale}
$$

시간은 같은 벽시계 도메인의 초 단위다. `preflight`는 추가로 (0,1] s 범위의 유한 stale window와 `previous_timestamp`가 있을 때 증가한 시각을 요구한다. Teleop의 monotonic 100 ms sink와 다른 계약이다. 실물 근거가 아닌 종이 계산에서 나이 0.3 s는 선언한 0.1 s를 초과해 거부된다. 설명 숫자로 장치 한도를 설정하지 않는다.

```python
snapshot_age_s, declared_window_s = 0.3, 0.1
assert not (0 <= snapshot_age_s <= declared_window_s)
```

## Code connection

### 소스 추적

[`src/pai_lab/hardware/gripper.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/gripper.py)

`gripper.py`는 폭·속도·힘 제한·timeout 프로토콜을 정의하며 벤더 제어기나 stale-state preflight를 구현하지 않는다. 종이 신선도 계산의 근거는 [`hardware/preflight.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/preflight.py)다. 얇은 entry point는 `runner.py`로 위임하며 runner는 준비 검사나 측정 출력 전에 이 골격 수업을 거부한다.

## Try it

### 통제된 비교

종이 비교만 한다. 식별·관절값·한도를 고정하고 가상의 스냅샷 나이만 stale window 경계 너머로 늘린다. 거부를 예측하고 없는 장치 근거를 나열한다. 실물 시험·시계/watchdog 변경·완료 영수증 생성을 하지 않는다. 수업 runner는 장치 동작 전에 scaffolded 실행을 거부한다.

## Recovery

실패 준비 기록·중단 에피소드 근거를 보존한다. 식별·최신 여부·추적·비활성/오류/E-stop·격리 네트워크가 실패하면 차단을 유지한다. 재연결에는 새 읽기 전용 확인·해당 로컬 rearm이 필요하며 실물 운동을 재개하지 않는다. 벤더 복구 절차를 따르며 펌웨어·토크·한도·watchdog을 자동 변경하지 않는다. `pal course resume --json`은 저장 학습 상태만 확인한다.

## Checkpoint

### 이해 확인

최신 비활성 스냅샷만으로 움직일 수 없는 이유는? 관측 상태 하나만 검사했으며 명령 전송·행동별 제어기·실물 한도·새 실행별 승인은 별도이기 때문이다. 종이 계산 뒤 수업이 완료되는가? 아니다.

준비·미해결 게이트를 로컬에 기록한다. 실제 장치·입력 근거와 해당 실행별 승인이 생기기 전에는 미완료로 유지한다. 실물 명령 없이 여기서 멈춘다.

<!-- pal:navigation:start -->
## Next lesson

[sim-teleop-01](./sim-teleop-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
