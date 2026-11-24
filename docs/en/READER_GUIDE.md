<!-- pal:language:start -->
<p align="right">
  <a href="../ko/READER_GUIDE.md" lang="ko">한국어</a> | <a href="READER_GUIDE.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

<a id="read-on-github-execute-in-your-terminal"></a>

# Learn through prompts with your AI agent

Use this guide to learn one lesson at a time by pasting prompts into Codex or Claude Code. The agent handles commands while you inspect theory, measured values and plots. Expand terminal references only for direct execution or troubleshooting. Dated installation reports do not establish current readiness.

## Start with Codex or Claude Code

**We recommend Codex or Claude Code.** Paste this sentence into the conversation; you do not need to learn terminal commands first.

```text
https://github.com/terryum/tutorial-robotics Clone this repository, install it, and help me start the tutorial.
```

The agent reuses an existing checkout or clones the repository when needed. It reads the repository instructions, checks the actual OS/environment, shows the smallest Core setup plan, and applies/verifies only the needed preparation. It preserves `.venv`, the lockfile and `.local/` progress. An existing environment that passes readiness verification on this host is reused without reinstalling. Unsupported environments or failed setup remain blocked with a concrete next action rather than a readiness claim.

If you have no completed or active learning lesson, the agent verifies readiness, gives the following invitation and **waits for your actual reply**. Learners with only a completed diagnostic also begin with the pendulum. If you have saved learning progress, the agent tells you the saved lesson and phase and asks whether to continue.

> The first tutorial is ready to open. Would you like to start?

The first lesson and its browser tab have not started yet. When ready, reply:

```text
Yes, start the first tutorial.
```

After your reply, the agent opens the [first pendulum lesson `core-01`](lessons/core-01.md) on GitHub in your selected language. It compares two starting angles, shows the results and asks a comprehension question. If browser control is unavailable, it shares the lesson link.

If you explicitly request a specific lesson, the agent verifies readiness and runs it. For a standalone environment check, request the [`core-00` (`T00`) diagnostic](lessons/core-00.md). Earlier `T00` records remain available. Diagnostics are excluded from learning progress.

## Prompts for learning sessions

### Next lesson

```text
Run the next eligible lesson only.
```

### Resume in a new chat

```text
https://github.com/terryum/tutorial-robotics I cleared the previous chat. Continue in the same existing checkout. Reread the repository instructions, curriculum/catalog.json and agent/workflow.md, then inspect .local/progress.json, .local/session.json, feedback and existing run evidence. Resume the last interrupted phase for one lesson without reinstalling, recloning or resetting progress.
```

### Rerun this lesson

```text
Rerun the current lesson. Preserve existing evidence and use a fresh run directory.
```

### Check progress

```text
Show my progress: completed lessons, current phase, remaining prerequisites and the next action.
```

### Pause

```text
Pause here and save the current lesson, explanation/comparison phase, run paths and next starting point.
```

### Questions and feedback

```text
[개선점] Explain the graph axes and units more simply.
```

<a id="manual-setup"></a>

## First setup — macOS Terminal, zsh

<details markdown="1">
<summary>Manual preparation and browser behavior reference</summary>

The initial language follows your Codex/Claude Code conversation. Select **한국어 | ENGLISH** at the top right of any curriculum page to open the same chapter in the other language. The Next lesson link stays in that language. When you ask the agent to continue, it reads the current tutorial tab's language and keeps it for the next page and explanation. Switch again using the links or explicitly request a language change in chat. If the tab is closed, the agent restores the last language it observed.

