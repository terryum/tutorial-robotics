---
name: run-next-tutorial
description: Guide one eligible lesson from local progress and capabilities, resuming pending comprehension.
---

Use `pal course next --json`. If comprehension is pending, use `pal course resume --json` and continue from the saved results and question. For a new lesson, follow the common workflow for prediction, baseline, validation, explanation and comparison. For `core-01`–`core-04`, present verified results and wait for the learner before review and finish.

Read [the common workflow](../../../agent/workflow.md). Learner state belongs only under ignored .local/. Never update shared progress or auto-commit it. System packages, GPU/ROS/Isaac, large models and real motion retain their explicit approval rules.
