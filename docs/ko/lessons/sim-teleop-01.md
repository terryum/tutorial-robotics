<!-- pal:language:start -->
<p align="right">
  <a href="sim-teleop-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-teleop-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-teleop-01 — Ubuntu VR 설치와 읽기 전용 입력

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / common` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-teleop-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

읽기 전용 입력 검증에는 실제 Quest·MANUS·VIVE 식별·펌웨어/SDK 호환·보정·동시 스트림 측정이 필요하다. Linux Hub 다운로드나 합성 패킷 파싱으로 USB 장치 동작을 증명하지 못한다. 수업은 scaffolded이며 일반 runner는 장치 근거를 만들기 전에 거부한다. 기존 VR 없는 경로와 벤더 환경을 보존한다.

선행 [개념 장](../concepts/data-imitation.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 소프트웨어 프로토콜 검사 이후에도 어떤 실제 입력 근거가 필요한가?

## Learning goals

읽기 전용 입력 검증에는 실제 Quest·MANUS·VIVE 식별·펌웨어/SDK 호환·보정·동시 스트림 측정이 필요하다.

소프트웨어 프로토콜 검사 이후에도 어떤 실제 입력 근거가 필요한가?

## Preflight

카탈로그 플랫폼·역량에 맞는 호스트를 사용하며 컴퓨터 이름이 준비를 허가하지 않는다. `core-teleop-01`은 macOS arm64·Linux x86_64를 지원하고 이후 선택 입력·수집 수업은 Linux x86_64다. [VR 준비](../setup/vr-teleop.md), [장비 단계](../equipment-stages.md), [검증 기록](../../verification/vr-teleop-2026-11-13.md)의 합성·실제 구별을 읽는다. 장치·보정·원시 에피소드는 무시되는 `.local/`에 두며 벤더 자동 설치·장치 동의를 뜻하지 않는다.

## Action

정식 명령 `pal lesson run sim-teleop-01`는 의도적으로 사용할 수 없다. runner는 준비 검사·출력 생성 전에 이 scaffold를 거부한다. 실행하지 않는다.

준비 교재다. 카탈로그·준비 보고서를 확인한다. 현재 runner는 이 scaffold에 `NotImplementedError`를 반환하며 성공 장치 실행을 만들지 않는다. 준비·계약 검사는 실물 실행이나 수업 완료가 아니다.

```bash
pal lesson check sim-teleop-01 --json
```

## Expected

실행은 차단된다. 이 scaffold에서 성공 실행 폴더·수치 장치 근거를 기대하지 않는다.

### 산출물 읽기

스트림별·동시 동작의 속도·최대 간격·추적 유효 비율·가림·좌우·release/재연결·독립 100 ms hold 근거를 준비한다. `rate_report`는 `full_60s`, `rate_hz`, `maximum_gap_ns`, `tracking_valid_ratio`를 계산하며 실제 검증을 주장하려면 실제 순서 있는 수신 기록이어야 한다. 공개 VR 보고서는 실제 장치가 없었다고 명시한다.

## How it works

### 직관

읽기 전용 입력 검증에는 실제 Quest·MANUS·VIVE 식별·펌웨어/SDK 호환·보정·동시 스트림 측정이 필요하다. Linux Hub 다운로드나 합성 패킷 파싱으로 USB 장치 동작을 증명하지 못한다. 수업은 scaffolded이며 일반 runner는 장치 근거를 만들기 전에 거부한다. 기존 VR 없는 경로와 벤더 환경을 보존한다.

### 계산과 단위

$$
f=\frac{N-1}{t_{last}-t_{first}},\qquad g_{max}=\max_i(t_{i+1}-t_i)
$$

단일 출처·좌우의 순서 있는 스트림과 ns를 s로 변환한 로컬 수신 시각을 쓴다. f는 Hz, 최대 간격 g는 s이며 전체 검증 기록은 최소 60 s를 포함해야 한다. 장치 데이터가 아닌 계산으로 60 s의 6001샘플은 100 Hz다. 평균 속도만 보면 긴 소실을 숨길 수 있다.

```python
samples, duration_s = 6001, 60.0
assert (samples - 1) / duration_s == 100.0
```

## Code connection

### 소스 추적

[`src/pai_lab/teleop_sources.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_sources.py)

`examples/sim-teleop-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py), [VR 검증 기록](../../verification/vr-teleop-2026-11-13.md)도 읽는다.

## Try it

### 통제된 비교

종이 비교만 한다. 가상 샘플 시각을 고정하고 추적 유효 플래그 하나만 바꾼다. 평균 속도는 같고 유효 비율만 바뀔 것으로 예측한다. 벤더 설치·EULA 동의·햅틱·실제 장치 작업을 뜻하지 않는다. 합성 속도 보고서를 장치 검증으로 저장하면 안 된다.

## Recovery

실패 준비 기록·중단 에피소드 근거를 보존한다. 식별·최신 여부·추적·비활성/오류/E-stop·격리 네트워크가 실패하면 차단을 유지한다. 재연결에는 새 읽기 전용 확인·해당 로컬 rearm이 필요하며 실물 운동을 재개하지 않는다. 벤더 복구 절차를 따르며 펌웨어·토크·한도·watchdog을 자동 변경하지 않는다. `pal course resume --json`은 저장 학습 상태만 확인한다.

## Checkpoint

### 이해 확인

평균 속도 외에 최대 간격을 보는 이유는? 몰린 샘플이 오래된 구간을 숨길 수 있기 때문이다. 소프트웨어 테스트로 실제 입력 수업이 완료되는가? 아니다. 실제 장치 근거가 필요하다.

준비·미해결 게이트를 로컬에 기록한다. 실제 장치·입력 근거와 해당 실행별 승인이 생기기 전에는 미완료로 유지한다. 실물 명령 없이 여기서 멈춘다.

<!-- pal:navigation:start -->
## Next lesson

[sim-teleop-02](./sim-teleop-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
