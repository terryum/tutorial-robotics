# hw-common-01 — 런타임 시작, 오프라인 재생과 명령 차단

이 수업은 **런타임 시작, 오프라인 재생과 명령 차단**을 `offline-command-sink` 구현과 `command-sink.json` artifact로 검사합니다.

| Field | Value |
|---|---|
| Stage / track | `hardware` / `common` |
| Legacy alias | `T35B` |
| Time / compute | 20–35 min / CPU smoke; external stack when noted |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `sim-deploy-01` |
| Safety | `read-only` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |

이 entrypoint는 명령을 전송하지 않는 offline/read-only 계약만 실행합니다. 실제 motion에는 새로운 실행 카드와 명시적 승인이 필요합니다.

## Learning goals

- capability와 선행 수업을 실행 전에 확인합니다.
- `offline-command-sink`이 만든 `command-sink.json`를 직접 검사합니다.
- 외부 GPU, ROS 2 또는 실제 장비 검증이 필요한 범위를 badge와 분리합니다.

## Preflight

```bash
pal host detect --json
pal setup verify --profile runtime-offline --json
pal lesson check hw-common-01 --json
```

## Action

```bash
pal lesson run hw-common-01 --headless --seed 7 --samples 64
```

The same thin entry point is available as `python examples/hw-common-01/run.py --headless`.

## Expected

`implemented` 수업은 exit code `0`과 함께 `command-sink.json`, `summary.json`, `trace.csv`, `lesson-report.md`를 생성합니다. scaffolded 수업은 exit code `2`와 `reader_test_required`를 반환하며 실행 artifact를 만들지 않습니다.

## Recovery

먼저 `pal lesson check hw-common-01 --json`을 실행합니다. capability가 없으면 `pal setup verify --profile runtime-offline --json`의 missing 목록을 따르고, 시스템 패키지나 firmware는 자동 설치하지 않습니다.

## How it works

runner는 catalog ID를 고유한 `offline-command-sink`에 dispatch하고 `emitted_command_count`을 계산합니다. 검사는 범용 성공 신호가 아니라 `command-sink.json`의 수업별 schema와 SHA-256을 사용합니다. 외부 runtime capability가 필요한 수업은 실제 host probe 없이 완료로 표시되지 않습니다.

Source references: `sample-candidate`. The source manifest owns external revisions; generated or cached vendor files are never edited in place.

## Try it

`pal lesson run hw-common-01 --headless --seed 8 --samples 96`로 seed와 표본 수를 바꿉니다. 새 artifact의 digest와 `changed_metric_value`가 달라지되 schema는 같아야 합니다.

## Checkpoint

`pal lesson check`는 양언어 heading, canonical 명령, entrypoint와 lesson별 test를 검사합니다. 출판 badge는 `maintainer-checked`이며 local 완료 여부와 독립적입니다.

Expected artifacts: `summary.json`, `trace.csv`, `command-sink.json`, `lesson-report.md`.

## Next lesson

과정의 다음 catalog 항목: [hw-common-02](./hw-common-02.md) — Real-hardware read-only integration gate
