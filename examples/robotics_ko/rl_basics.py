"""Compare model-based value iteration and sample-based Q-learning on a 4x4 grid."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

SIZE = 4
STATE_COUNT = SIZE**2
START, GOAL, ROUGH = 12, 15, 13  # State index = row * SIZE + column.
OBSTACLES = (5, 6)
ACTIVE = [state for state in range(STATE_COUNT) if state not in (*OBSTACLES, GOAL)]
NAMES = ("north", "east", "south", "west")
DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
STEP_REWARD, GOAL_REWARD, STALL_PENALTY = -0.04, 1.0, 0.7
GAMMA = 0.95
SEEDS = (7, 21, 42)
SAMPLE_COUNT, CHECKPOINT = 120_000, 4_000
VISIT_RATE_POWER = 0.6
BELLMAN_TOLERANCE, RETURN_TOLERANCE = 1e-12, 0.02


def destinations():
    """Return the intended next state for every active state and action."""
    intended = np.zeros((STATE_COUNT, len(DIRECTIONS)), dtype=int)
    for state in ACTIVE:
        row, column = divmod(state, SIZE)
        for action, (dr, dc) in enumerate(DIRECTIONS):
            r, c = row + dr, column + dc
            target = r * SIZE + c
            if 0 <= r < SIZE and 0 <= c < SIZE and target not in OBSTACLES:
                intended[state, action] = target
            else:
                intended[state, action] = state
    return intended


def reward_table():
    reward = np.zeros((STATE_COUNT, STATE_COUNT))
    reward[ACTIVE] = STEP_REWARD
    reward[ACTIVE, GOAL] = GOAL_REWARD
    reward[ROUGH, ROUGH] -= STALL_PENALTY
    return reward


def transition_model(intended, slip_probability):
    """Build P[s, a, s_next], with zero outgoing mass at the goal and walls."""
    probability = np.zeros((STATE_COUNT, len(DIRECTIONS), STATE_COUNT))
    for state in ACTIVE:
        for action, target in enumerate(intended[state]):
            probability[state, action, target] += 1 - slip_probability
            probability[state, action, state] += slip_probability
    return probability


def bellman_backup(probability, rewards, values):
    return np.sum(probability * (rewards[:, None, :] + GAMMA * values), axis=2)


def value_iteration(probability, rewards):
    values = np.zeros(STATE_COUNT)
    for iteration in range(1, 1001):
        updated = bellman_backup(probability, rewards, values).max(axis=1)
        if np.max(np.abs(updated - values)) <= BELLMAN_TOLERANCE:
            action_values = bellman_backup(probability, rewards, updated)
            return updated, action_values, iteration
        values = updated
    raise RuntimeError("Value iteration did not converge")


def sample_transitions(intended, rewards, slip_probability, seed):
    """Query the simulator at uniformly sampled state-action pairs."""
    rng = np.random.default_rng(seed)
    states = rng.choice(ACTIVE, size=SAMPLE_COUNT)
    actions = rng.integers(len(DIRECTIONS), size=SAMPLE_COUNT)
    slips = rng.random(SAMPLE_COUNT) < slip_probability
    next_states = np.where(slips, states, intended[states, actions])
    return zip(states, actions, rewards[states, next_states], next_states, strict=True)


def q_learning(transitions):
    """Yield greedy policies from a stream of (state, action, reward, next_state)."""
    q = np.zeros((STATE_COUNT, len(DIRECTIONS)))
    visits = np.zeros_like(q, dtype=int)
    yield 0, q.argmax(axis=1)
    for count, (state, action, reward, following) in enumerate(transitions, start=1):
        # The goal's action values remain zero: it is never a queried state.
        target = reward + GAMMA * q[following].max()
        visits[state, action] += 1
        step_size = float(visits[state, action]) ** -VISIT_RATE_POWER
        q[state, action] += step_size * (target - q[state, action])
        if count % CHECKPOINT == 0 or count == SAMPLE_COUNT:
            yield count, q.argmax(axis=1)


def evaluate_policy(probability, rewards, policy):
    """Compute the expected discounted return without reusing training samples."""
    transition = probability[np.arange(STATE_COUNT), policy]
    expected_reward = np.sum(transition * rewards, axis=1)
    return np.linalg.solve(np.eye(STATE_COUNT) - GAMMA * transition, expected_reward)


def policy_grid(policy):
    cells = [NAMES[action] for action in policy]
    for state in OBSTACLES:
        cells[state] = "wall"
    cells[GOAL] = "goal"
    return [cells[row : row + SIZE] for row in range(0, STATE_COUNT, SIZE)]


def write_figure(output, slip_probability, optimal_policy, learned_policy, reference, trace):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, axes = plt.subplot_mosaic(
        [["optimal", "learned"], ["return", "return"]],
        figsize=(7.4, 6.8),
        layout="constrained",
    )
    fig.suptitle(f"Gridworld with {slip_probability:.0%} slip probability")
    for key, title, policy in (
        ("optimal", "Value iteration", optimal_policy),
        ("learned", f"Q-learning (seed {SEEDS[0]})", learned_policy),
    ):
        ax = axes[key]
        ax.set(title=title, xlim=(0, SIZE), ylim=(SIZE, 0), aspect="equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for state, label in enumerate(label for row in policy for label in row):
            row, col = divmod(state, SIZE)
            color = {START: "#d7eefe", GOAL: "#ccebd9", ROUGH: "#ffe6ad"}.get(state, "white")
            if label == "wall":
                color = "#253441"
            ax.add_patch(Rectangle((col, row), 1, 1, facecolor=color, edgecolor="#71818e"))
            if label in NAMES:
                dr, dc = DIRECTIONS[NAMES.index(label)]
                ax.annotate(
                    "",
                    xy=(col + 0.50 + dc * 0.22, row + 0.49 + dr * 0.22),
                    xytext=(col + 0.50 - dc * 0.16, row + 0.49 - dr * 0.16),
                    arrowprops={"arrowstyle": "-|>", "color": "#24313c", "lw": 1.5},
                )
            marker = {START: "Start", GOAL: "Goal", ROUGH: "Rough"}.get(state)
            if marker:
                ax.text(col + 0.5, row + 0.10, marker, ha="center", va="top", fontsize=8)

    ax = axes["return"]
    ax.axhline(reference, color="#24313c", linestyle="--", label="Value iteration")
    for seed, color in zip(SEEDS, ("#1767b2", "#bd4624", "#22744e"), strict=True):
        rows = [(count, value) for row_seed, count, value in trace if row_seed == seed]
        ax.plot(*zip(*rows, strict=True), color=color, alpha=0.82, label=f"Seed {seed}")
    ax.set(xlabel="Training transitions", ylabel="Expected return from start")
    ax.grid(alpha=0.2)
    ax.legend(loc="lower right", ncols=2, fontsize=8)
    fig.savefig(output / "rl-basics.png", dpi=140)
    plt.close(fig)


def run(output, slip_probability):
    intended, rewards = destinations(), reward_table()
    probability = transition_model(intended, slip_probability)
    values, action_values, iterations = value_iteration(probability, rewards)
    residual = float(np.max(np.abs(action_values.max(axis=1) - values)))
    optimal_policy = action_values.argmax(axis=1)
    reference = float(values[START])
    trace = []
    learned = []
    for seed in SEEDS:
        transitions = sample_transitions(intended, rewards, slip_probability, seed)
        for count, policy in q_learning(transitions):
            start_return = float(evaluate_policy(probability, rewards, policy)[START])
            trace.append((seed, count, start_return))
        learned.append(
            {
                "seed": seed,
                "start_return": start_return,
                "start_action": NAMES[policy[START]],
                "absolute_start_gap": abs(reference - start_return),
                "policy": policy_grid(policy),
            }
        )

    report = {
        "slip_probability": slip_probability,
        "grid_size": SIZE,
        "start": divmod(START, SIZE),
        "goal": divmod(GOAL, SIZE),
        "rough": divmod(ROUGH, SIZE),
        "obstacles": [divmod(state, SIZE) for state in OBSTACLES],
        "step_reward": STEP_REWARD,
        "goal_reward": GOAL_REWARD,
        "rough_stall_penalty": STALL_PENALTY,
        "discount": GAMMA,
        "reference": {
            "start_return": reference,
            "start_action": NAMES[optimal_policy[START]],
            "start_action_values": dict(zip(NAMES, action_values[START].tolist(), strict=True)),
            "iterations": iterations,
            "bellman_residual": residual,
            "policy": policy_grid(optimal_policy),
        },
        "training_samples_per_seed": SAMPLE_COUNT,
        "visit_rate_power": VISIT_RATE_POWER,
        "learned": learned,
        "return_tolerance": RETURN_TOLERANCE,
        "passed": residual <= BELLMAN_TOLERANCE
        and all(row["absolute_start_gap"] <= RETURN_TOLERANCE for row in learned),
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "rl-basics.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    with (output / "rl-basics-trace.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("seed", "training_transitions", "start_return"))
        writer.writerows(trace)
    write_figure(
        output,
        slip_probability,
        report["reference"]["policy"],
        learned[0]["policy"],
        reference,
        trace,
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--slip-probability", type=float, default=0.1)
    args = parser.parse_args()
    if not 0 <= args.slip_probability <= 1:
        parser.error("--slip-probability must lie between 0 and 1")
    report = run(args.output_dir, args.slip_probability)
    print(json.dumps(report, allow_nan=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
