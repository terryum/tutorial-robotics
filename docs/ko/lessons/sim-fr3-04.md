<!-- pal:language:start -->
<p align="right">
  <a href="sim-fr3-04.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-fr3-04.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-fr3-04 — FR3 동일 조건 엔진 증거 비교

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / fr3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `sim-fr3-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

[PhysX 개념](../concepts/physx.md)에서 모델 가져오기와 엔진 비교의 경계를 읽습니다. 이 수업은 이미 완료한 MuJoCo·PhysX 기록을 분석하며 여기서 PhysX를 실행하지 않습니다. “같은 목표를 주었다”는 말이 성립하는지부터 확인합니다.

## Learning goals

완료한 두 실행에서 목표 배열·초기 자세·월드 좌표계·제어 주기를 일치시킨 뒤 TCP 오차 RMS 차이, 관절 오차와 측정 접촉력을 비교합니다. 값이 다를 때 import·구동기·물리 엔진 원인을 구분하며 실물 안전성을 추론하지 않습니다.

## Preflight

카탈로그 선행 수업은 `sim-fr3-01`이며, 실제 소비 코드는 완료된 `core-fr3-09`와 `sim-fr3-01`의 검증된 run을 모두 요구합니다. 공개 [환경 검증](../../verification/robot-paths-2026-11-08.md)에 남은 Isaac/PhysX 범위를 확인합니다. Mac에서 분석 코드를 실행할 수 있다는 사실은 Mac에서 PhysX를 검증했다는 뜻이 아닙니다.

`pal course next --json`과 두 원본 run의 `experiment.json`을 읽습니다. `frame`, `initial_q_rad`, `tcp_targets_m`, `control_dt_s`가 정확히 같아야 하며 표본 수도 일치해야 합니다. PhysX 기록이 없거나 손상되었으면 대체 수치·MuJoCo 재실행으로 채우지 않습니다. 외부 역량·증거가 준비될 때까지 대기합니다.

## Action

두 원본의 완료·해시 검증과 일치 조건을 만족한 경우에만 분석을 실행합니다. 이는 실물 동작이나 GPU 학습 실행이 아닙니다.

```bash
pal lesson run sim-fr3-04 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-fr3-04/baseline-01 --json
```

이 폴더를 BASE로 기록합니다. `previous_run`이 각 수업의 현재 완료 기록을 선택하므로 다른 run을 비교하려면 먼저 어떤 입력이 선택되었는지 `run.json`의 `inputs`와 원본 기록으로 확인합니다. 분석을 위해 개인 진도를 임의로 완료 표시하지 않습니다.

## Expected

`engine-comparison.json`, `trace.csv`, `plot.png`, `experiment.json`, `run.json`을 확인합니다. 이 분석은 정책 학습을 수행하지 않고 `evaluation.json`을 새로 생성하지 않습니다. 원본의 정책 성능 판정이 있더라도 엔진 일치·실물 안전성의 판정과 구분합니다.

현재 검사는 일치 조건과 유한 수치만 확인하며 엔진 차이에 대한 수치 통과 한계를 두지 않습니다. 차이가 작아도 실제 로봇의 허용 오차를 입증하지 않습니다. 카탈로그 badge `reader_test_required`는 이 문서 편집으로 바뀌지 않습니다.

## Observe

### 두 곡선과 RMS 차이

`trace.csv`의 두 번째 열은 MuJoCo TCP 오차(m), 세 번째 열은 PhysX TCP 오차(m)입니다. 이 수업의 두 번째 열은 이름이 `reference`이지만 0 목표선이 아니라 측정한 첫 엔진의 오차입니다. `plot.png`에서 두 곡선을 구분합니다.

`engine-comparison.json`의 `tcp_error_difference_rmse_m`는 두 오차 크기의 차이를 요약합니다. `joint_errors_a_rad`, `joint_errors_b_rad`와 `contacts_a_N`, `contacts_b_N`도 각각 rad·N 단위로 비교합니다. 이는 TCP 위치 벡터끼리의 차이나 접촉 모델의 동일성을 직접 계산한 값이 아닙니다.

현재 출력 시각은 코드의 `i * 0.02`로 재구성됩니다. 원본의 `control_dt_s`와 실제 시간 배열을 대조하고 0.02 s와 다르면 이 축을 물리적 시간 정렬의 증거로 사용하지 않습니다. 이 제한을 숨기고 지연 분석을 수행하지 않습니다.

## How it works

### 비교할 수 있는 조건을 먼저 고정하기

두 엔진의 초기 관절 자세(rad), 목표 위치 배열(m), 세계 좌표계와 제어 주기(s)를 먼저 맞춥니다. 같은 인덱스의 TCP 오차 크기를 $e_i^M,e_i^P$라고 하면 다음 값을 계산합니다.

$$
D=\sqrt{\frac{1}{N}\sum_{i=0}^{N-1}(e_i^M-e_i^P)^2}.
$$

$N$은 같은 수의 표본, 각 $e$와 $D$의 단위는 m입니다. 계산 예시(측정값 아님): 두 표본의 오차 차이가 [0.003, 0.004] m이면 $D\approx0.0035355$ m입니다. 두 엔진이 모두 같은 방향으로 20 mm씩 틀리면 D는 0일 수 있으므로 D=0은 목표 달성의 증거가 아닙니다.

### 엔진 차이의 원인을 단정하지 않기

다른 곡선은 적분·접촉뿐 아니라 모델 변환, 관성, actuator/drive, 좌표계 처리에서 생길 수 있습니다. 현재 일치 검사에 관절 이름·구동기 설정·툴 보정 전체가 포함되지는 않습니다. 이 항목은 별도로 검토해야 합니다. “엔진만 바꾸었다”는 인과 주장은 같은 목표 필드 네 개가 같다는 사실보다 강한 주장입니다.

## Code connection

[`runner.py`](../../../src/pai_lab/lessons/runner.py)는 이 ID를 [`comparison.run`](../../../src/pai_lab/lessons/comparison.py)으로 전달합니다. [`learning.previous_run`](../../../src/pai_lab/lessons/learning.py)이 두 완료 run을 찾고 원본 산출물 검증과 입력 기록을 수행합니다. 비교 모듈은 MuJoCo `trace.csv`의 세 번째 열과 PhysX payload의 `tcp_errors_m`를 읽습니다.

이 분기는 `seed`, `samples`, `variant`를 새 실험 조건으로 사용하지 않습니다. 같은 원본을 두고 `--variant 0.8`을 붙여도 엔진·목표·제어기를 바꾸는 비교가 되지 않습니다. 학습 체크포인트를 생성하는 분기와도 다릅니다.

## Try it

### 한 변수 계산 비교: 한 표본의 차이만 바꾸기

외부 실행 증거가 없는 상태에서는 계산 연습만 합니다. 위 예시에서 첫 번째 오차 차이를 0.003 → 0.006 m로 바꾸고 두 번째는 0.004 m로 유지하면 $D=\sqrt{(0.006^2+0.004^2)/2}\approx0.0050990$ m입니다. 큰 편차에 제곱이 더 큰 가중을 주는 이유를 설명하세요. 이는 분석식의 한 변수 비교이며 새로운 엔진 실행·정책 평가·학습 완료 증거가 아닙니다.

실제 엔진 조건을 바꾸는 실험은 원본 생산 수업에서 양쪽에 동일한 조건을 적용해 새 기록을 만든 뒤 분석합니다. 두 엔진의 목표가 달라졌다면 비교가 실패하는 것이 올바른 결과입니다. `--variant`로 분석 입력이 바뀌었다고 기록하지 않습니다.

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run sim-fr3-04 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [경로 안내](../paths.md)를 따릅니다.

## Checkpoint

### 이해 확인

1. D가 작아도 두 엔진 모두 목표에서 멀 수 있는 이유는 무엇인가요?
2. 파일의 `reference` 열은 이 수업에서 무엇을 뜻하나요?
3. 네 개의 일치 필드 외에 모델·구동기 검토가 필요한 이유는 무엇인가요?
4. 외부 PhysX 기록이 없는 Mac에서 이 수업의 어떤 부분을 공부할 수 있고 어떤 검증은 남아 있나요?

원본 run 두 개, 일치 필드, D(m), 관절·접촉 비교와 미확인 조건을 기록합니다. 계산 연습만 수행했다면 완료 처리하지 않습니다. 실측·비교·검토 증거가 준비된 뒤 공통 학습 workflow의 완료 조건을 충족해야 합니다.

답의 기준: 같은 큰 오차끼리는 차이가 0일 수 있습니다. reference는 MuJoCo 측정값입니다. 목표 필드 일치는 구동기·관성 동일성을 보장하지 않습니다. Mac에서는 식과 저장 기록을 분석할 수 있지만 실제 PhysX 생산·렌더링 검증은 해당 역량이 있는 환경에서 남아 있습니다.

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-03](./core-enlight-03.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
