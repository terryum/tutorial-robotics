# core-rl-01 — 최소 연속 행동 PPO

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / learning` |
| Legacy alias | `T23` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

최소 연속 행동 PPO의 전체 갱신 과정을 따라갑니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

```bash
pal host detect --json
pal lesson check core-rl-01 --json
```

## Action

```bash
pal lesson run core-rl-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-rl-01/baseline-01 --json
```

## Expected

policy.npz, parameter_delta, advantage_std, clip_fraction을 확인합니다. 다시 로드한 예측이 같아야 합니다. 짧은 optimizer 검사는 제어 정책의 성공을 입증하지 않습니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check core-rl-01 --run-dir .local/runs/core-rl-01/baseline-01 --json
```

## How it works

선형 가우시안 actor가 실제 진자 rollout을 수집합니다. 선형 critic과 GAE가 이점을 계산하며 시간 제한에서는 bootstrap하고 종료 상태에서는 하지 않습니다. clipped surrogate로 확률비 변화를 제한합니다. 손실 곡선을 미리 정하지 않고 경사로 파라미터를 갱신합니다.

```text
L = mean min(rA, clip(r, 0.8, 1.2)A)
```

## Code connection

`examples/core-rl-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

actor 경사 갱신 크기를 0.01 → 0.015로 바꿉니다. seed와 rollout·갱신 수는 고정하고 파라미터 변화 및 측정 보상을 비교합니다.

```bash
pal lesson run core-rl-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-rl-01/comparison-01 --variant 1.5 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

명령을 그대로 복사하기 전에 `--notes`를 자신이 관찰한 구체적인 수치와 해석으로 바꿉니다. 접수된 [개선점]을 먼저 저장·수정·재검증합니다. 미해결 개선점, 변경된 실행 코드, 손상된 산출물은 완료를 막습니다. 실행만으로 진도가 완료되지 않습니다. 완료 후 여기서 멈춥니다.

```bash
pal lesson review core-rl-01 --run-dir .local/runs/core-rl-01/baseline-01 --comparison-run-dir .local/runs/core-rl-01/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish core-rl-01 --run-dir .local/runs/core-rl-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-07](./core-fr3-07.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
