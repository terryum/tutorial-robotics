<!-- pal:language:start -->
<p align="right">
  <a href="core-teleop-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-teleop-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-teleop-01 — 양손 입력·클러치·재생

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

헤드셋 구매 없이 양손 데이터 계약을 배운다. 합성 좌우 자세·스위치 이벤트를 `CommandSink`로 보내 에피소드 3개를 저장·재로딩하고 저장·폐기·중단 결과를 구별한다. `provenance=synthetic`는 부수 라벨이 아니라 결과의 일부다. 동기화되지 않은 장치 시계가 아니라 로컬 수신 시계로 최신 여부를 판단한다.

선행 [개념 장](../concepts/data-imitation.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 클러치·타임스탬프·재생은 양손 입력의 의미를 어떻게 보존하는가?

## Learning goals

헤드셋 구매 없이 양손 데이터 계약을 배운다.

클러치·타임스탬프·재생은 양손 입력의 의미를 어떻게 보존하는가?

## Preflight

카탈로그 플랫폼·역량에 맞는 호스트를 사용하며 컴퓨터 이름이 준비를 허가하지 않는다. `core-teleop-01`은 macOS arm64·Linux x86_64를 지원하고 이후 선택 입력·수집 수업은 Linux x86_64다. [VR 준비](../setup/vr-teleop.md), [장비 단계](../equipment-stages.md), [검증 기록](../../verification/vr-teleop-2026-11-13.md)의 합성·실제 구별을 읽는다. 장치·보정·원시 에피소드는 무시되는 `.local/`에 두며 벤더 자동 설치·장치 동의를 뜻하지 않는다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run core-teleop-01 --headless --seed 7 --samples 16 --output-dir .local/runs/core-teleop-01/baseline-01 --json
```

## Expected

실제 장치 검증 보고서가 아니라 합성 재생·수집 근거를 기대한다. 카탈로그 산출물·`experiment.json`·`trace.csv`·`plot.png`·에피소드 매니페스트를 확인한다. 저장 3에피소드와 폐기·중단 기록으로 생명주기·출처를 보존한다. 실제 60초 장치 속도·추적·가림·재연결 검증은 별도 실제 입력 게이트다.

## Observe

기록한 입력과 적용 목표를 따로 확인합니다. 합성 timestamp는 테스트용으로 생성한 시각입니다.

### 산출물 읽기

`experiment.json` → `payload`의 `schema_version=2`, `provenance`, 저장 3·폐기 1·중단 1, 에피소드 `splits`, `command_publishers=0`, `live_input_verified=False`, `watchdog_ns`를 읽는다. 매니페스트는 `frames.jsonl` 해시를 담고 재생은 미저장·손상을 거부한다. Trace는 합성 시간의 수용 bool이며 실물 추적 품질 측정이 아니다. 소스의 프레임 간격은 10 ms다.

## How it works

### 직관

헤드셋 구매 없이 양손 데이터 계약을 배운다. 합성 좌우 자세·스위치 이벤트를 `CommandSink`로 보내 에피소드 3개를 저장·재로딩하고 저장·폐기·중단 결과를 구별한다. `provenance=synthetic`는 부수 라벨이 아니라 결과의 일부다. 동기화되지 않은 장치 시계가 아니라 로컬 수신 시계로 최신 여부를 판단한다.

### 계산과 단위

$$
t_{age}=t_{poll}-t_{receive},\qquad 0\leq t_{age}<100000000\ \mathrm{ns}
$$

자세 7원소는 m 단위 xyz와 무차원 단위 쿼터니언 xyzw이며 이름 있는 손가락 각도는 rad다. sequence·수신 시각은 증가 정수다. 정확히 100 ms에서 hold가 래치된다. 장치 근거가 아닌 계산으로 100,000,000 ns는 0.1 s이며 99,999,999 ns는 경계 아래다.

```python
age_ns = 100_000_000
assert age_ns / 1e9 == 0.1
assert not (0 <= age_ns < 100_000_000)
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/teleop.py)

`examples/core-teleop-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py), [VR 검증 기록](../../verification/vr-teleop-2026-11-13.md)도 읽는다.

## Try it

### 통제된 비교

샘플 수를 고정하고 `variant`만 1→0.8로 바꾼다. 합성 왼손목 x 변위가 바뀌며 100 ms watchdog은 같다. 기록 자세는 바뀌어도 수용 trace는 같을 수 있다. Timeout·재연결·추적 소실 뒤에는 두 스위치의 새 release·로컬 rearm·새 press가 필요하며 자세 도착만으로 제어를 재개하지 않는다.

```bash
pal lesson run core-teleop-01 --headless --seed 7 --samples 16 --variant 0.8 --output-dir .local/runs/core-teleop-01/comparison-01 --json
pal lesson check core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --json
pal lesson check core-teleop-01 --run-dir .local/runs/core-teleop-01/comparison-01 --json
pal lesson compare core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --comparison-run-dir .local/runs/core-teleop-01/comparison-01 --output-dir .local/comparisons/core-teleop-01/comparison-01 --json
```

## Recovery

중단된 에피소드를 보존하고 저장·폐기·중단 상태를 구분합니다. 기존 에피소드를 덮어쓰지 않고 재연결 후에는 로컬 재무장 전 조작을 재개하지 않습니다.

## Checkpoint

### 이해 확인

같은 수용 trace에서 자세가 다를 수 있는가? 그렇다. 수용은 유효성·최신 여부를 검사하며 자세 일치 검사가 아니다. 사람 시연인가? 아니다. provenance·live_input_verified가 이를 명시한다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --comparison-run-dir .local/runs/core-teleop-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-01](./core-fr3-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
