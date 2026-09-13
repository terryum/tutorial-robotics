# Claude Code instructions

Read `agent/workflow.md`, `curriculum/catalog.json`, and the selected bilingual lesson before acting. Use `.claude/skills/tutorial-robotics/SKILL.md` for orchestration. `pal` is authoritative for host detection, setup planning, lesson selection, execution, and read-only hardware preflight.

Never install system packages, drivers, CUDA, ROS distributions, Isaac Sim, firmware, or large models automatically. Never actuate hardware without a fresh explicit approval and run card.

Start guided learning by opening the current lesson's GitHub page in the reader's language. Reuse the same tutorial tab for subsequent lessons and reruns, following the companion-tab instructions in `agent/workflow.md`. Include the lesson link in the opening explanation; report unavailable browser control honestly.

Initialize the lesson language from the conversation. Before subsequent navigation, preserve the language currently selected in the tutorial tab, including manual 한국어/ENGLISH switches; follow the language continuity rules in `agent/workflow.md`.
