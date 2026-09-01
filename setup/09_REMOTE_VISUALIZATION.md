# Remote Visualization and Control Plane

## MacBook as cockpit

Use MacBook for:

- VS Code/Codex Remote SSH to WS2 and WS1
- Jupyter/metrics tunnels
- NVIDIA-supported WebRTC/browser streaming for Isaac
- report, figure, video and dataset-manifest inspection
- Git and deployment-promotion review

## Required SSH aliases

Codex should help create user-owned SSH config aliases without storing secrets in the repository.

```text
Host ws2
    HostName <ws2-address>
    User <user>

Host ws1
    HostName <ws1-address>
    User <user>
```

## Result handling

Persistent files under `outputs/`, `reports/`, and artifact manifests are canonical. Streaming windows are interactive convenience only.

Large artifacts may remain on WS2/WS1/NAS, but the repository must record immutable path/URI and hash. Do not claim a remote result is available locally without checking.

## Safety boundary

Remote SSH from MacBook may launch simulation and inspect robot-runtime state. It must not bypass `$hardware-gate` or turn a Mac prompt into unrestricted remote motion authority.
