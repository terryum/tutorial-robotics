<!-- pal:language:start -->
<p align="right">
  <a href="core-02.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-02 — 공개 로봇 소스 고정과 자산 매니페스트

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `T02` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

먼저 [개념 교재: simulation](../concepts/simulation.md)를 읽고, [장비를 늘리는 학습 순서](../equipment-stages.md)에서 이 수업의 실행 단계를 확인합니다.

## Learning goals

고정한 소스 커밋과 모델 파일이 같은지 확인합니다. 파일을 메모리에 복사해 한 바이트만 바꾸고 SHA-256 값을 비교하면, 모델 이름이 같아도 파일이 달라졌는지 알아낼 수 있습니다.

## Preflight

### 실행 전에 예측하기

파일의 길이와 나머지 바이트가 같고 첫 바이트만 달라질 때, 두 SHA-256 값이 일치할지 예측하세요.

에이전트는 [실행 안내](../READER_GUIDE.md#manual-setup)에 따라 Core 환경을 준비하고 확인합니다. 직접 실행할 때는 저장소 루트에서 `sh bootstrap.sh --plan`으로 계획을 읽고, 준비가 필요하면 `--apply`를 실행합니다. `source .venv/bin/activate`로 환경을 활성화한 뒤 아래 명령으로 준비 상태를 확인하세요. 이미 사용한 실행 폴더가 있으면 이름 끝에 `02`처럼 새 번호를 붙이세요. 아래 첫 명령 묶음으로 필요한 공개 모델을 준비합니다.

```bash
pal assets fetch mujoco-menagerie
pal assets fetch wuji-description-beta2
pal assets fetch flexiv-description
```

```bash
pal host detect --json
pal lesson check core-02 --json
```

## How it works

Git의 주석이 달린 태그(annotated tag)는 커밋을 바로 가리키는 대신 태그 객체를 가리킬 수 있습니다. 실험에서는 실제 커밋을 고정하고, 선택한 모델과 라이선스 파일의 바이트를 해시로 확인합니다. $b$는 파일의 바이트열이고 $h$는 SHA-256 해시입니다. 계산하면 256비트는 32바이트이고, 16진수로는 64자리입니다. 같은 내용이 들어 있는 파일은 같은 해시를 갖습니다. 이 검사로 파일 바이트가 바뀌었는지 확인합니다. 메시 파일이 바뀌면 같은 자세에서도 접촉이나 충돌 결과가 달라질 수 있습니다.

$$
h=\operatorname{SHA256}(b)
$$

## Code connection

[`examples/core-02/run.py`](../../../examples/core-02/run.py)에서 [`runner.py`](../../../src/pai_lab/lessons/runner.py)를 거쳐 [`physics.py`](../../../src/pai_lab/lessons/physics.py)로 이어집니다. [`models.provenance`](../../../src/pai_lab/lessons/models.py)는 `assets/model-lock.json`에 적힌 모델 파일의 SHA-256을 비교하고 누락되거나 바뀐 파일을 거부합니다. `physics.run`은 FR3·Wuji·Enlight·G1·Sharpa·ALOHA에서 고정 커밋과 라이선스, 파일 해시 집계값을 읽습니다.

## Action

에이전트가 아래 명령으로 기준 실행을 기록합니다.

```bash
pal lesson run core-02 --headless --seed 7 --samples 64 --output-dir .local/runs/core-02/baseline-01 --json
```

## Expected

여섯 공개 모델 캐시가 `assets/model-lock.json`과 일치해야 합니다. 다운로드 영수증은 체크아웃 밖에 남습니다. 아래 예시 그래프에서 1은 커밋 ID 길이가 40자인지 검사한 결과입니다. 고정 소스 전체에 대한 검사와는 별개입니다.

![core-02 measured plot](../../assets/examples/core-02-plot.png)

```bash
pal lesson check core-02 --run-dir .local/runs/core-02/baseline-01 --json
```

## Observe

`source-pins.json`의 `models`에서 `model`, `revision`, `license`, `files_digest`를 찾아보세요. 커밋 ID는 불러온 버전을, 라이선스는 재사용 조건을 알려 줍니다. `lesson inspect`로 실행 기록을 확인하고, 아래 명령으로 그래프와 원시 수치를 직접 열 수 있습니다.

```bash
pal lesson inspect core-02 --run-dir .local/runs/core-02/baseline-01 --json
```

```bash
open .local/runs/core-02/baseline-01/plot.png
```

```bash
python -m json.tool .local/runs/core-02/baseline-01/experiment.json
```

## Try it

코드는 저장소의 `assets/sources.json`을 바이트열로 읽고, 메모리에서 만든 복사본의 첫 바이트를 XOR 1로 바꿉니다. 원본 파일과 vendor 캐시는 그대로입니다. 한 번 실행하면 두 값이 `source-pins.json`의 `hash_comparison`에 함께 저장됩니다. 결과에서 `byte_offset`, `original_byte`, `changed_byte`로 바꾼 위치와 값을 확인하고 `original_sha256`과 `changed_sha256`을 대조하세요. 비교를 위해 seed를 바꾸거나 별도 실행을 만들 필요는 없습니다.

에이전트가 아래 명령으로 실행 기록을 검증해 결과 페이지를 만듭니다. 에이전트는 교재와 별도 창에 페이지를 열고 표시를 확인합니다. 별도 창을 띄우기 어려우면 결과 탭을 사용합니다. 화면을 제어할 수 없는 환경에서는 실제 측정값과 채팅에서 표시할 수 있는 이미지를 보여 줍니다.

```bash
pal lesson present core-02 --run-dir .local/runs/core-02/baseline-01 --language ko --json
```

## Recovery

`capability-unavailable`이 반환되면 에이전트는 `missing_capabilities` 또는 `error`에서 어떤 Python·모델·플랫폼·외부 스택이 필요한지 확인해 조치 방법을 안내합니다. 준비가 끝나면 새 폴더에서 같은 실험을 실행하고, 실패한 `run.json`과 수치를 보존합니다. 시스템 패키지·드라이버·CUDA·ROS·Isaac·대형 모델은 별도 준비가 필요합니다. 체크섬 오류가 나면 vendor 파일을 직접 수정하지 말고 고정 캐시를 복구합니다.

## Checkpoint

해시 일치로 어떤 사실을 확인할 수 있나요? 메모리에서 바꾼 바이트가 비교 결과의 어느 필드에 나타나는지 찾아보세요. 다음 수업에서는 파일을 읽어 모델을 컴파일하고 실제 구조를 확인합니다.

`lesson present`를 실행하면 에이전트가 이해 확인 대기 상태와 결과를 저장합니다. 새 대화에서도 같은 질문과 결과에서 이어갈 수 있습니다. 답을 함께 확인하거나 독자가 완료를 요청한 뒤에만 에이전트가 실제 관찰과 설명을 `--notes`에 적어 검토와 완료를 기록합니다. 피드백에 해결이 필요한 문제가 있으면 먼저 수정하고 재검증합니다. 변경된 실행 코드나 손상된 산출물은 완료를 막습니다.

```bash
pal lesson review core-02 --run-dir .local/runs/core-02/baseline-01 --notes "검사한 이름·단위·구조·제한과 실제 근거를 자신의 값으로 적으세요." --json
pal lesson finish core-02 --run-dir .local/runs/core-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-03](./core-03.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
