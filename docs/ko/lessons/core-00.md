<!-- pal:language:start -->
<p align="right">
  <a href="core-00.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-00.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-00 — 저장소 시작과 호스트 점검

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `T00` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `None` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

먼저 [개념 교재: simulation](../concepts/simulation.md)를 읽고, [장비를 늘리는 학습 순서](../equipment-stages.md)에서 이 수업의 실행 단계를 확인합니다.

## Learning goals

호스트 준비 상태, 로컬 실행 기록, 학습 완료를 구분합니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

```bash
pal host detect --json
pal lesson check core-00 --json
```

## Action

```bash
pal lesson run core-00 --headless --seed 7 --samples 64 --output-dir .local/runs/core-00/baseline-01 --json
```

## Expected

실제 개발 실행의 예시입니다. 가로축·세로축의 단위와 기준/측정 곡선의 차이를 먼저 읽습니다. 개인 실행 결과는 별도 검사합니다.

![core-00 measured plot](../../assets/examples/core-00-plot.png)

host-audit.json의 platform_id, python, capability_status를 읽습니다. seed를 8로 바꿔도 OS나 설치 패키지는 달라지지 않아야 합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check core-00 --run-dir .local/runs/core-00/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect core-00 --run-dir .local/runs/core-00/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/core-00/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/core-00/baseline-01/experiment.json
```

## How it works

capability는 해당 검사가 성공했을 때 사용할 수 있습니다. Python은 major/minor 버전을 확인합니다. 패키지 import와 실제 렌더링·장치 연산 성공은 서로 다른 증거입니다.

$$
r=N_{available}/N_{checked}
$$

기호·단위·조건: N: 개수; r: 무차원.

손으로 계산하는 예시(실행 측정값이 아님): 3/5=0.6.

실전 연결: import 성공만으로 렌더링 성공을 판단할 수 없습니다.

### 입력에서 관측까지

로봇 수업의 첫 입력은 관절 명령이 아니라 실행할 호스트의 사실입니다. 설치된 패키지 이름과 실제로 성공한 기능 probe를 구별하면, 나중에 렌더링·CUDA·ROS가 없을 때 수식이나 정책의 오류로 오해하지 않습니다. available·unavailable·unverified 상태는 범주형 값이며 뒤 두 상태는 모두 그래프에서 0입니다. 그래프의 1·0은 available 여부를 표시한 값입니다. 물리 단위나 성능 점수가 아닙니다.

## Code connection

`examples/core-00/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

### 실제 코드와 산출물 읽기

[`physics.py`](../../../src/pai_lab/lessons/physics.py)와 [`runner.py`](../../../src/pai_lab/lessons/runner.py)의 dispatch를 대조합니다.

`physics.run`의 core-00 분기는 `detect_host().to_dict()`의 `capability_status`를 한 행씩 읽고 available을 1로 바꿉니다. `host-audit.json`의 `platform_id`, `python`, 상태별 설명을 그래프 인덱스와 대조합니다. summary의 metric은 available 역량의 개수이지 위 비율 r 자체가 아닙니다. 예를 들어 5개 중 3개이면 비율은 0.6이고 개수는 3입니다(계산 예시). 이 수업의 검사도 Python 3.12를 확인하며 모든 외부 스택이 있다고 판정하지 않습니다.

## Try it

이 수업은 구조·환경 조사입니다. seed를 바꾼 수치 실험을 요구하지 않습니다. 이름·단위·선수 조건과 실제 artifact를 대조하고, 발견한 항목을 review notes에 적습니다.

<details>
<summary>선택 심화: 가정이 깨지면 무엇이 달라질까요?</summary>

본문 식의 입력 하나를 고르고 단위를 적습니다. 그 값이 두 배일 때 출력이 두 배인지, 포화·정규화·좌표 변환 때문에 다른지 코드에서 확인합니다. 다른 가정이나 모델까지 동시에 바꾸면 한 변수 비교가 아니므로 별도 실행으로 기록합니다.

</details>

### 바꾸기 전에 예측하기

한 변수 계산 비교로 체크한 항목을 5개로 고정하고 available 개수만 3→4로 바꾸면 r은 0.6→0.8입니다. 실제 seed만 바꿔 재실행해도 설치 상태는 바뀌지 않아야 합니다. 이 결과는 환경 관찰이며 누락된 스택을 자동 설치할 이유가 아닙니다.

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

명령을 그대로 복사하기 전에 `--notes`를 자신이 관찰한 구체적인 수치와 해석으로 바꿉니다. 접수된 [개선점]을 먼저 저장·수정·재검증합니다. 미해결 개선점, 변경된 실행 코드, 손상된 산출물은 완료를 막습니다. 실행만으로 진도가 완료되지 않습니다. 완료 후 여기서 멈춥니다.

```bash
pal lesson review core-00 --run-dir .local/runs/core-00/baseline-01 --notes "검사한 이름·단위·구조·제한과 실제 근거를 자신의 값으로 적으세요." --json
pal lesson finish core-00 --run-dir .local/runs/core-00/baseline-01 --json
```

### 이해 확인과 답의 기준

질문: count=3과 r=0.6은 왜 모순이 아닌가요? 답: 서로 다른 요약입니다. 질문: NumPy import 성공으로 Isaac 준비를 결론 낼 수 있나요? 답: 별도 runtime·GPU probe가 필요합니다. 자신의 platform·Python·첫 미충족 역량과 다음 확인 항목을 적습니다.

이 구조 감사는 `evidence.comparison_errors`의 명시적 예외여서 별도 comparison run이 필수가 아닙니다. 위 review 명령은 baseline만 전달합니다. 종이 계산을 실행된 비교 산출물로 꾸미지 않고 실제로 확인한 감사 근거를 notes에 적습니다.

<!-- pal:navigation:start -->
## Next lesson

[core-01](./core-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
