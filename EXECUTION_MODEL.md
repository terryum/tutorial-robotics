# Execution model

The course is ordered by its prerequisite DAG and filtered by actual host capabilities. It never requires a MacBook before a workstation.

```text
catalog + local course selection + detected capabilities + safety state
                              ↓
                     next eligible lesson
```

- Stage 1 `core`: Python 3.12 on macOS arm64 or Linux. ROS 2 is not a prerequisite. FR3 Gym and episode data use dependency-light simulation contracts.
- Stage 2 `sim`: Ubuntu 24.04 x86_64. ROS 2, NVIDIA, and Isaac capabilities apply only to their matching tracks. `sim-deploy-01` uses a committed sample candidate and does not require every GPU track.
- Stage 3 `hardware`: isolated Ubuntu runtime. Complete `hw-common-01/02`, then only a robot track you own. The integrated Enlight+Wuji lesson requires both robots.

`pal host detect` records read-only host facts. Users may declare separately verified capabilities in `.local/capabilities.json`. `pal course next` checks stage scope, selected robots, electives, prerequisites, capabilities, and hardware safety requirements.

Learner progress and run artifacts remain in `.local/`. Repository publication evidence remains in `state/PUBLISHING.md`. Completing a lesson on one host does not imply another host has its dependencies, and `reader_test_required` never becomes verified merely because the dependency-light smoke passes.

Setup automation is intentionally limited to Python extras in an active project virtual environment. System packages, drivers, CUDA, ROS distributions, Isaac Sim, firmware, large models, and hardware motion require separate manual action and approval.
