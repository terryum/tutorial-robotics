# Remote Visualization and Control Plane

## Maintained setup instructions

Use the [English remote development guide](../docs/en/setup/remote-development/index.md)
or [한국어 원격 개발 가이드](../docs/ko/setup/remote-development/index.md).
Those pages own the MacBook/WS1/WS2 prompts, SSH configuration, GPU tests,
optional GUI, local result records and reboot recovery. Preserve installed
environments and add only missing requirements.

## MacBook as cockpit

Use MacBook for:

- VS Code/Codex Remote SSH to WS2 and WS1
- Jupyter/metrics tunnels
- NVIDIA-supported WebRTC/browser streaming for Isaac
- report, figure, video and dataset-manifest inspection
- Git and deployment-promotion review

SSH aliases are user-owned settings. Follow the maintained MacBook guide for
host-key verification, conflict-safe merging and effective configuration checks.
The example names `ws1`/`ws2` do not override an existing alias for another host.

## Result handling

Persistent files under `outputs/`, `reports/`, and artifact manifests are canonical. Streaming windows are interactive convenience only.

Large artifacts may remain on WS2/WS1/NAS. Keep actual private paths/URIs and
hashes in local manifests; publish only redistributable, sanitized references.
Do not claim a remote result is available locally without checking.

## Safety boundary

Remote SSH from MacBook may launch simulation and inspect robot-runtime state. It must not bypass `$hardware-gate` or turn a Mac prompt into unrestricted remote motion authority.
