# sim-ros-04 — 시뮬레이션과 ROS 2 공통 embodiment API

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / ros2` |
| Legacy alias | `T21` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `sim-ros-02` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

## Learning goals

시뮬레이션과 ROS의 공통 reset·observe·act·close 인터페이스를 확인합니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-ros-04 --json
```

## Action

```bash
pal lesson run sim-ros-04 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-ros-04/baseline-01 --json
```

## Expected

embodiment-contract.json의 동작 횟수와 trace를 비교합니다. 통신 실패 뒤에도 객체가 정리되는지 확인합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/sim-ros-04/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/sim-ros-04/baseline-01/experiment.json
```

## How it works

embodiment 인터페이스는 생명주기·단위·순서를 정의합니다. reset 서비스는 MuJoCo를 초기화하고 observe는 수신 상태를 읽으며 act는 시뮬레이션 입력만 바꿉니다. 마지막에 ROS 객체를 정리합니다. 실물 어댑터에는 별도 승인 절차가 필요합니다.

$$
e=\max_{t,j}|q^{sent}_{t,j}-q^{received}_{t,j}|
$$

기호·단위·조건: q rad; t는 대응 sequence/time; 값보다 이름을 먼저 대조.

손으로 계산하는 예시(실행 측정값이 아님): sent 0.2 rad, received 0.199 rad → error 0.001 rad.

실전 연결: 상태 수신 성공은 명령 발행이나 물리적 정지 증거와 다릅니다.

## Code connection

`examples/sim-ros-04/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/ros.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

시뮬레이션 액추에이터 계약의 정현파 명령 진폭을 0.1 → 0.15로 바꿉니다. 메시지 수와 QoS는 같습니다.

```bash
pal lesson run sim-ros-04 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-ros-04/comparison-01 --variant 1.5 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

```bash
pal lesson compare sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --comparison-run-dir .local/runs/sim-ros-04/comparison-01 --output-dir .local/comparisons/sim-ros-04/comparison-01 --json
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
pal lesson review sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --comparison-run-dir .local/runs/sim-ros-04/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish sim-ros-04 --run-dir .local/runs/sim-ros-04/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-g1-01](./sim-g1-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
