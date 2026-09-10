# Tutorial Robotics agent workflow

1. Run `pal host detect --json` and inspect the result.
2. Run `pal setup plan --stage <stage> --out .local/setup-plan.json --json` and show the plan before applying it.
3. Never install `sudo` packages, GPU drivers, CUDA, ROS distributions, Isaac Sim, firmware, or large models automatically.
4. Initialize the requested course scope with `pal course init`, then use `pal course next --json`.
5. For one lesson, run `pal lesson check ID --json`, `pal lesson run ID --headless --json`, inspect all artifacts, and explain the data flow and `Try it` result.
6. Treat capability-unavailable as an honest result. Never turn it into a skip or success.
7. Before any real hardware interaction, use `pal hardware preflight ROBOT --read-only`. Do not emit motion, enable torque, update firmware, or alter limits without a fresh user-approved run card.
8. Keep machine state and learner progress under `.local/`; never commit serials, IPs, credentials, raw data, bags, or checkpoints.
