<!-- pal:language:start -->
<p align="right">
  <a href="hw-common-02.md" lang="ko">한국어</a> | <a href="../../en/lessons/hw-common-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-common-02 — 실물 하드웨어 읽기 전용 통합 게이트

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / common` |
| Legacy alias | `T36` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network` |
| Prerequisites | `hw-common-01` |
| Safety | `read-only` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

선행 [개념 장](../concepts/deployment-hardware.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 장비 동작 전에 어떤 읽기 전용 검사가 필요한가?

## Learning goals

읽기 전용 스냅샷은 관측 상태가 일관되고 최신이며 비활성인지 답한다.

장비 동작 전에 어떤 읽기 전용 검사가 필요한가?

## Preflight

장비 검증 전까지 이 수업은 scaffolded / reader_test_required입니다. 오프라인 후보 검증과 공통 읽기 전용 게이트, 해당 로봇의 선행 시뮬레이션을 확인합니다. 장비 이름이나 네트워크 연결만으로 준비됐다고 판단하지 않습니다.

[하드웨어 안전 절차](../../07_SAFETY.md)를 읽고 로컬 snapshot에서 모델·펌웨어 식별, torque-disabled, 오류·E-stop, 관절/힘 한계, 통신 timeout, timestamp 신선도, 격리 네트워크를 확인합니다. 비공개 serial·IP·보정값은 .local/에만 둡니다.

[하드웨어 안전](../../07_SAFETY.md)을 읽는다. 이 장은 근거를 준비하며 장치 동작을 요청·허가하지 않는다.

## Action

정식 명령 `pal lesson run hw-common-02`는 의도적으로 사용할 수 없다. runner는 준비 검사·출력 생성 전에 이 scaffold를 거부한다. 실행하지 않는다.

준비 교재다. 카탈로그·준비 보고서를 확인한다. 현재 runner는 이 scaffold에 `NotImplementedError`를 반환하며 성공 장치 실행을 만들지 않는다. 준비·계약 검사는 실물 실행이나 수업 완료가 아니다.

```bash
pal lesson check hw-common-02 --json
```

## Expected

실물 검증 증거가 없다는 구체적인 사유를 읽습니다. 장비가 준비되면 모델 정체성·상태 수신율·단위/축/관절 순서·신선도와 중단 경로를 읽기 전용으로 먼저 측정해야 합니다.

### 산출물 읽기

이 scaffold는 성공 실행 산출물을 약속하지 않는다. 무시되는 로컬 근거 목록에 정확한 모델·좌우·펌웨어/SDK, `positions_rad`, `position_limits_rad`, `joint_group`, `timestamp`, `previous_timestamp`, `stale_after_s`, `enabled=False`, `error=False`, `estop_ready=True`, `command_authority_count=0`, 네트워크, 독립 stop/watchdog/timeout 시험을 준비한다. `ready`, `errors`, `valid_until_s`는 데이터 검사 결과이며 실행 허가가 아니다. 비공개 장치 식별·보정을 게시하지 않는다.

## How it works

### 직관

읽기 전용 스냅샷은 관측 상태가 일관되고 최신이며 비활성인지 답한다. 명령 권한을 주지 않는다. `preflight`는 외부에서 캡처한 JSON 파일을 읽으며 로봇에 연결하지 않는다. 후속 게이트 전에 정확한 모델·한도 안 유한 관절값·명령 권한 0개·무오류·E-stop 준비·격리 네트워크를 확인한다.

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

[`src/pai_lab/hardware/preflight.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/preflight.py)

`examples/hw-common-02/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

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

[hw-fr3-01](./hw-fr3-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
