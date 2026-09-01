"""Inspect the pinned Wuji Hand 2 MuJoCo contract."""

from __future__ import annotations

import argparse

import mujoco

from wuji_hand2_setup import WujiHand2MujocoBackend


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    args = parser.parse_args()

    backend = WujiHand2MujocoBackend(args.side)
    tip_sites = [
        mujoco.mj_id2name(backend.model, mujoco.mjtObj.mjOBJ_SITE, index)
        for index in range(backend.model.nsite)
        if (mujoco.mj_id2name(backend.model, mujoco.mjtObj.mjOBJ_SITE, index) or "").endswith("_tip")
    ]
    print(f"side={backend.side}")
    print(f"model={backend.model_path}")
    print(f"joints={backend.model.njnt} actuators={backend.model.nu} sites={backend.model.nsite}")
    print(f"control_dt={backend.control_dt:.4f}s")
    print(f"tip_sites={','.join(tip_sites)}")


if __name__ == "__main__":
    main()
