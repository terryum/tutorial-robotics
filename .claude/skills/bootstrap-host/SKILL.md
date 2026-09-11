---
name: bootstrap-host
description: Audit or provision only the requested environment while preserving local learner state.
---

Start with sh bootstrap.sh --plan, which works without Python/pal and writes no state. Show the smallest plan before applying it. Readiness-only requests stop after read-only checks; T00 remains pending.

Read [the common workflow](../../../agent/workflow.md). Learner state belongs only under ignored .local/. Never update shared progress or auto-commit it. System packages, GPU/ROS/Isaac, large models and real motion retain their explicit approval rules.
