<!-- pal:language:start -->
<p align="right">
  <a href="sim-cross-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-cross-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-cross-01 — MuJoCo–Isaac sim-to-sim 검증

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / cross` |
| Legacy alias | `T35` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `isaac-sim` |
| Prerequisites | `core-fr3-08, sim-isaac-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

선행 [개념 장](../concepts/physx.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 두 물리 엔진을 비교하기 전에 어떤 조건을 맞춰야 하는가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

같은 초기 상태와 적용 힘으로 실제 엔진 두 개를 비교한다.

두 물리 엔진을 비교하기 전에 어떤 조건을 맞춰야 하는가?

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-cross-01 --json
```

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-cross-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-cross-01/baseline-01 --json
```

## Expected

각 엔진의 qpos와 전체 RMSE를 확인합니다. 초기 수용 한계는 0.15 rad입니다. 넘으면 원인을 조사할 실패이며 검사를 면제하지 않습니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/sim-cross-01/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/sim-cross-01/baseline-01/experiment.json
```

### 산출물 읽기

`experiment.json` → `payload`의 `joint_order`, `isaac_joint_indices`, `states`, `state_rmse_rad`, `comparison`, `dt_s`, 카메라·깊이 필드를 확인한다. `isaac-observations.json`은 엔진 payload를 보존한다. `state_parity`는 RMS 0.15 rad 미만의 교육 기준이며 실물 허용 오차가 아니다. 스칼라뿐 아니라 대응된 관절 trace도 읽는다.

## How it works

### 직관

같은 초기 상태와 적용 힘으로 실제 엔진 두 개를 비교한다. `isaac.run`은 가져온 Wuji articulation을 effort 제어로 바꾸고 MuJoCo 구동기를 비활성화한 뒤 샘플마다 MuJoCo와 PhysX를 각각 한 스텝 진행한다. 관절 이름으로 PhysX 인덱스를 대응하며 그림이 비슷하다고 순서가 같지는 않다. 두 엔진의 자세를 직접 지정하는 것과 다른 동역학 비교다.

### 계산과 단위

$$
e=\sqrt{\frac{1}{Nn}\sum_{i=1}^N\sum_{j=1}^n(q^M_{ij}-q^P_{ij})^2}
$$

`states`는 이름 있는 회전 좌표 n개의 N개 샘플이며 rad 단위다. 스칼라도 rad다. 기준 물리 스텝은 0.002 s, 힘은 `0.002 * variant * sin(0.1*i)` N m이다. RMS는 관절·시간 평균이며 최대 오차가 아니다. 엔진 측정이 아닌 계산 예제에서 차이 [0.01, -0.01] rad의 RMS는 0.01 rad이다.

```python
import numpy as np
difference_rad = np.array([0.01, -0.01])
assert np.isclose(np.sqrt(np.mean(difference_rad**2)), 0.01)
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/isaac.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/isaac.py)

`examples/sim-cross-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

## Try it

### 통제된 비교

두 엔진의 힘을 함께 배율 조정하는 `variant`만 바꾸고 시드·소스·자세·샘플 수를 고정한다. 큰 힘은 드라이브·접촉 차이를 드러낼 수 있으며 일치 개선을 보장하지 않는다. 실제 Isaac 호스트가 필요하고 휴대형 대체 실행으로 PhysX를 검증할 수 없다.

```bash
pal lesson run sim-cross-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-cross-01/comparison-01 --json
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
pal lesson check sim-cross-01 --run-dir .local/runs/sim-cross-01/comparison-01 --json
pal lesson compare sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --comparison-run-dir .local/runs/sim-cross-01/comparison-01 --output-dir .local/comparisons/sim-cross-01/comparison-01 --json
```

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

### 이해 확인

MuJoCo 구동기를 끄는 이유는? 추가 구동기 제어기가 힘 실험을 바꾸지 않게 하기 위해서다. RMS 0.15 rad 미만이면 실물이 안전한가? 아니다. 이 시뮬레이션 비교의 기준일 뿐이다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --comparison-run-dir .local/runs/sim-cross-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-cross-01 --run-dir .local/runs/sim-cross-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-deploy-01](./sim-deploy-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->


[Isaac 6.0 importer 변경 사항](https://docs.isaacsim.omniverse.nvidia.com/latest/migration_guides/isaac_sim_6_0/urdf_mjcf_importer_exporter_pipeline.html). 실제 5.1/6.0 호스트 실행 검증은 별도로 필요합니다.
