<!-- pal:language:start -->
<p align="right">
  <a href="sim-enlight-02.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-enlight-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-02 — Enlight 접촉 과제 시뮬레이션과 후보 번들

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `T41A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-enlight-02, sim-deploy-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

선행 [개념 장](../concepts/deployment-hardware.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 접촉 과제 번들은 왜 게이트 평가 전까지 후보로 남는가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

이 후보는 학습 정책이 아니라 알려진 제어기다.

접촉 과제 번들은 왜 게이트 평가 전까지 후보로 남는가?

## Preflight

장비 setup·매뉴얼 참조: [Enlight](../setup/enlight.md).

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-enlight-02 --json
```

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-enlight-02 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-enlight-02/baseline-01 --json
```

## Expected

실제 탐침·테이블 힘, 유한하고 제한된 제어, 렌더링 형상을 요구합니다. candidate-controller.json과 contact-actions.npz를 읽고 hardware_compatible은 false로 둡니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/sim-enlight-02/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/sim-enlight-02/baseline-01/experiment.json
```

### 산출물 읽기

`contact-actions.npz`는 실제 포화 명령을 저장한다. `candidate-controller.json`과 `experiment.json` → `payload`는 이득·`mean_normal_force_N`·`candidate_only=True`·`hardware_compatible=False`·롤백을 보고한다. 법선력 스칼라는 이름 있는 프로브·테이블쌍의 샘플별 합을 평균하며 학습 체크포인트나 보정 실물 힘이 아니다.

## How it works

### 직관

이 후보는 학습 정책이 아니라 알려진 제어기다. `enlight_contact`는 Enlight 모델에서 파생 프로브·테이블 장면을 만든다. MuJoCo가 동역학을 적분하며 Torch는 CUDA에서 28원소 제어 입력을 계산한다. 여기의 GPU 산술은 PhysX 시뮬레이션이나 Isaac Lab 학습이 아니다.

### 계산과 단위

$$
\tau=\operatorname{clip}(80(q^*-q)-12\dot q+b+J^T[0,0,-2v]^T,\tau_{min},\tau_{max})
$$

위치 오차 7개·속도 7개·편향 7개·자코비안 힘 항 7개가 28입력이다. 각도는 rad, 속도 rad/s, 편향·토크 N m, 힘은 월드 N이며 v는 무차원 `variant`다. 접촉 측정이 아닌 계산으로 편향·힘 항 전 80×0.01−12×0.02=0.56 N m이다.

```python
import numpy as np
raw_nm = 80 * 0.01 - 12 * 0.02
assert np.isclose(raw_nm, 0.56)
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/gpu.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/gpu.py)

`examples/sim-enlight-02/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

`variant`만 1에서 1.5로 바꾸면 요청 하향 월드 힘이 2→3 N이 되며 PD 이득 80·12는 같다. 측정 힘과 적용 토크를 비교한다. 포화·기하로 비례 응답이 안 나올 수 있다. 동역학이 MuJoCo여도 CUDA가 없으면 unavailable이다.

```bash
pal lesson run sim-enlight-02 --headless --seed 7 --samples 64 --variant 1.5 --output-dir .local/runs/sim-enlight-02/comparison-01 --json
pal lesson check sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
pal lesson check sim-enlight-02 --run-dir .local/runs/sim-enlight-02/comparison-01 --json
pal lesson compare sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --comparison-run-dir .local/runs/sim-enlight-02/comparison-01 --output-dir .local/comparisons/sim-enlight-02/comparison-01 --json
```

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

### 이해 확인

무엇을 학습했는가? 이 경로의 이득은 고정되어 학습하지 않는다. 양의 접촉력은 무엇을 증명하는가? 이름 있는 시뮬레이션 프로브·테이블 접촉이며 안전한 실물 힘 제어가 아니다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --comparison-run-dir .local/runs/sim-enlight-02/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-02 --run-dir .local/runs/sim-enlight-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-wuji-02](./sim-wuji-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
