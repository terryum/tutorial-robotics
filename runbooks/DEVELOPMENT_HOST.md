# Runbook — Any Development Host

MacBook and WS2 share this runbook. The host capability audit decides the runnable subset.

## Start

```text
이 checkout을 DEVELOPMENT mode로 사용한다. git pull 이후 EXECUTION_MODEL.md, AGENTS.md, state/HOST_STATUS.md와 state/PROGRESS.md를 읽고 $bootstrap-host를 실행해. shared progress를 존중하고 현재 capabilities로 가능한 다음 tutorial 하나만 완료해. 결과를 push할 때 현재 host 행도 같은 commit에서 갱신해.
```

## Rules

- A tutorial completed on another host stays done.
- Unsupported tutorials remain globally pending; do not create a host-specific shared status.
- Reconstruct local environments from committed specs; never copy another host's virtual environment.
- WS2 may run portable/core lessons and should preserve their small educational baseline before GPU scaling.
- Before switching hosts, complete one tutorial, generate report/state, and prepare one focused Git commit.
- Before any requested push containing tutorial or installation results, update
  the current row in `state/HOST_STATUS.md` and preserve every other host row.
