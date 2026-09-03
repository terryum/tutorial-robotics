# Public Source and Curriculum Alignment

## Authority and boundary

[`../references/PUBLIC_CURRICULUM.md`](../references/PUBLIC_CURRICULUM.md) is the
public conceptual baseline. Organization-specific robots, adapters, motion,
configuration, learning data, and hardware integration belong only in a private
sibling overlay. The public tutorial graph remains complete without that overlay.

## Public model roles

| Role | Model | Tutorial coverage |
|---|---|---|
| control reference | Franka Research 3 v2 | T05–T10, T22–T24 |
| humanoid learning reference | Unitree G1 29-DoF | T25–T26 |
| dexterous-hand target | Wuji Hand 2 Beta 2 | T14–T16A, T27, T38, T42A–T42B |
| dexterous comparison | Sharpa Wave | T16–T16A |
| bimanual imitation reference | ALOHA | T28–T30 |

## Learning progression

The prerequisite graph, rather than a fixed machine sequence, determines order.
Portable lessons establish deterministic MuJoCo, control, ROS 2, dataset, and
small-learning baselines. A compatible Linux GPU host then scales those same
ideas with CUDA and Isaac environments. Runtime lessons remain read-only until
their explicit safety gates and per-run approvals are satisfied.

Every source is pinned or recorded by manifest. Vendor repositories are treated
as read-only dependencies, and restricted assets are never redistributed.
