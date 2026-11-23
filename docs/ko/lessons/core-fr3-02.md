<!-- pal:language:start -->
<p align="right">
  <a href="core-fr3-02.md" lang="ko">한국어</a> | <a href="../../en/lessons/core-fr3-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-fr3-02 — FR3 관절 공간 PD 제어

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `T06` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

이 수업의 질문은 아래 목표를 실행 결과의 값과 연결해 설명할 수 있는가입니다. 먼저 Expected의 결과 기준을 읽고 실행한 뒤, 관찰·계산·코드를 순서대로 확인합니다.

[터미널 준비·재개·결과 열기·카메라 조작](../READER_GUIDE.md)

[제어·접촉 개념](../concepts/control-contact.md)을 먼저 읽습니다. 질문은 “목표를 향해 당기는 힘을 키우면 왜 반드시 더 좋은 응답이 되지 않는가?”입니다. 위치 오차, 속도 감쇠, 토크 제한 세 가지를 분리해 읽어 보세요.

## Learning goals

FR3 동역학에 제한된 관절 PD 토크를 적용합니다.

## Preflight

장비 setup·매뉴얼 참조: [Franka Research 3](../setup/fr3.md).

처음이면 저장소 루트에서 `sh bootstrap.sh --plan`을 실행하고 계획을 읽은 뒤 `--apply`로 환경을 준비합니다. `source .venv/bin/activate` 후 아래 명령을 사용합니다. 이미 같은 이름의 실행 폴더가 있으면 02처럼 새 이름을 정합니다.

필요한 공개 모델을 한 번 준비합니다:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-fr3-02 --json
```

## Action

```bash
pal lesson run core-fr3-02 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-02/baseline-01 --json
```

## Expected

고정된 공개 모델로 실행해 검토한 예시입니다. 개인 실행 결과는 별도로 검사합니다.

![core-fr3-02 plot.png](../../assets/examples/core-fr3-02-plot.png)

첫 관절 목표를 0.18 rad 이동합니다. 첫 관절 오차는 0.02 rad 미만, 전체 팔 오차는 0.5 rad 미만이어야 합니다. 토크 포화와 중력에 의한 잔여 오차를 살펴봅니다.

공통 산출물은 summary.json, trace.csv, experiment.json, plot.png, run.json과 lesson-report.md입니다. 모델 수업에는 실제 frame.png 또는 외부 스택의 evaluation/isaac 이미지도 있습니다. 파일 크기만 보지 말고 그래프 축·단위·영상 구도를 직접 확인합니다.

```bash
pal lesson check core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --json
```

## Observe

먼저 metric의 단위, observed_first/observed_last, checks를 읽습니다. inspection은 검증된 파일만 읽고 종료하며 진도를 완료하지 않습니다.

```bash
pal lesson inspect core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --json
```

Mac 결과 그래프 열기(창을 닫아도 실행 기록은 유지됩니다):

```bash
open .local/runs/core-fr3-02/baseline-01/plot.png
```

다른 OS의 파일 관리자에서는 같은 PNG를 엽니다. 원시 수치는 아래 JSON에 있습니다.

```bash
python -m json.tool .local/runs/core-fr3-02/baseline-01/experiment.json
```

### 파일을 식의 각 항과 대응하기

| 파일·필드 | 읽을 값 | 해석 |
|---|---|---|
| `control.csv` | `time_s`, `joint`, `target_rad`, `q_rad`, `velocity_rad_s`, `requested_nm`, `applied_nm` | 한 제어 시점의 식 피연산자와 포화 전후 토크 |
| `experiment.json` → `payload` | `gain`, `kd`, `target_qpos`, `qpos`, `qvel`, `commanded_joint_error` | 이득과 상태, 첫 관절 최종 오차 |
| `trace.csv` | 세 번째 열 | 25회 적분마다 저장한 전체 팔 오차 노름(rad) |

CSV 헤더는 실제 파일에서 확인합니다. `control.csv`의 한 행에서 위치 오차와 감쇠 항을 계산해 `requested_nm`과 대조한 뒤 같은 행의 적용 토크와 비교하세요. 마지막 `torque_nm` 표본 하나만으로 전체 실행에 포화가 없었다고 결론 내릴 수 없습니다.

[과거 공개 검증](../../verification/reader-experience.md)은 이 수업의 전체 팔 오차 0.3376263 rad를 기록합니다. 당시 코드·variant 조건의 값이며 이번 실행의 측정값이나 첫 관절 오차가 아닙니다. 현재 실행은 자신의 산출물로 판정합니다.

## How it works

비례 토크는 위치 오차를 줄이고 미분 토크는 속도를 감쇠합니다. 여기서는 kp=120 Nm/rad, kd=2√kp Nms/rad입니다. 중력 보상 없이 정상상태 오차가 남으므로 지령을 준 첫 관절과 전체 팔 오차를 구분합니다.

$$
\tau_{raw}=K_p(q^*-q)-K_d\dot q,\qquad\tau=\operatorname{clip}(\tau_{raw},\tau_{min},\tau_{max})
$$

기호·단위·조건: q,q*: rad; qdot: rad/s; Kp: Nm/rad; Kd: Nm s/rad; 토크: Nm.

손으로 계산하는 예시(실행 측정값이 아님): 120 × 0.18 − 21.9089 × 0 = 21.6 Nm.

실전 연결: 하중의 중력은 잔여 오차를 만들며, 포화되면 이득 증가 효과도 제한됩니다.

### 오차 벡터에서 관절 토크까지

이 모델에서 관절 위치 $q$, 목표 $q^*$와 속도 $\dot q$는 각각 길이 7인 배열입니다. 식은 배열의 같은 관절끼리 원소별로 적용됩니다. 예를 들어 오차가 양수이고 정지해 있으면 비례 항은 양의 토크를 만듭니다. 목표로 움직이기 시작하면 $-K_d\dot q$가 그 움직임을 감쇠합니다. 감쇠 항은 목표까지의 거리 자체를 측정하지 않습니다.

0.18 rad는 약 10.3°이며 시뮬레이션의 목표 변화입니다. 첫 관절만 목표를 바꾸어도 중력과 관성 결합 때문에 다른 관절이 움직일 수 있습니다. 따라서 첫 관절의 절댓값 오차와 전체 팔의 $\|q^*-q\|_2$는 서로 다른 질문에 답합니다. 이 수업은 중력 보상 없이 PD를 관찰하고, 다음 수업에서 보상 항을 추가합니다.

### 포화된 구간의 해석

$\tau_{raw}$가 모델의 관절별 토크 한계를 넘으면 $\tau$만 동역학에 적용됩니다. 원시 토크가 계속 커져도 적용 토크가 같은 구간에서는 이득 증가가 같은 비율의 힘 증가로 이어지지 않습니다. 토크 한계는 로봇 모델에서 읽은 값이며 실물에서 승인한 한계가 아닙니다.

## Code connection

`examples/core-fr3-02/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. runner는 실행을 기록하고 실험 모듈이 실제 상태에서 수치를 계산합니다. `experiment.json`의 payload를 계산 코드와 대조합니다.

