# Runbook — Isolated Robot Runtime

This mode can run on WS1 or an isolated WS2. Machine name does not grant permission; capabilities and safety gates do.

## Preconditions

- Ubuntu/vendor-supported runtime
- dedicated or explicitly validated robot network
- one active command authority
- training/Isaac batch jobs stopped on the same host
- candidate bundle and hash available
- physical E-stop and stop path verified

## Start

```text
git pull 이후 state/HOST_STATUS.md와 state/PROGRESS.md를 읽고 이 host를 ROBOT_RUNTIME mode로 전환할 준비를 audit해. development batch process, active GPU jobs, environment, NIC, command authority와 E-stop path를 확인하고 실제 command 없이 T35B offline replay/command-sink 단계까지만 진행해. 결과를 push할 때 현재 host 행을 non-secret summary로 갱신해.
```

## Preferred placement

- Use a dedicated or explicitly isolated runtime host.
- Private robot placement is defined only in its private overlay.
- Any placement must provide the same capability and safety evidence.

## Exit back to development

Disable control/torque, stop drivers, flush/hash recordings, detach robot command authority, deactivate runtime environment, and only then return to `DEVELOPMENT`. Do not automatically restart training.
