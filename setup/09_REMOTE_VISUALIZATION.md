# Remote Visualization and Control Plane

## Maintained setup instructions

Use the [English remote development guide](../docs/en/setup/remote-development/index.md)
or [한국어 원격 개발 가이드](../docs/ko/setup/remote-development/index.md).
Those pages own MacBook/WS1/WS2 and future Windows/Ubuntu laptop prompts,
Tailscale/OpenSSH configuration, both GNOME RDP modes, GPU tests, local result
records and reboot recovery. Preserve installed
environments and add only missing requirements.

## Laptop as development client

Start MacBook → WS1 → WS2, verifying each WS from MacBook after setup.
Future Windows/Ubuntu laptops use the same servers, with independent acceptance.
See [network/RDP](../docs/en/setup/remote-development/network-rdp.md),
[client alternatives](../docs/en/setup/remote-development/laptops.md) and
[record templates](../docs/en/setup/remote-development/records.md).

Use the laptop for:

- VS Code/Codex Remote SSH to WS2 and WS1
- Jupyter/metrics tunnels
- GNOME RDP Remote Login and Desktop Sharing over Tailscale
- Windows App (Mac), mstsc (Windows), or Remmina (Ubuntu)
- Version-matched NVIDIA WebRTC for Isaac when separately needed
- report, figure, video and dataset-manifest inspection
- Git and deployment-promotion review

SSH aliases are user-owned settings. Follow the maintained client guide for
host-key verification, conflict-safe merging and effective configuration checks.
The example names `ws1`/`ws2` do not override an existing alias for another host.

## Result handling

Persistent files under `outputs/`, `reports/`, and artifact manifests are canonical. Streaming windows are interactive convenience only.

Large artifacts may remain on WS2/WS1/NAS. Keep actual private paths/URIs and
hashes in local manifests; publish only redistributable, sanitized references.
Do not claim a remote result is available locally without checking.

## Safety boundary

Remote SSH from a laptop may launch simulation and inspect robot-runtime state. It must not bypass `$hardware-gate` or turn a client prompt into unrestricted remote motion authority.