`arm_control`은 입력 목표를 만든 뒤 `gain * (target_q - data.qpos) - kd * data.qvel`을 계산합니다. `np.clip`으로 모델의 토크 범위를 적용해 `qfrc_applied`에 씁니다. 이 경로에서는 모델 actuator를 비활성화하므로 이 토크가 이중 적용되지 않습니다. `control.csv`는 mj_step **직전**의 시각·관절·목표·현재 위치·속도·토크를 저장합니다. `mj_step` 25회 뒤 `mj_forward`로 관측 위치를 갱신하고 전체 오차를 trace.csv에 기록합니다. 첫 번째 행의 21.6 Nm 계산을 직접 재현한 뒤 포화된 행을 찾으세요.

감쇠 규칙의 숫자 `2√kp`는 기준 관성 1 kg m²를 가정한 교육용 수치 규칙입니다. 일반 1자유도 임계 감쇠식은 $K_d=2\sqrt{I K_p}$이며, 실제 다관절 팔은 결합 관성과 하중 때문에 관절마다 임계 감쇠가 달라집니다.

## Try it

`kp`만 120 → 180 Nm/rad로 바꿉니다. `kd`는 21.9089 Nm s/rad로 유지합니다. 기존 `--variant 1.5`는 kp와 kd=2√kp 규칙을 함께 바꾸는 별도 실험입니다.

```bash
pal lesson run core-fr3-02 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-02/comparison-01 --param kp=180 --json
```

위 명령에서 지정한 이름 있는 파라미터 한 값만 바꿉니다. 기본 결과와 비교 결과의 수치·형상·한계를 설명합니다. 차이가 없으면 해당 변수가 이 실험에서 불변인 이유를 설명하고 성능 개선으로 꾸미지 않습니다.

```bash
pal lesson compare core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --comparison-run-dir .local/runs/core-fr3-02/comparison-01 --output-dir .local/comparisons/core-fr3-02/comparison-01 --json
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
pal lesson review core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --comparison-run-dir .local/runs/core-fr3-02/comparison-01 --notes "측정 결과와 한 변수 비교를 설명하고 그래프와 렌더링을 확인했습니다." --json
pal lesson finish core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --json
```

### 이해 확인

1. 목표에서 멀지만 이미 빠르게 움직이는 관절에서 두 토크 항의 부호는 어떻게 될까요?
2. 첫 관절 오차가 기준을 통과해도 전체 팔 오차를 따로 보는 이유는 무엇인가요?
3. `kp`를 180으로 바꾸고 `kd`를 고정하면 원시 토크·적용 토크·오차 곡선 중 무엇이 반드시 달라지고, 무엇은 포화 때문에 거의 같을 수 있나요?

답에는 `control.csv` 한 행의 계산과 최종 오차 두 종류를 포함합니다. 더 큰 이득만으로 실물 제어 적합성을 결론 내리지 않습니다.

답의 기준: 양의 위치 오차는 양의 비례 토크를 만들지만 양의 속도는 음의 감쇠 토크를 만듭니다. 전체 팔 노름은 첫 관절 외의 중력 처짐도 포함합니다. 초기 속도가 0이면 kp=180에서 첫 관절 원시 토크는 32.4 Nm로 계산되지만, 실제 적용값과 최종 응답은 제한과 동역학을 읽어 판단해야 합니다.

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-03](./core-fr3-03.md)

다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다.
<!-- pal:navigation:end -->
