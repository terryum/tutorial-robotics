# WS2 Windows installation verification

Verified: 2026-09-07 18:05 KST. OS layer: Windows native. Mode: DEVELOPMENT.

## Result

**in-progress** overall. Installed software and prior simulation smoke evidence are verified; interactive device setup is incomplete. This is installation evidence, not tutorial completion.

| Check | Observed result |
|---|---|
| Scoped installer/package-manager process scan | None detected; no process stopped or installer restarted |
| Isaac Sim VERSION | `6.0.1-rc.7+release.42383.32955d8d.gl` from the 6.0.1 distribution |
| Existing bundled Python executable, `--version` | Python 3.12.13 |
| `nvidia-smi --query-gpu=name,driver_version --format=csv,noheader` | NVIDIA GeForce RTX 5090; driver 616.64 |
| Existing compatibility stdout log | `System checking result ... PASSED` matched |
| Existing simulation smoke log | `Hello World!` matched |

The log checks inspected previously generated evidence; the simulation was not rerun for this status update. Earlier execution completed successfully. Raw logs and installation paths remain local and are not committed.

## Read-only command evidence

Local path variables below denote the existing installation and ignored evidence directory. They are not new installation requests.

```powershell
Get-Content -LiteralPath (Join-Path $isaacRoot 'VERSION')
& $pythonExe --version
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
$compatibilityText = Get-Content -LiteralPath (Join-Path $logsRoot 'isaac-compatibility.stdout.log') -Raw
$helloText = Get-Content -LiteralPath (Join-Path $logsRoot 'isaac-hello-world.log') -Raw
$compatibilityText -match 'System checking result.*PASSED'
$helloText -match 'Hello World!'
Get-Process | Where-Object {
    $_.ProcessName -match '^(msiexec|winget|SteamSetup|OculusSetup|vivehub|ManusInstallerOffline|setup|installer|curl|tar)$'
} | Select-Object ProcessName,Id
```

The two log predicates returned True. The scoped process scan returned zero entries; this is not a claim that every system background updater is absent.

## Continuation

- Last successful step: installed-version audit and inspection of prior simulation evidence.
- Current blocker: interactive hardware setup and observations are incomplete, not a package installation failure.
- Next action: resume the existing hardware guide and confirm device readiness; do not reinstall from scratch.
- No Linux, WSL2, ROS 2, Isaac Lab, full development environment, or hardware readiness is inferred from Windows checks.
- Only the `WS2_WINDOWS` ledger row is updated. Other hosts and `state/PROGRESS.md` remain unchanged; T00 is pending.
- No configuration or dependency lock was changed for the Windows installation audit.
