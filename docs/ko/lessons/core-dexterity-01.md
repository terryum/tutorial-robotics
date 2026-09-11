# core-dexterity-01 — Wuji와 Sharpa 모델 비교

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / dexterity` |
| Legacy alias | `T16` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-wuji-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

측정된 모델 속성으로 Wuji와 Sharpa를 비교합니다.

## Preflight

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

필요한 공개 모델을 한 번 준비합니다:

```bash
pal assets fetch wuji-description-beta2
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-dexterity-01 --json
```

## Action

```bash
pal lesson run core-dexterity-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-dexterity-01/baseline-01 --json
```

## Expected

값을 비교하기 전에 차원 이름을 읽습니다. 질량 단위는 kg이고 개수는 무차원입니다. 두 모델 모두 손끝 다섯 개를 제공해야 합니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check core-dexterity-01 --run-dir .local/runs/core-dexterity-01/baseline-01 --json
```

## How it works

관절 수·구동기 수·손끝 수·총질량은 서로 다른 비교 차원입니다. 관절 이름이 다르면 인덱스가 같아도 같은 관절이 아닙니다. 개수 비율은 구조 요약이며 정교함이나 파지 성능 점수가 아닙니다.

```text
count ratio = min(n_Wuji,n_Sharpa) / max(n_Wuji,n_Sharpa)
```

## Code connection

`examples/core-dexterity-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/hands.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

## Try it

seed를 7 → 8로 바꿉니다. 구조 검사·고정 모델 화면·결정론적 추론은 동일할 수 있습니다. 원격 서비스는 로컬 seed와 별개로 변할 수 있으므로 이 한계를 기록합니다.

```bash
pal lesson run core-dexterity-01 --headless --samples 64 --output-dir .local/runs/core-dexterity-01/comparison-01 --seed 8 --json
```

seed·표본 수·variant 중 위 명령의 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

## Recovery

capability-unavailable이면 missing 목록에 나온 Python·모델·플랫폼·외부 스택을 준비한 뒤 같은 수업을 새 폴더에서 재실행합니다. 실패한 run.json과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 자동 설치하지 않습니다. 체크섬 오류는 vendor 소스를 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

명령을 그대로 복사하기 전에 `--notes`를 자신이 관찰한 구체적인 수치와 해석으로 바꿉니다. 접수된 [개선점]을 먼저 저장·수정·재검증합니다. 미해결 개선점, 변경된 실행 코드, 손상된 산출물은 완료를 막습니다. 실행만으로 진도가 완료되지 않습니다. 완료 후 여기서 멈춥니다.

```bash
pal lesson review core-dexterity-01 --run-dir .local/runs/core-dexterity-01/baseline-01 --comparison-run-dir .local/runs/core-dexterity-01/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish core-dexterity-01 --run-dir .local/runs/core-dexterity-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-data-01](./core-data-01.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
