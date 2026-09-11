# sim-isaac-02 — Isaac 카메라, 조명과 합성 데이터

이 수업은 **Isaac 카메라, 조명과 합성 데이터**을 `isaac-synthetic-data` 구현과 `synthetic-camera.json` artifact로 검사합니다.

| Field | Value |
|---|---|
| Stage / track | `sim` / `isaac` |
| Legacy alias | `T34` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `isaac-sim` |
| Prerequisites | `sim-isaac-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |

이 수업은 실제 하드웨어 명령을 전송하지 않습니다.

## Learning goals

- capability와 선행 수업을 실행 전에 확인합니다.
- `isaac-synthetic-data`이 만든 `synthetic-camera.json`를 직접 검사합니다.
- 외부 GPU, ROS 2 또는 실제 장비 검증이 필요한 범위를 badge와 분리합니다.

## Preflight

```bash
pal host detect --json
pal setup verify --profile isaac --json
pal lesson check sim-isaac-02 --json
```

## Action

```bash
pal lesson run sim-isaac-02 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/sim-isaac-02/run.py --headless`.

## Expected

`implemented` 수업은 exit code `0`과 함께 `synthetic-camera.json`, `summary.json`, `trace.csv`, `lesson-report.md`를 생성합니다. scaffolded 수업은 exit code `2`와 `reader_test_required`를 반환하며 실행 artifact를 만들지 않습니다.

## Recovery

먼저 `pal lesson check sim-isaac-02 --json`을 실행합니다. capability가 없으면 `pal setup verify --profile isaac --json`의 missing 목록을 따르고, 시스템 패키지나 firmware는 자동 설치하지 않습니다.

## How it works

runner는 catalog ID를 고유한 `isaac-synthetic-data`에 dispatch하고 `annotation_count`을 계산합니다. 검사는 범용 성공 신호가 아니라 `synthetic-camera.json`의 수업별 schema와 SHA-256을 사용합니다. 외부 runtime capability가 필요한 수업은 실제 host probe 없이 완료로 표시되지 않습니다.

Source references: `isaac-sim-ws`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

`pal lesson run sim-isaac-02 --headless --seed 8 --samples 96`로 seed와 표본 수를 바꿉니다. 새 artifact의 digest와 `changed_metric_value`가 달라지되 schema는 같아야 합니다.

## Checkpoint

`pal lesson check`는 양언어 heading, canonical 명령, entrypoint와 lesson별 test를 검사합니다. 출판 badge는 `reader_test_required`이며 local 완료 여부와 독립적입니다.

Expected artifacts: `summary.json`, `trace.csv`, `lesson-report.md`, `synthetic-camera.json`.

## Next lesson

과정의 다음 catalog 항목: [sim-cross-01](./sim-cross-01.md) — MuJoCo to Isaac sim-to-sim validation
