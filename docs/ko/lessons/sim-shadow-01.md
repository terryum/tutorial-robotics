<!-- pal:language:start -->
<p align="right">
  <a href="sim-shadow-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-shadow-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-shadow-01 — Shadow Hand PhysX 입문

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / shadow` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco, isaac-sim, nvidia-cuda` |
| Prerequisites | `core-shadow-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

PhysX에서 제어·관측·렌더링을 수행하는 코드입니다. Mac에서 실행 검증하지 않았습니다. import 성공만으로 수업을 통과하지 않습니다.

선행 [개념 장](../concepts/physx.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: Shadow의 어떤 결합·접촉 특성에 PhysX 근거가 필요한가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

PhysX 입문은 가져온 Shadow의 관절 이름·드라이브 의미·결합·실제 물체 접촉을 보존해야 한다.

Shadow의 어떤 결합·접촉 특성에 PhysX 근거가 필요한가?

## Preflight

선행 수업: core-shadow-01. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

Ubuntu NVIDIA GPU와 설치된 Isaac Sim이 필요합니다. `pal setup verify --profile isaac --json`으로 점검합니다. 누락 시 capability-unavailable이며 다른 물리 엔진으로 대체하지 않습니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-shadow-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-shadow-01/baseline-01 --json
```

## Expected

`shadow-physx.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`physx-observations.json`의 `joint_states`, `commands`, `couplings_required`, `object_contact_forces_N`, 소스·엔진 식별을 본다. 센서는 손바닥과 이름 있는 물체를 필터링하며 양의 유한 측정 힘이 필요하다. 가져온 결합 검증 실패는 차단한다. Trace는 첫 관절 목표·관측이며 힘은 별도로 본다.

## How it works

### 직관

PhysX 입문은 가져온 Shadow의 관절 이름·드라이브 의미·결합·실제 물체 접촉을 보존해야 한다. 지정 손가락 닫힘·열림에서 손목 관절을 제외한다. 가져오기는 미검증 mimic/tendon 대응을 거부하며 그럴듯한 그림으로 추론하지 않고 동적 결합을 다시 검사한다.

### 계산과 단위

$$
c(\phi)=\frac{1-\cos(2\pi\phi)}2,\qquad \phi\in[0,1]
$$

무차원 ramp에 0.7×variant를 곱한 관절각(rad)을 명령한다. 실제 드라이브 응답·물체 힘은 측정해야 한다. 원본 equality 관절 다항식을 0.05 rad 이내로 검사하며 스키마 존재만으로 부족하다. 실행이 아닌 계산에서 c(0.5)=1이다.

```python
import numpy as np
phase = 0.5
ramp = (1 - np.cos(2 * np.pi * phase)) / 2
assert np.isclose(ramp, 1.0)
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/isaac_tasks.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac_tasks.py)

`examples/sim-shadow-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

## Try it

### 통제된 비교

소스·시드·샘플 수를 고정하고 `variant`만 1→0.8로 바꿔 지정 닫힘 진폭을 줄인다. 한도·접촉 때문에 실제 변위는 비선형일 수 있다. 물체 접촉과 관절별 변화를 구별한다. 작은 닫힘이 더 좋은 파지라는 뜻은 아니다.

```bash
pal lesson run sim-shadow-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-shadow-01/comparison-01 --json
pal lesson check sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --json
pal lesson check sim-shadow-01 --run-dir .local/runs/sim-shadow-01/comparison-01 --json
pal lesson compare sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --comparison-run-dir .local/runs/sim-shadow-01/comparison-01 --output-dir .local/comparisons/sim-shadow-01/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run sim-shadow-01 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [실행 안내](../READER_GUIDE.md#학습-중단재개와-호스트-이동)를 따릅니다.

## Checkpoint

### 이해 확인

물체 접촉과 자기 접촉을 구별하는 이유는? 접힌 손가락이 과제 물체 없이 손 자체에 닿을 수 있기 때문이다. 양의 접촉 하나가 안정 파지를 증명하는가? 아니다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --comparison-run-dir .local/runs/sim-shadow-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-shadow-01 --run-dir .local/runs/sim-shadow-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-stretch3-01](./core-stretch3-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
