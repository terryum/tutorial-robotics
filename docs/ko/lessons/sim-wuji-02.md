<!-- pal:language:start -->
<p align="right">
  <a href="sim-wuji-02.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-wuji-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-wuji-02 — Wuji 정교 조작 후보 번들

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / wuji` |
| Legacy alias | `T42A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `sim-wuji-01, sim-deploy-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

선행 [개념 장](../concepts/deployment-hardware.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 정교 조작 후보에는 어떤 모델·정책 식별 정보가 필요한가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

정교 조작 후보는 완료된 실제 `sim-wuji-01` 체크포인트를 읽고 동일한 고정 벤더 과제를 play 모드로 구성해 평가한 뒤 정확한 정책 바이트를 복사한다.

정교 조작 후보에는 어떤 모델·정책 식별 정보가 필요한가?

## Preflight

장비 setup·매뉴얼 참조: [Wuji Hand 2 Beta 2](../setup/wuji.md).

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-wuji-02 --json
```

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-wuji-02 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-wuji-02/baseline-01 --json
```

## Expected

평균 보상, evaluation-actions.npz, evaluation.png, candidate/manifest.json을 읽습니다. 실제 checkpoint 재로딩과 유한한 평가를 요구하며 performance_verified는 false로 둡니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/sim-wuji-02/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/sim-wuji-02/baseline-01/experiment.json
```

### 산출물 읽기

`candidate/manifest.json`의 `task`, `policy_sha256`, `mean_reward`, `candidate_only=True`, `hardware_compatible=False`, `performance_verified=False`, `rollback=command-sink`를 읽는다. `evaluation-actions.npz`는 샘플 행동, `evaluation.png`는 실제 렌더링이다. 유한값·재로딩 검사는 실행을 확인하며 손안 과제를 해결한 것은 아니다.

## How it works

### 직관

정교 조작 후보는 완료된 실제 `sim-wuji-01` 체크포인트를 읽고 동일한 고정 벤더 과제를 play 모드로 구성해 평가한 뒤 정확한 정책 바이트를 복사한다. 체크포인트 재로딩·과제 롤아웃이며 새 학습이 아니다. 벤더 과제 모델이 곧 Beta 2 실물 손의 동등성은 아니다.

### 계산과 단위

$$
\bar r=\frac1N\sum_{i=1}^N r_i
$$

N은 평가 스텝, r은 벤더 과제 보상이며 평균 단위도 과제 점수다. 행동 형태는 벤더 과제를 따르며 보편적인 20관절 배열이 아니다. 정책 평가가 아닌 계산으로 보상 [1,2,3]의 평균은 2다.

```python
import numpy as np
assert np.mean([1.0, 2.0, 3.0]) == 2.0
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/gpu.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/gpu.py)

`examples/sim-wuji-02/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

## Try it

### 통제된 비교

체크포인트·시드·과제를 유지하고 `samples`를 64→96으로 바꾼다. 여기서는 평가 지평만 바뀌며 최적화는 호출하지 않는다. 선언한 지평의 보상 분포를 비교하고 모델 출처를 보존한다. 이 후보에서 `variant`는 쓰지 않는다.

```bash
pal lesson run sim-wuji-02 --headless --seed 7 --samples 96 --output-dir .local/runs/sim-wuji-02/comparison-01 --json
pal lesson check sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
pal lesson check sim-wuji-02 --run-dir .local/runs/sim-wuji-02/comparison-01 --json
pal lesson compare sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --comparison-run-dir .local/runs/sim-wuji-02/comparison-01 --output-dir .local/comparisons/sim-wuji-02/comparison-01 --json
```

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

### 이해 확인

정책 해시가 맞으면 파지가 좋아졌는가? 아니다. 바이트 식별이다. `performance_verified`가 거짓인 이유는? 짧은 롤아웃이 과제 해결 성능 게이트를 구현하지 않기 때문이다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --comparison-run-dir .local/runs/sim-wuji-02/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[hw-common-01](./hw-common-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
