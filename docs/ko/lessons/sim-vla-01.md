# sim-vla-01 — SmolVLA 미세조정과 정책 서버

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / vla` |
| Legacy alias | `T32C` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-vla-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

준비된 SmolVLA 가중치를 실제 로컬 데이터로 미세조정하고 추론 서버를 실행합니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-vla-01 --json
```

## Action

```bash
pal lesson run sim-vla-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-vla-01/baseline-01 --json
```

## Expected

parameter_delta, 유한한 손실, training-observation.png, server-response.json을 읽습니다. 재로딩한 신경망 정책의 응답이며 command sink에 보관합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-vla-01 --run-dir .local/runs/sim-vla-01/baseline-01 --json
```

## How it works

LeRobot processor가 상태·행동을 정규화하고 언어를 토큰화합니다. 모델 손실 계산·역전파·정책과 processor 저장·재로딩 뒤 실제 loopback HTTP 요청을 보냅니다. 대형 가중치와 데이터 영상은 명시적으로 준비하며 offline 모드로 숨은 다운로드를 막습니다.

```text
batch → processors → SmolVLA loss → gradient → checkpoint → HTTP inference
```

## Code connection

`examples/sim-vla-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/vla.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

AdamW 학습률을 10⁻⁴ → 1.5×10⁻⁴로 바꿉니다. 준비된 모델과 데이터셋은 같습니다.

```bash
pal lesson run sim-vla-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-vla-01/comparison-01 --variant 1.5 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

명령을 그대로 복사하기 전에 `--notes`를 자신이 관찰한 구체적인 수치와 해석으로 바꿉니다. 접수된 [개선점]을 먼저 저장·수정·재검증합니다. 미해결 개선점, 변경된 실행 코드, 손상된 산출물은 완료를 막습니다. 실행만으로 진도가 완료되지 않습니다. 완료 후 여기서 멈춥니다.

```bash
pal lesson review sim-vla-01 --run-dir .local/runs/sim-vla-01/baseline-01 --comparison-run-dir .local/runs/sim-vla-01/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish sim-vla-01 --run-dir .local/runs/sim-vla-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-vla-02](./sim-vla-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
