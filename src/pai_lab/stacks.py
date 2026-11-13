"""Isolated, pinned optional stacks. Verification never implies task performance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT
from pai_lab.local import write_json


def registry() -> dict[str, Any]:
    return dict(json.loads((ROOT / "setup/stack-lock.json").read_text()))


def run(command: list[str], **kwargs: Any) -> None:
    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        timeout=kwargs.pop("timeout", 3600),
        **kwargs,
    )


def paths(profile: str) -> tuple[Path, Path]:
    revision = registry()["profiles"][profile]["revision"]
    base = ROOT / ".local/stacks" / profile / revision
    return base / "source", base / "env"


def plan(profile: str) -> dict[str, Any]:
    item = registry()["profiles"][profile]
    source, env = paths(profile)
    supported = platform.system() == "Linux" and platform.machine() == "x86_64"
    return {
        "profile": profile,
        "supported": supported,
        "source": str(source),
        "environment": str(env),
        "lock": item,
        "status": "planned" if supported else "capability-unavailable",
        "managed_storage_limit_gb": registry()["budget"]["managed_storage_gb"],
        "system_changes": "audit required; no driver, reboot or EULA changes in this command",
        "model_weights": "separate revision-pinned download and inference acceptance required",
    }


def size_bytes(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file() and not p.is_symlink())


def apply(profile: str, accept_eula: bool = False) -> dict[str, Any]:
    result = plan(profile)
    if not result["supported"]:
        raise RuntimeError("optional GPU stacks require native Linux x86_64")
    if not shutil.which("uv") or not shutil.which("nvidia-smi"):
        raise RuntimeError("install uv and verify the NVIDIA driver first; see update runbook")
    if profile == "isaac-modern" and not accept_eula:
        raise RuntimeError("Isaac requires existing explicit user EULA consent; use --accept-eula")
    budget = int(result["managed_storage_limit_gb"]) * 1_000_000_000
    if (
        size_bytes(ROOT / ".local/stacks") >= budget
        or shutil.disk_usage(ROOT).free < 20_000_000_000
    ):
        raise RuntimeError(
            "storage budget exhausted or less than 20 GB free; preserve existing data"
        )
    item = result["lock"]
    source, env = paths(profile)
    source.parent.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        run(
            [
                "git",
                "clone",
                "--no-checkout",
                "https://github.com/" + item["repository"],
                str(source),
            ]
        )
        run(["git", "-C", str(source), "checkout", "--detach", item["revision"]])
        run(["git", "-C", str(source), "submodule", "update", "--init", "--recursive"])
    actual = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"], text=True)
    if actual != item["revision"] or dirty:
        raise RuntimeError("source revision/cleanliness mismatch; preserve source and investigate")
    variables = os.environ.copy()
    variables.update(UV_PROJECT_ENVIRONMENT=str(env), UV_LINK_MODE="copy", GIT_LFS_SKIP_SMUDGE="1")
    if accept_eula:
        variables.update(OMNI_KIT_ACCEPT_EULA="YES", ACCEPT_EULA="Y")
    command = [
        "uv",
        "sync",
        "--frozen",
        "--no-dev",
        "--python",
        item["python"],
        "--project",
        str(source),
    ]
    for extra in item["extras"]:
        command += ["--extra", extra]
    run(command, env=variables)
    if size_bytes(ROOT / ".local/stacks") > budget:
        raise RuntimeError(
            "post-install storage limit exceeded; no automatic deletion or promotion"
        )
    return verify(profile, accept_eula)


def verify(profile: str, accept_eula: bool = False) -> dict[str, Any]:
    source, env = paths(profile)
    python = env / "bin/python"
    result = plan(profile)
    if not result["supported"] or not python.is_file():
        return dict(result, status="capability-unavailable", ready=False)
    if profile == "isaac-modern" and not accept_eula:
        raise RuntimeError("Isaac launch requires explicit EULA consent; use --accept-eula")
    item = result["lock"]
    actual = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != item["revision"]:
        raise RuntimeError("source revision mismatch")
    run(["uv", "pip", "check", "--python", str(python)])
    run(
        [
            str(python),
            "-c",
            "import torch; assert torch.cuda.is_available(); x=torch.ones(8,device='cuda'); assert x.sum().item()==8; torch.cuda.synchronize()",
        ]
    )
    for check in item["verify"]:
        variables = os.environ.copy()
        if accept_eula:
            variables.update(OMNI_KIT_ACCEPT_EULA="YES", ACCEPT_EULA="Y")
        run([str(python), "-c", check], cwd=source, timeout=300, env=variables)
    result.update(
        status="runtime-smoke-passed",
        ready=True,
        model_inference_verified=False,
        training_verified=False,
        task_performance_verified=False,
    )
    result["lock_sha256"] = hashlib.sha256(
        (ROOT / "setup/stack-lock.json").read_bytes()
    ).hexdigest()
    write_json(env.parent / "runtime-verification.json", result)
    return result


def download(profile: str) -> dict[str, Any]:
    item = registry()["profiles"][profile]
    if "weights" not in item:
        raise RuntimeError("no revision-pinned weights for this profile")
    _, env = paths(profile)
    python = env / "bin/python"
    if not python.is_file():
        raise RuntimeError("install the isolated profile first")
    destination = env.parent / "weights"
    if size_bytes(ROOT / ".local/stacks") >= 300_000_000_000:
        raise RuntimeError("managed storage budget exhausted")
    code = (
        "from huggingface_hub import snapshot_download; "
        "snapshot_download(repo_id="
        + repr(item["weights"]["repository"])
        + ", revision="
        + repr(item["weights"]["revision"])
        + ", local_dir="
        + repr(str(destination))
        + ")"
    )
    run([str(python), "-c", code])
    result = {
        "profile": profile,
        "status": "weights-downloaded",
        "path": str(destination),
        "identity": item["weights"],
        "model_inference_verified": False,
    }
    write_json(env.parent / "weights-receipt.json", result)
    return result


def discover(profile: str) -> dict[str, Any]:
    item = registry()["profiles"][profile]
    endpoint = "https://api.github.com/repos/" + item["repository"] + "/commits/HEAD"
    with urllib.request.urlopen(endpoint, timeout=30) as response:
        candidate = json.load(response)["sha"]
    return {
        "profile": profile,
        "locked": item["revision"],
        "candidate": candidate,
        "adopted": False,
        "reason": "candidate needs isolated compatibility and GPU acceptance",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pal stack")
    parser.add_argument("operation", choices=("plan", "apply", "verify", "discover", "download"))
    parser.add_argument("--profile", required=True, choices=tuple(registry()["profiles"]))
    parser.add_argument("--accept-eula", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.operation == "apply":
            result = apply(args.profile, args.accept_eula)
        elif args.operation == "verify":
            result = verify(args.profile, args.accept_eula)
        else:
            result = {"plan": plan, "discover": discover, "download": download}[args.operation](
                args.profile
            )
        print(json.dumps(result, indent=2))
        return 2 if result.get("status") == "capability-unavailable" else 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "blocked", "profile": args.profile, "reason": str(error)}))
        return 2
