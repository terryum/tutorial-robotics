# sim-ros-02 — MuJoCo–ROS 2 브리지

이 수업에서는 **MuJoCo–ROS 2 브리지**의 재현 가능한 최소 기준선을 만들고, 상태·기준값·관측값의 흐름을 수치 artifact로 검사합니다.

| Field | Value |
|---|---|
| Stage / track | `sim` / `ros2` |
| Legacy alias | `T19` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `ros2-jazzy` |
| Prerequisites | `core-04`, `sim-ros-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |

이 수업은 실제 하드웨어 명령을 전송하지 않습니다.

## Learning goals

- capability와 선행 수업을 실행 전에 확인합니다.
- 고정 seed로 기준 trace를 만들고 SHA-256으로 기록합니다.
- 외부 GPU, ROS 2 또는 실제 장비 검증이 필요한 범위를 badge와 분리합니다.

## Preflight

```bash
pal host detect --json
pal setup verify --stage sim --json
pal lesson check sim-ros-02 --json
```

## Action

```bash
pal lesson run sim-ros-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-ros-02/run.py --headless`.

## Expected

exit code `0`과 함께 `summary.json`, `trace.csv`, `lesson-report.md`가 생성됩니다. `summary.json`의 `metric_value`는 유한하고 같은 seed에서 재현되어야 합니다.

## Recovery

먼저 `pal lesson check sim-ros-02 --json`을 실행합니다. capability가 없으면 `pal setup verify --stage sim --json`의 missing 목록을 따르고, 시스템 패키지나 firmware는 자동 설치하지 않습니다.

## How it works

공통 runner는 20 ms 간격의 정규화된 기준 신호와 관측 신호를 생성합니다. 평균 절대 추종 오차 $E=\frac{1}{N}\sum_i |r_i-y_i|$를 계산하고, CSV 바이트의 SHA-256을 checkpoint로 사용합니다. 이 값은 인터페이스와 재현성 smoke를 검증하며 실제 로봇 정확도나 센서 힘을 의미하지 않습니다.

Source references: `ros2-jazzy`, `mujoco-ros2-core`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

`pal lesson run sim-ros-02 --headless --seed 8 --samples 96`로 seed와 표본 수를 바꿉니다. 새 artifact의 digest와 `changed_metric_value`가 달라지되 schema는 같아야 합니다.

## Checkpoint

`pal lesson check`는 양언어 heading, canonical 명령, entrypoint와 lesson별 test를 검사합니다. 출판 badge는 `maintainer-checked`이며 local 완료 여부와 독립적입니다.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`.

## Next lesson

과정의 다음 catalog 항목: [sim-ros-03](./sim-ros-03.md) — Rosbag episode recording and deterministic replay
