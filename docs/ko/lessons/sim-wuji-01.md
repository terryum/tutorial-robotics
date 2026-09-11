# sim-wuji-01 — Wuji GPU 손안 조작 PPO

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / wuji` |
| Legacy alias | `T27` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-wuji-02, core-rl-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

## Learning goals

고정된 Wuji MJLab 재배향 과제를 학습·평가합니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-wuji-01 --json
```

## Action

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-wuji-01/baseline-01 --json
```

## Expected

정책 텐서 변경, 유한한 평가 보상, 비어 있지 않은 영상을 요구합니다. 짧은 실행의 성공과 손안 조작 성능을 구분합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/sim-wuji-01/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/sim-wuji-01/baseline-01/experiment.json
```

## How it works

vendor 과제는 자체 손·물체·보상·PPO runner를 등록합니다. 지원되는 Pixi 환경, 준비된 자산, 별도 로컬 출력 폴더를 사용합니다. vendor 학습 embodiment가 자동으로 보정된 Beta 2 실물 모델이 되는 것은 아닙니다.

$$
\theta_{k+1}=\theta_k-\eta\nabla_\theta L_k
$$

기호·단위·조건: θ: 학습 파라미터; η: 학습률; L: 알고리즘 손실; 예시는 scalar SGD.

손으로 계산하는 예시(실행 측정값이 아님): θ=1, η=0.01, gradient=2 → new θ=0.98.

실전 연결: 실제 학습은 가중치를 바꾸고 재로드해야 하며 짧은 smoke로 성공률을 보장하지 않습니다.

## Code connection

`examples/sim-wuji-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/gpu.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

표본 예산을 64 → 96으로 바꿉니다. 학습 수업은 이 예산에서 갱신 수와 평가 길이를 결정하며, 후보 평가 수업은 평가 길이만 바꿉니다.

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --output-dir .local/runs/sim-wuji-01/comparison-01 --samples 96 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

```bash
pal lesson compare sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --comparison-run-dir .local/runs/sim-wuji-01/comparison-01 --output-dir .local/comparisons/sim-wuji-01/comparison-01 --json
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
pal lesson review sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --comparison-run-dir .local/runs/sim-wuji-01/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-vla-01](./sim-vla-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
