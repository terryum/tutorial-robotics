[한국어](../../../ko/setup/remote-development/ubuntu.md) | [ENGLISH](../../../en/setup/remote-development/ubuntu.md)

# WS1 and WS2 Ubuntu incremental setup

Start with the appropriate WS prompt in the [overview](index.md). Run this common procedure independently on each machine; never copy another host's addresses, keys, GPU indices or virtual environments. Reading the guide alone does not authorize installation. On an execution request, show the necessary changes and carry them through installation and verification.

## 1. Identify the target and existing environments

| Logical role | Example SSH alias | Record directory | Example tmux session |
|---|---|---|---|
| WS1 | `ws1` | `.local/remote-development/ws1/` | `robotics-ws1` |
| WS2 | `ws2` | `.local/remote-development/ws2/` | `robotics-ws2` |

Match the user-supplied logical role to actual hostname, OS and user; do not rename the host. If records claim the opposite WS role, resolve target ambiguity. Both machines can train in **DEVELOPMENT**, but must not train concurrently with ROBOT_RUNTIME. Do not stop active robot services or other users' training; defer conflicting changes.

Read checkout/parent `AGENTS.md`, [host history](https://github.com/terryum/tutorial-robotics/blob/main/state/HOST_STATUS.md) and the relevant Ubuntu report. [WS1 history](https://github.com/terryum/tutorial-robotics/blob/main/setup/WS1_UBUNTU_VERIFICATION_2026-09-11.md) and [WS2 history](../../../WS2_UBUNTU_INSTALLATION_STATUS.md) are starting points, not current acceptance evidence. Windows/WSL results do not establish native Ubuntu readiness. If a private overlay exists, follow its Ubuntu handoff and pin checks separately.

Inspect Ubuntu/kernel/architecture, sudo availability, CPU/RAM, GPU/VRAM/driver and active processes, disk space/inodes, SSH/VPN/desktop/display manager, existing Python/uv/Conda, ROS, Isaac and Docker environments and locks. Read only relevant information; do not dump credentials or the entire environment.

Preserve working environments. Do not reinstall/upgrade the OS, bulk apt upgrade, purge drivers, format disks or create mounts. Show missing tools and proposed commands, and use normal permissions. Create records only for authorized installation; protect backups and real connection details with owner-only access.

## 2. Base tools and Codex

Compare installed packages and install only missing requirements available for the actual Ubuntu version. Base candidates are `openssh-server tmux git rsync curl ca-certificates unzip jq ripgrep python3-venv`. Add `git-lfs`, `build-essential`, `pkg-config`, `pciutils` and `ubuntu-drivers-common` only for selected project/diagnostic needs. Do not replace system Python or use `sudo pip`.

If uv is absent, use its [official user installation](https://docs.astral.sh/uv/getting-started/installation/). Do not convert existing Conda projects. Verify PATH in login shells and noninteractive SSH. Preserve global Git identity and remotes.

Follow [official Codex installation and remote authentication](index.md#when-codex-is-not-installed-yet), verifying version and login status. Do not clone or overwrite models, MCP, skills or managed policy. Do not bulk-install VS Code desktop or code-server on the WS.

## 3. OpenSSH and networking

1. Preserve the SSH port/configuration and install OpenSSH only if missing. Inspect Ubuntu's actual service/socket configuration and enable it at boot. Check syntax with `sudo sshd -t` before a necessary reload. Keep the old connection until a new one succeeds.
2. Add the MacBook public key once to the target account's `authorized_keys`, retaining existing entries. If no public key is available, leave only registration at `NEEDS_INPUT` and continue independent work.
3. Do not weaken root/password login or disable existing password access before testing key authentication. Allow only needed ports from actual trusted LAN/VPN networks or `tailscale0`. Do not reset/disable UFW, enable it without verifying access, or create router forwarding.
4. Keep the existing LAN/VPN recovery path and prepare [Tailscale](network-rdp.md) for off-site access after company permission and Personal eligibility checks. Verify boot service, tailnet policy, host firewall and expiry/recovery conditions. Use **OpenSSH over Tailscale**, not Tailscale SSH. Do not configure exit nodes/subnet routes or expose company/robot networks.
5. Obtain the SHA256 fingerprint of an active SSH public host-key file, for example `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256`. Confirm that key is enabled; otherwise select the actual public-key file. Do not read private host keys.

After reviewing missing packages and permissions, an example is `sudo apt install openssh-server tmux` **only if those are missing**. Inspect `systemctl status ssh.service ssh.socket --no-pager` and `systemctl is-enabled ssh.service ssh.socket` first. On a host using socket activation, enable its existing `ssh.socket`; on a service-based host, enable its existing `ssh.service` (`sudo systemctl enable --now ACTUAL_SSH_UNIT`). Do not enable both blindly or replace the configured port. Expected: the audited listener and a fresh key-authenticated connection work; recover via the retained session and backed-up configuration if they do not.

Write connection details, public fingerprints and project/Python paths into local `CLIENT-CONNECTION.md`. Until actual MacBook access, record `SSH_READY=PENDING: CLIENT_TEST_PENDING`. Teammates use their own accounts/keys. Management access does not justify exposing robot NICs or ROS DDS discovery externally.

## 4. GPU drivers and environment selection

Inspect actual `nvidia-smi` output even when RTX 5090 is expected. Record a different GPU without claiming 5090 acceptance. Do not replace a working driver merely for freshness. Only if a change is needed, consult [Ubuntu installation](https://ubuntu.com/server/docs/nvidia-drivers-installation/) and [NVIDIA kernel module support](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html), then propose a GPU-compatible package and rollback. Blackwell uses open kernel modules. Do not mix `.run` and APT installations; inspect Secure Boot/MOK needs first. Sources checked 2026-10-01; recheck at execution time.

The CUDA value in `nvidia-smi` describes driver support, not the PyTorch wheel runtime or a compilation Toolkit. Do not install the full Toolkit unless custom CUDA extension compilation requires it.

Select environments in this order:

1. Inspect the project's README, environment records and lock, then reuse its existing manager. Do not add GPU dependencies to the tutorial's Python 3.12 Core `.venv`.
2. Keep `gpu-mjlab`, `gpu-lerobot` and vendor/modern Isaac environments separate. Preserve existing Isaac, ROS and Docker; SSH setup is not a reason to reinstall them.
3. If no suitable GPU test environment exists, create an independent uv project at `gpu-smoke/` below the record directory. Start by checking Python 3.12 support for the selected PyTorch release. Do not change repository locks. The minimum dependency is CUDA `torch`; add compatible `torchvision`, Jupyter/TensorBoard only when the project needs them.
4. Check GPU architecture, driver, Python and project requirements against [official PyTorch installation](https://pytorch.org/get-started/locally/). [Blackwell/CUDA 12.8 introduction in 2.7](https://pytorch.org/blog/pytorch-2-7/) is historical context, not a mandated version. Do not copy old wheel/nightly recipes blindly.
5. For a new uv project, follow [official PyTorch index configuration](https://docs.astral.sh/uv/guides/integration/pytorch/) with a named CUDA index, `explicit = true` and `tool.uv.sources`. Record actual index URL/exact versions and run `uv lock`, `uv sync --locked`, `uv pip check` in that independent project. Preserve incompatible existing environments while isolating their problem elsewhere.

Prepare large models, datasets, Isaac/ROS distributions or containers only when needed and included in the installation request. Reading documentation does not trigger installation. Never copy `.venv` between framework environments.

## 5. Actual GPU and checkpoint tests

Write and run the test script below the record directory with the selected environment's Python. Check other GPU workloads and use small, short synthetic inputs. An absent GPU is `NOT_APPLICABLE`; a busy GPU that cannot safely be tested is `PENDING`.

1. Record Python path, torch/CUDA runtime versions, actual device name/capability/index/UUID locally. Check `torch.cuda.is_available()` and the model/tensor CUDA devices.
2. Run a small CUDA matrix multiply and Conv2d → loss → backward → optimizer.step in FP32. Use `torch.cuda.synchronize()` to expose asynchronous errors; check finite loss/gradients and changed parameters. CPU fallback and `no kernel image` are not success.
3. If supported, repeat with BF16 autocast; otherwise record the reason separately from FP32. Exercise a small synthetic DataLoader and relevant torchvision operations if installed. A single architecture string does not determine compatibility.
4. Save model, optimizer, step and used RNG states from one process and exit. In a second process, load this self-created checkpoint and verify increased steps and updated parameters. Loading a file alone is not resumed training.
5. Save `gpu-smoke-result.json` and logs. Retest affected environments after dependency changes. Container workloads require tests inside the container too.

These tests establish only GPU computation and continuation. ROS needs its lesson's DDS/record-replay checks; Isaac needs version-matched official smoke/example execution; mjlab/LeRobot need task-specific validation. Do not accept licenses/EULAs before the user reviews them.

## 6. Persistent work and results

Use the tmux session in the role table. Test a synthetic logging job across detach, SSH disconnection and reconnection. If logind policy terminates it, record the cause instead of unconditionally relaxing policy. A WS reboot ends tmux.

A launcher must preserve the actual working directory, Python/GPU selection, unique run directory, unbuffered logs and failing exit codes. Do not document nonexistent `train.py` commands. Training checkpoints retain used optimizer/scheduler/scaler/RNG state and preferably use a temporary file followed by atomic rename. Do not enable automatic training or robot control on boot by default.

If Jupyter/TensorBoard is needed, prepare it only in the selected environment and follow [MacBook tunneling](macbook.md). Keep loopback binding and Jupyter authentication. Exclude data, checkpoints, GPU UUIDs and real addresses from Git; whole-dataset replication requires a separate request.

## 7. Reuse existing RustDesk

Follow the [RustDesk audit and tests](rustdesk.md) first: version/build, service and boot state, Wayland/Xorg, ID/relay servers, authentication and active sessions. Preserve colleagues’ settings, passwords, server keys and running services; do not reinstall RustDesk. Reuse the existing connection route and keep Tailscale for SSH/development. Do not switch to direct-IP access or build a relay.

Missing functionality remains pending/failed while independent SSH/GPU work continues. No preview installation, Xorg switch, automatic login or forced session termination as a default fix. Test each WS from MacBook, then independently from future clients. `GUI_READY` follows `RUSTDESK_READY`; unattended access requires separate lock and reboot evidence. [GNOME RDP](network-rdp.md) is an optional supplement for unmet needs, excluded from default installation and acceptance. Preserve installed NoMachine.

## 8. Reboot and recovery

Before reboot, inspect active work/sessions, change impact/reason, `cat /proc/sys/kernel/random/boot_id`, SSH/VPN boot configuration, pre-login networking and suspend policy. If unattended access requires it, adjust only AC automatic suspend and preserve screen locking; do not mask every power target.

Check whether disk unlock, Secure Boot MOK enrollment or boot recovery needs local/BMC/PiKVM access. Defer reboot if that required route is unavailable. Do not change BIOS, encryption or Secure Boot arbitrarily. SSH changes must pass a separate new connection test first.

Write completed steps, backup/recovery commands, reconnect address, next GPU test command and guide path into `RESUME.md`. Present impact and recovery, then obtain only missing reboot approval; do not re-ask for the same approved reboot. Explain that the Codex session may end and do not promise automatic reconnection.

After reboot, reread this guide and verify changed boot ID, MacBook SSH/VS Code access without local login, `nvidia-smi` and the same environment's GPU/checkpoint tests. Verify RustDesk without local login and record lock/disconnect/monitor tests separately; record selected RDP modes independently. Resume real training manually after inspecting checkpoints. Retain `REBOOT_UNTESTED` when untested and `CLIENT_TEST_PENDING` for server-only evidence.

## 9. Closeout and next work

Use the [common result format](index.md#records-and-acceptance), securely passing only `CLIENT-CONNECTION.md` to the MacBook. Distinguish missing input, a different GPU, incomplete required GUI and untested reboot. New records do not overwrite historical success or other hosts' state. Setup does not automatically run lesson finish or hardware commands.

Before switching from development to robot runtime, clear training workloads and verify a separate runtime environment, isolated network, validated bundle, read-only checks and current-run approval. SSH access is not motion authority.
