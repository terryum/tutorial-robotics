---
name: robotics-lesson-authoring
description: Write Korean and English robotics concepts, lesson explanations and reader guides grounded in implementation and evidence; excludes learner execution.
---

# robotics-lesson-authoring

Read `agent/book-contract.md`, assigned lesson specification, actual dispatch implementation/tests and relevant public verification. Read [authoring criteria](references/authoring.md), [terminology](references/glossary.md) and the appropriate [lesson template](assets/lesson.md) before drafting.

Draft Korean first in the assigned run output folder. Preserve existing H2 sections; expand with H3. Connect motivation/intuitions, necessary math, actual code, artifact interpretation, one-variable comparison and comprehension questions. Explain symbols, dimensions, units, frames and tensor shapes inline. Link the relevant concept chapter before using its assumptions. Preserve valid instructions and measured examples. Calculations are explicitly non-measured; new external results require evidence.

Read technical/reader feedback and fix source-grounded defects before English translation. Match goals, conditions, limitations, equations and numbers across languages; use shared glossary. Distinguish ACT contract, VLA mock, optimizer execution, independent policy performance and hardware readiness. Hardware scaffolds teach preparation and block execution; use paper comparisons rather than invented commands. WS labels never replace capabilities.

Return immutable drafts, source locations, observed checks and unresolved issues. No automatic lesson execution, device action or progress changes. Do not edit another worker's scope or generated common blocks. Main integrates after review.
