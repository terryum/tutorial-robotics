# core-wuji-01 — Wuji Hand 2 Beta 2 관절, 자세와 시너지

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / wuji` |
| Legacy alias | `T14` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-02, core-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

## Learning goals

손 시너지로 제한된 open·half·closed 자세를 만듭니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

필요한 공개 모델을 한 번 준비합니다:

```bash
pal assets fetch wuji-description-beta2
```

```bash
pal host detect --json
pal lesson check core-wuji-01 --json
```

## Action

```bash
pal lesson run core-wuji-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-wuji-01/baseline-01 --json
```

## Expected

실제 개발 실행의 예시입니다. 가로축·세로축의 단위와 기준/측정 곡선의 차이를 먼저 읽습니다. 개인 실행 결과는 별도 검사합니다.

![core-wuji-01 measured plot](../../assets/examples/core-wuji-01-plot.png)

세 named pose와 MuJoCo가 계산한 다섯 손끝 위치를 확인합니다. 시너지 크기만 늘려 관절 한계에 도달하는지 관찰합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check core-wuji-01 --run-dir .local/runs/core-wuji-01/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect core-wuji-01 --run-dir .local/runs/core-wuji-01/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/core-wuji-01/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/core-wuji-01/baseline-01/experiment.json
```

## How it works

시너지는 스칼라 하나를 20개 관절 설정으로 바꿉니다. 굽힘과 벌림에 다른 계수를 적용하고 고정된 Beta 2 관절 한계로 제한합니다. 파지 제어기 학습이 아니라 자세 구성 실험입니다.

$$
q=\operatorname{clip}(s\alpha,q_{min},q_{max})
$$

기호·단위·조건: s: 무차원 synergy; α,q: rad; 제한은 모델에서 읽음.

손으로 계산하는 예시(실행 측정값이 아님): s=0.5, α=0.8 rad → q=0.4 rad before clipping.

실전 연결: 자세를 만든 것만으로 파지력이나 물체 유지가 보장되지 않습니다.

## Code connection

`examples/core-wuji-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/hands.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

시너지 진폭 배율을 1 → 1.5로 바꿉니다. 제한 적용 후 관절별 값을 확인합니다. 이미 포화된 관절은 변하지 않을 수 있습니다.

```bash
pal lesson run core-wuji-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-wuji-01/comparison-01 --variant 1.5 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

```bash
pal lesson compare core-wuji-01 --run-dir .local/runs/core-wuji-01/baseline-01 --comparison-run-dir .local/runs/core-wuji-01/comparison-01 --output-dir .local/comparisons/core-wuji-01/comparison-01 --json
```

<details>
<summary>선택 심화: 가정이 깨지면 무엇이 달라질까요?</summary>

본문 식의 입력 하나를 고르고 단위를 적습니다. 그 값이 두 배일 때 출력이 두 배인지, 포화·정규화·좌표 변환 때문에 다른지 코드에서 확인합니다. 다른 가정이나 모델까지 동시에 바꾸면 한 변수 비교가 아니므로 별도 실행으로 기록합니다.

</details>

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

명령을 그대로 복사하기 전에 `--notes`를 자신이 관찰한 구체적인 수치와 해석으로 바꿉니다. 접수된 [개선점]을 먼저 저장·수정·재검증합니다. 미해결 개선점, 변경된 실행 코드, 손상된 산출물은 완료를 막습니다. 실행만으로 진도가 완료되지 않습니다. 완료 후 여기서 멈춥니다.

```bash
pal lesson review core-wuji-01 --run-dir .local/runs/core-wuji-01/baseline-01 --comparison-run-dir .local/runs/core-wuji-01/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish core-wuji-01 --run-dir .local/runs/core-wuji-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-wuji-02](./core-wuji-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
