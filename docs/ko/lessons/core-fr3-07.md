# core-fr3-07 — ROS 없는 FR3 도달 환경

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `T22` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

FR3 도달 과제의 reset·관측·행동·보상·에피소드 경계를 사용합니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

필요한 공개 모델을 한 번 준비합니다:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-fr3-07 --json
```

## Action

```bash
pal lesson run core-fr3-07 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-07/baseline-01 --json
```

## Expected

transitions.json의 각 전이를 읽습니다. 기본 자코비안 제어기가 거리를 줄여야 합니다. 스텝 수를 세고 성공과 시간 초과를 구분합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check core-fr3-07 --run-dir .local/runs/core-fr3-07/baseline-01 --json
```

## How it works

관측은 관절 위치 차이 7개, 스케일한 속도 7개, 월드 목표 오차 3개입니다. 제한된 행동 7개가 관절 위치 목표를 바꿉니다. 도달 성공은 terminated, 64스텝 시간 제한은 truncated로 구분해야 PPO bootstrap이 올바릅니다.

```text
observation ∈ R¹⁷; action ∈ R⁷; reward = −distance − effort penalty
```

## Code connection

`examples/core-fr3-07/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

```bash
pal lesson run core-fr3-07 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-07/comparison-01 --variant 1.5 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

명령을 그대로 복사하기 전에 `--notes`를 자신이 관찰한 구체적인 수치와 해석으로 바꿉니다. 접수된 [개선점]을 먼저 저장·수정·재검증합니다. 미해결 개선점, 변경된 실행 코드, 손상된 산출물은 완료를 막습니다. 실행만으로 진도가 완료되지 않습니다. 완료 후 여기서 멈춥니다.

```bash
pal lesson review core-fr3-07 --run-dir .local/runs/core-fr3-07/baseline-01 --comparison-run-dir .local/runs/core-fr3-07/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish core-fr3-07 --run-dir .local/runs/core-fr3-07/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-08](./core-fr3-08.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