After you reply to start the first lesson, the agent opens the [English pendulum lesson on GitHub](https://github.com/terryum/tutorial-robotics/blob/main/docs/en/lessons/core-01.md). It creates one new tab if no tutorial tab exists, then navigates that same tutorial tab for subsequent lessons and reruns. Unrelated tabs stay untouched. If browser control is unavailable, the agent says so and provides the link for you to open manually.

Keep the Codex/Claude Code conversation and terminal on one side and the GitHub lesson on the other. Follow the agent's pointers to Expected, Observe and How it works to connect measured results to the theory. For a common foundation experiment, the agent opens the local result page in a separate window or result tab. Opening the theory page alone does not start a simulation.

Git retrieves pinned sources. Python runs the experiments. uv installs locked dependencies into `.venv`. MuJoCo provides dynamics and rendering; NumPy performs numerical calculations.

If no checkout exists, clone with `git clone https://github.com/terryum/tutorial-robotics.git` and use that directory. Reuse an existing checkout instead of cloning again. Use the repository root for all relative paths below. Adjust the first path if your checkout lives elsewhere.

```bash
cd ~/Codes/robotics/tutorial-robotics
```

```bash
sh bootstrap.sh --plan
```

This prints the OS, architecture, disk space, Python/uv status, environment path and proposed commands, then exits. If setup is needed, apply the minimal Core plan. Wait while dependencies download; preserve an error and reread the plan if installation fails.

```bash
sh bootstrap.sh --apply
```

```bash
source .venv/bin/activate
```

```bash
pal setup verify --profile core --json
```

Expect `ready: true`. Otherwise address missing_capabilities and rerun verify. CUDA, ROS and Isaac need their separately prepared lesson environments.

Only after choosing to start manually, continue with course selection below. Agent preparation does not automatically run init/next.

```bash
pal course init --json
```

```bash
pal course next --json
```

Select one eligible lesson. New learners and learners who have only completed the environment diagnostic start at `core-01`. Initializing preserves existing `completed` records.

</details>

## Resume in a new terminal

Clearing the conversation or opening a new chat does not remove the same checkout's files. Paste:

```text
https://github.com/terryum/tutorial-robotics I cleared the previous chat. Continue in the same existing checkout. Reread the repository instructions, curriculum/catalog.json and agent/workflow.md, then inspect .local/progress.json, .local/session.json, feedback and existing run evidence. Resume the last interrupted phase for one lesson without reinstalling, recloning or resetting progress.
```

The agent rereads the saved lesson and phase, then continues from existing evidence. If comprehension is pending, it reopens the same result and asks the saved question. If multiple checkouts make the destination ambiguous, identify the existing path to use. Progress files do not substitute for readiness on another host.

<details markdown="1">
<summary>Direct queries in a new terminal</summary>

Run `cd` and `source .venv/bin/activate` in each new terminal. Installation is not repeated.

Completed lessons and timestamps are saved in this clone's `.local/progress.json`.
The last lesson and phase are in `.local/session.json`, feedback in
`.local/feedback.json`, and execution/review evidence in `.local/runs/`.
They survive terminal restarts. Git ignores `.local/`, so your state is not shared
with other learners. Keep the same checkout and `.local/` to resume; a fresh clone
starts with no completed lessons.

```bash
pal course list --json
pal course next --json
```

`list` shows completed and incomplete learning lessons. `next` shows the next lesson to run.
The `status` command below shows only remaining or review-needed lessons.
Running `pal course init` again preserves completed records.

```bash
pal course status --json
```

```bash
pal feedback list --json
```

```bash
python -m json.tool .local/session.json
```

Read session.json after at least one execution. If it does not exist, start with `pal course next --json`. `pal: command not found` usually means activation is missing.

On another host, prepare locked sources and rerun verify there. Copying progress does not verify that environment. Preserve original evidence and use a fresh run directory.

</details>

## One lesson at a time

After your start or next-lesson prompt, the agent handles this sequence while you inspect the evidence and ask questions. Finishing one lesson does not automatically start another.

1. Read what you will learn and why. Predict the result before changing an input.
2. The agent traces the changed input and fixed conditions in the code, then runs the baseline under Action.
3. The agent checks the artifacts and values with `lesson inspect`. Find the axes and units you will use to check your prediction.
4. Change one input under Try it and read the effect. The hash and model dimension lessons record the comparison in a single run.
5. For the common foundations, the agent builds a page from verified runs with `pal lesson present`, opens it in a separate window from the lesson, and confirms the results display. If a separate window is unavailable, it opens a result tab. The page stays open until you close it or the agent recognizes the window it opened and replaces the result in the next lesson. If screen control is unavailable, the agent shares actual measurements and any images supported in chat. You can also open PNGs with macOS `open` or a file manager and read CSVs in a text editor.
6. The agent saves the result and question in the awaiting-comprehension phase. After discussing your answer or receiving your request to finish, it records progress with `lesson review` and `lesson finish`. Ask to start the next lesson when ready.

If baseline-01 exists, choose baseline-02. Never overwrite earlier evidence. Keep failed run.json receipts. Press Ctrl-C in the terminal to interrupt a running process.

## Model replay and Mac controls

```text
Show the saved model-state replay from this lesson and explain the joints and frames at the same timestamps as the graph.
```

Saved-state replay is not a new dynamics experiment. The agent checks that replay evidence exists and selects an appropriate viewer or image.

<details markdown="1">
<summary>Direct replay commands and Mac controls</summary>

For a lesson with saved model state, substitute its actual ID and run path:

```bash
mjpython -m pai_lab.cli lesson view core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01
```

The window replays once and exits. Add `--speed 0.25` for slower playback. Left-drag rotates, right-drag translates and scrolling zooms. Enable secondary click on a trackpad or begin with a mouse. Shift-drag selects horizontal movement. Match displayed axes to model joint/frame names. Closing the window stops replay.

Replay assigns saved qpos/qvel and calls `mj_forward`. It does not integrate dynamics with `mj_step` or produce new force/contact experiment evidence. Without a GUI, render the final saved state:

```bash
pal lesson view core-fr3-02 --run-dir .local/runs/core-fr3-02/baseline-01 --offscreen .local/pd-replay-01.png
```

Preserve older runs without replay files and create a fresh run. Binary replay models require the same MuJoCo version.

</details>

## Turn questions into teaching improvements

```text
[개선점] Explain the graph axes and units more simply.
```

The agent saves your original question, current lesson and observed values, then connects the explanation, documentation correction and verification. For an immediate fix, request:

```text
[개선점] 지금 바로 고쳐줘. The graph units are missing.
```

<details markdown="1">
<summary>Direct feedback recording commands</summary>

```bash
pal feedback add 'Original question; step: Observe; actual value; difference from expectation' --lesson core-fr3-02 --json
```

Resolve with `pal feedback resolve ID --evidence 'answer and cause; missing explanation; changed file; verification result; next starting point'`. Add reusable explanations to the lesson; keep personal execution data under `.local`. Developers select an independent session with `PAL_LOCAL_DIR` and never manufacture learner completion.

Math follows [GitHub mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). Mac replay follows the [MuJoCo passive viewer](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer).

</details>
