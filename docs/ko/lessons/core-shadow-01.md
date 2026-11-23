<!-- pal:language:start -->
<p align="right">
  <a href="core-shadow-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-shadow-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-shadow-01 — Shadow Hand 관절·시너지·물체 접촉

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / shadow` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

고정한 모델의 관절·구동기 이름과 주소를 검사하고 실제 움직임·접촉을 기록합니다.

선행 [개념 장](../concepts/robot-hands.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: Shadow 관절 시너지는 어떻게 물체 접촉을 만드는가?

## Learning goals

입문은 손목을 고정하고 손가락 하나를 움직인 뒤 공유 손가락 시너지로 닫고 연다.

Shadow 관절 시너지는 어떻게 물체 접촉을 만드는가?

## Preflight

선행 수업: core-04. `pal course next --json`으로 준비 상태를 확인합니다. 실행 결과·진도는 ignored `.local/`에 저장합니다.

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run core-shadow-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-shadow-01/baseline-01 --json
```

## Expected

`shadow-introduction.json`, `trace.csv`, `plot.png`, `experiment.json`을 확인합니다. `evaluation.json`의 performance_verified는 학습 성능만 나타냅니다.

## Observe

축·단위·첫/마지막 오차·최댓값을 읽습니다. 렌더링에서 모델과 움직임을 확인하고, payload의 관절 이름·그룹·접촉을 수치와 대조합니다.

### 산출물 읽기

`experiment.json` → `payload`의 `actuator_names`, `groups`, `qpos`, `qvel`, `commands`, `contact_counts`, `couplings`, `nq`, `nu`, `time_s`를 읽는다. `contact_observed`는 이름 있는 구를 뜻한다. 그래프는 관절 변위 노름이며 힘·파지 성공이 아니다. 양의 개수는 접촉이 있었다는 뜻뿐이다.

## How it works

### 직관

입문은 손목을 고정하고 손가락 하나를 움직인 뒤 공유 손가락 시너지로 닫고 연다. 파생 장면은 고정 grasp site에 이름 있는 구 `contact_object`를 두며 자기 접촉이 아니라 물체 접촉을 센다. 명령은 구동기를 다루고 `qpos`는 결과 동역학 상태다. 지정 제어이며 학습 파지 정책이 아니다.

### 계산과 단위

$$
c(\phi)=\frac{1-\cos(2\pi\phi)}2,\qquad \phi\in[0,1]
$$

무차원 ramp는 0에서 시작해 위상 0.5에서 1, 끝에서 0이다. MuJoCo 명령은 선택 구동기의 상한에 0.7×variant×ramp를 곱하고 범위를 적용한다. rad 단위 관절 변위 노름과 N 단위 접촉력은 다르다. 실행이 아닌 계산 예제에서 c(0.5)=1이다.

```python
import numpy as np
phase = 0.5
ramp = (1 - np.cos(2 * np.pi * phase)) / 2
assert np.isclose(ramp, 1.0)
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/embodiments.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py)

`examples/core-shadow-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

소스·시드·샘플 수를 고정하고 `variant`만 1→0.8로 바꿔 지정 닫힘 진폭을 줄인다. 한도·접촉 때문에 실제 변위는 비선형일 수 있다. 물체 접촉과 관절별 변화를 구별한다. 작은 닫힘이 더 좋은 파지라는 뜻은 아니다.

```bash
pal lesson run core-shadow-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-shadow-01/comparison-01 --json
pal lesson check core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --json
pal lesson check core-shadow-01 --run-dir .local/runs/core-shadow-01/comparison-01 --json
pal lesson compare core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --comparison-run-dir .local/runs/core-shadow-01/comparison-01 --output-dir .local/comparisons/core-shadow-01/comparison-01 --json
```

## Recovery

중단 시 기록을 보존합니다. `pal course pause`, `pal course resume`, `pal lesson run core-shadow-01 --resume-from BASE --json`은 저장 상태를 확인하며 자동 동작을 재개하지 않습니다. 짧은 시뮬레이션은 새 run에서 재시작합니다. 학습 재개·호스트 이동은 [경로 안내](../paths.md)를 따릅니다.

## Checkpoint

### 이해 확인

물체 접촉과 자기 접촉을 구별하는 이유는? 접힌 손가락이 과제 물체 없이 손 자체에 닿을 수 있기 때문이다. 양의 접촉 하나가 안정 파지를 증명하는가? 아니다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --comparison-run-dir .local/runs/core-shadow-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-shadow-01 --run-dir .local/runs/core-shadow-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-shadow-01](./sim-shadow-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
