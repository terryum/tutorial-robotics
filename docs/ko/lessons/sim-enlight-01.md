<!-- pal:language:start -->
<p align="right">
  <a href="sim-enlight-01.md" lang="ko">한국어</a> | <a href="../../en/lessons/sim-enlight-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-enlight-01 — Enlight ROS 2 가상 하드웨어

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / enlight` |
| Legacy alias | `T18` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `core-enlight-01, sim-ros-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

선행 [개념 장](../concepts/ros.md)과 [장비 확장 순서](../equipment-stages.md)를 읽는다. 이 수업의 질문: 가상 하드웨어는 장비 연결 전에 무엇을 검증하는가?필요한 경우 [NVIDIA 생태계 실습](../nvidia-ecosystem.md)을 참고하되, 이 수업이 쓰는 실제 엔진·프레임워크는 아래 생산자로 구별한다.

## Learning goals

Fake hardware는 통신과 실물 권한을 분리한다.

가상 하드웨어는 장비 연결 전에 무엇을 검증하는가?

## Preflight

장비 setup·매뉴얼 참조: [Enlight](../setup/enlight.md).

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

[WS1 환경·입력 준비](../../verification/ws1-handoff.md)를 먼저 읽습니다. 이 호스트에서 외부 스택이 확인되기 전에는 reader_test_required입니다.

```bash
pal host detect --json
pal lesson check sim-enlight-01 --json
```

## Action

준비된 환경을 활성화하고 새 출력 폴더를 쓴다. 반환 실행 경로를 보존하며 실행만으로 완료되지 않는다.

```bash
pal lesson run sim-enlight-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-enlight-01/baseline-01 --json
```

## Expected

일곱 관절 이름, 수신 상태의 정확한 일치, reset 결과를 확인합니다. 실패·종료 때 ROS 객체가 모두 닫히는지도 봅니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/sim-enlight-01/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/sim-enlight-01/baseline-01/experiment.json
```

### 산출물 읽기

`experiment.json`의 `qos`, `domain`, `localhost_only`, `source`, 토픽·서비스 그래프와 최상위 `checks`를 읽는다. Reliable depth 10, localhost-only domain 217, 서비스·수신 마감을 사용한다. `state_equal`, `all_messages_received`, `tf_received`, `service_roundtrip`은 실제 DDS 트래픽에 대응해야 한다. 정적 항등 TF는 실물 팔 보정이 아니다.

## How it works

### 직관

Fake hardware는 통신과 실물 권한을 분리한다. `ros.run`은 Enlight MuJoCo 초안을 불러와 시뮬레이션 동역학을 진행하고 격리 ROS 환경에서 이름 있는 관절 상태를 발행한다. Trigger reset 서비스는 시뮬레이션을 초기화하며 생산용 Flexiv 드라이버를 열거나 RDK·펌웨어 호환성을 검증하지 않는다.

### 계산과 단위

$$
e_{msg}=\max_i|q^{sent}_{i,0}-q^{received}_{i,0}|
$$

첫 관절 위치는 rad, 타임스탬프는 ROS 초·나노초로 나눈 시뮬레이션 시간이며 속도는 rad/s다. 최대 송수신 오차는 전송 검사이지 목표 추종 오차가 아니다. DDS 측정이 아닌 계산 예제로 0.2 rad를 보내고 받으면 오차는 0이다.

```python
sent_rad, received_rad = 0.2, 0.2
assert abs(sent_rad - received_rad) == 0.0
```

## Code connection

### 소스 추적

[`src/pai_lab/lessons/ros.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/ros.py)

`examples/sim-enlight-01/run.py`는 공통 runner로 위임하며 runner는 카탈로그 구현·역량을 확인한 뒤 분기한다. 위 소스가 여기의 양을 계산한다. 메타데이터 파일 이름만으로 계산 내용을 판단하면 안 된다.

[공개 경로 검증](../../verification/robot-paths-2026-11-08.md)은 기존 시뮬레이션 근거와 미검증 외부·장치 실행을 구별한다.

## Try it

### 통제된 비교

시드·샘플 수·모델을 유지하고 시뮬레이션 사인 입력 배율 `variant`만 바꾼다. 위치는 달라져도 메시지 일치는 유지될 수 있다. Reliable QoS를 실시간 제어 보장으로 해석하지 않는다.

```bash
pal lesson run sim-enlight-01 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/sim-enlight-01/comparison-01 --json
pal lesson check sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
pal lesson check sim-enlight-01 --run-dir .local/runs/sim-enlight-01/comparison-01 --json
pal lesson compare sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --comparison-run-dir .local/runs/sim-enlight-01/comparison-01 --output-dir .local/comparisons/sim-enlight-01/comparison-01 --json
```

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

### 이해 확인

통신 오차 0인데 운동은 나쁠 수 있는 이유는? 원하지 않는 상태도 충실히 전송할 수 있기 때문이다. 실물 Flexiv 네트워크를 검사하는가? 아니다.

두 실행의 실제 값·축·그림을 확인한다. 아래 notes를 측정값·해석으로 바꾸고 피드백을 해소한 다음 수업 하나를 review/finish한다. 역량이 없으면 unavailable이며 공개 배지가 자신의 완료는 아니다.

```bash
pal lesson review sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --comparison-run-dir .local/runs/sim-enlight-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-enlight-01 --run-dir .local/runs/sim-enlight-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-02](./sim-enlight-02.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
