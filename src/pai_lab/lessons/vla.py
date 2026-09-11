"""Prepared local SmolVLA fine-tuning and bounded inference transport."""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import numpy as np

from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.gpu import inputs, pinned_source
from pai_lab.local import write_json


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    import torch
    from PIL import Image

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    source = pinned_source("lerobot")
    import lerobot

    if not Path(lerobot.__file__).resolve().is_relative_to(source):
        raise FileNotFoundError("install the pinned LeRobot checkout in the selected environment")
    settings = inputs(identifier)
    if identifier == "sim-vla-02":
        endpoint = settings["endpoint"]
        if not endpoint.startswith("https://") and not endpoint.startswith("http://127.0.0.1:"):
            raise ValueError("remote endpoint must use HTTPS or loopback HTTP")
        request_file = Path(settings["request_file"])
        payload = request_file.read_bytes()
        started = time.monotonic()
        response = json.loads(
            urllib.request.urlopen(
                urllib.request.Request(endpoint, payload, {"Content-Type": "application/json"}),
                timeout=5,
            ).read(2_000_000)
        )
        actions = np.asarray(response["actions"], dtype=float)
        if actions.ndim != 2 or actions.shape[1] != int(settings["action_dimension"]):
            raise ValueError("remote action schema mismatch")
        return Experiment(
            [(float(i), 0.0, float(v)) for i, v in enumerate(actions.ravel())],
            float(time.monotonic() - started),
            {
                "actions": actions.tolist(),
                "request_sha256": hashlib.sha256(payload).hexdigest(),
                "command_sink": True,
                "transport": "HTTP JSON",
                "model_identity": response.get("model_identity"),
            },
            {
                "finite_actions": bool(np.isfinite(actions).all()),
                "bounded_actions": bool(np.max(np.abs(actions)) <= float(settings["action_limit"])),
            },
        )
    from lerobot.datasets.lerobot_dataset import LeRobotDataset
    from lerobot.policies.factory import make_pre_post_processors
    from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
    from torch.utils.data import DataLoader

    checkpoint = Path(settings["checkpoint"])
    dataset_root = Path(settings["dataset_root"])
    if not checkpoint.is_dir() or not (dataset_root / "meta/info.json").is_file():
        raise FileNotFoundError("prepare the local pretrained checkpoint and LeRobot dataset first")
    torch.manual_seed(seed)
    policy = SmolVLAPolicy.from_pretrained(str(checkpoint), local_files_only=True).to("cuda")
    policy.config.device = "cuda"
    metadata = json.loads((dataset_root / "meta/info.json").read_text())
    delta_timestamps = {"action": [i / metadata["fps"] for i in range(policy.config.chunk_size)]}
    dataset = LeRobotDataset(
        settings["dataset_repo_id"],
        root=dataset_root,
        delta_timestamps=delta_timestamps,
        download_videos=False,
    )
    preprocess, postprocess = make_pre_post_processors(
        policy.config, pretrained_path=str(checkpoint), dataset_stats=dataset.meta.stats
    )
    loader = DataLoader(dataset, batch_size=2, shuffle=False, num_workers=0)
    parameters = [p for p in policy.parameters() if p.requires_grad]
    initial = parameters[0].detach().clone()
    optimizer = torch.optim.AdamW(parameters, lr=1e-4 * variant)
    rows = []
    batch: Any = None
    policy.train()
    iterator = iter(loader)
    for step in range(max(2, min(16, samples // 8))):
        try:
            raw = next(iterator)
        except StopIteration:
            iterator = iter(loader)
            raw = next(iterator)
        batch = preprocess(raw)
        batch = {
            key: value.to("cuda") if torch.is_tensor(value) else value
            for key, value in batch.items()
        }
        optimizer.zero_grad()
        loss = policy(batch)["loss"]
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 10.0)
        optimizer.step()
        rows.append((float(step), 0.0, float(loss.detach().cpu())))
    delta = float((parameters[0] - initial).norm().detach().cpu())
    saved = output / "policy"
    policy.save_pretrained(saved)
    preprocess.save_pretrained(saved)
    postprocess.save_pretrained(saved)
    policy = SmolVLAPolicy.from_pretrained(str(saved), local_files_only=True).to("cuda").eval()
    tensor_batch = {
        key: value.detach().cpu().tolist() for key, value in batch.items() if torch.is_tensor(value)
    }
    dtypes = {key: value.dtype for key, value in batch.items() if torch.is_tensor(value)}
    for value in batch.values():
        if torch.is_tensor(value) and value.ndim == 4 and value.shape[1] == 3:
            pixels = np.clip(value[0].detach().cpu().permute(1, 2, 0).numpy() * 255, 0, 255).astype(
                np.uint8
            )
            Image.fromarray(pixels).save(output / "training-observation.png")
            break

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            pass

        def do_POST(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 20_000_000:
                self.send_error(400)
                return
            request = json.loads(self.rfile.read(length))
            observation = {
                key: torch.tensor(value, dtype=dtypes[key], device="cuda")
                for key, value in request["observation"].items()
            }
            with torch.inference_mode():
                policy.reset()
                action = postprocess(policy.select_action(observation)).cpu().tolist()
            encoded = json.dumps(
                {"actions": action, "model_identity": "local-finetuned-SmolVLA"}
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        body = json.dumps({"observation": tensor_batch}).encode()
        request = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}", body, {"Content-Type": "application/json"}
        )
        response = json.loads(urllib.request.urlopen(request, timeout=60).read())
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    write_json(output / "server-response.json", response)
    return Experiment(
        rows,
        rows[0][2] - rows[-1][2],
        {
            "parameter_delta": delta,
            "loss": [r[2] for r in rows],
            "server": "loopback HTTP",
            "action_shape": list(np.shape(response["actions"])),
            "performance_verified": False,
        },
        {
            "parameters_updated": delta > 0,
            "finite_loss": bool(np.isfinite(rows).all()),
            "real_server_inference": bool(np.isfinite(response["actions"]).all()),
        },
        files=["policy", "server-response.json", "training-observation.png"],
    )
