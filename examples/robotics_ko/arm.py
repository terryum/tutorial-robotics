"""Deterministic point-mass pendulum and collision-checked two-link arm."""

from __future__ import annotations

import argparse
import heapq
import json
import math
from itertools import pairwise
from pathlib import Path

import numpy as np

L1, L2 = 1.0, 1.0  # m
GRAVITY = 9.81  # m/s²
OBSTACLE = np.array([0.99, 0.70])  # m in the world frame
GRID_STEP_DEG = 5
GRID_STEP = np.deg2rad(GRID_STEP_DEG)
JOINT_LIMITS_DEG = ((-90, 90), (0, 180))
START_DEG, GOAL_DEG = (-45, 90), (45, 90)
CLEARANCE = 0.01  # m, required minimum throughout each segment
SPEED = 1.0  # rad/s per joint


def link_points(q):
    """Return the first-link endpoint and TCP in the world frame, in metres."""
    q1, q2 = np.moveaxis(q, -1, 0)
    elbow = L1 * np.stack((np.cos(q1), np.sin(q1)), axis=-1)
    tcp = elbow + L2 * np.stack((np.cos(q1 + q2), np.sin(q1 + q2)), axis=-1)
    return elbow, tcp


def solve_ik(target):
    """Return two elbow configurations for a nonsingular, reachable target."""
    x, y = target
    cosine = (x * x + y * y - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    if not -1 < cosine < 1:
        raise ValueError("IK example requires a nonsingular reachable target")
    q2 = np.array([np.arccos(cosine), -np.arccos(cosine)])
    q1 = np.arctan2(y, x) - np.arctan2(L2 * np.sin(q2), L1 + L2 * cosine)
    return np.column_stack((q1, q2))


def jacobian(q):
    """Map joint velocity (rad/s) to world-frame TCP velocity (m/s)."""
    q1, q2 = q
    distal_x = L2 * np.cos(q1 + q2)
    distal_y = L2 * np.sin(q1 + q2)
    return np.array(
        [
            [-L1 * np.sin(q1) - distal_y, -distal_y],
            [L1 * np.cos(q1) + distal_x, distal_x],
        ]
    )


def check_kinematics():
    target = np.array([1.0, 1.0])
    solutions = solve_ik(target)
    ik_error = np.linalg.norm(link_points(solutions)[1] - target, axis=1)
    q = np.deg2rad([30, 60])
    epsilon = 1e-6
    delta = epsilon * np.eye(2)
    finite_diff = ((link_points(q + delta)[1] - link_points(q - delta)[1]) / (2 * epsilon)).T
    analytic = jacobian(q)
    jac_error = float(np.max(np.abs(analytic - finite_diff)))
    determinants = [float(np.linalg.det(jacobian(np.deg2rad([30, q2])))) for q2 in (60, 30, 0)]
    if max(ik_error) >= 1e-12 or jac_error >= 1e-8 or abs(determinants[-1]) >= 1e-12:
        raise RuntimeError("kinematics verification failed")
    return {
        "status": "passed",
        "links_m": [L1, L2],
        "ik_goal_xy_m": target.tolist(),
        "ik_q_deg": np.rad2deg(solutions).tolist(),
        "ik_error_m": ik_error.tolist(),
        "jacobian_q_deg": [30, 60],
        "epsilon_rad": epsilon,
        "jacobian_m_per_rad": analytic.tolist(),
        "finite_difference_m_per_rad": finite_diff.tolist(),
        "jacobian_max_error_m_per_rad": jac_error,
        "determinant_q2_60_30_0_m2_per_rad2": determinants,
    }


def segment_distance(start, end):
    direction = end - start
    fraction = np.sum((OBSTACLE - start) * direction, axis=-1) / np.sum(direction**2, axis=-1)
    nearest = start + np.clip(fraction, 0, 1)[..., None] * direction
    return np.linalg.norm(OBSTACLE - nearest, axis=-1)


def link_clearance(q, radius):
    elbow, tcp = link_points(q)
    base = np.zeros_like(elbow)
    return np.minimum(segment_distance(base, elbow), segment_distance(elbow, tcp)) - radius


def certify_edge(start, end, radius):
    """Lower-bound the clearance of the entire linear segment in joint space."""
    dq = end - start
    bound = (L1 + L2) * abs(dq[0]) + L2 * abs(dq[1])
    intervals = 2 * max(1, math.ceil(bound / 0.03))
    fractions = np.linspace(0, 1, intervals + 1)
    sampled = float(np.min(link_clearance(start + fractions[:, None] * dq, radius)))
    return sampled, sampled - bound / (2 * intervals)


def grid_plan(radius):
    origin = np.deg2rad([joint[0] for joint in JOINT_LIMITS_DEG])
    size = [round((hi - lo) / GRID_STEP_DEG) + 1 for lo, hi in JOINT_LIMITS_DEG]
    start, goal = [
        tuple(round(value) for value in ((np.deg2rad(q) - origin) / GRID_STEP))
        for q in (START_DEG, GOAL_DEG)
    ]

    def pose(node):
        return origin + GRID_STEP * np.array(node)

    def estimate(node):
        return abs(goal[0] - node[0]) + abs(goal[1] - node[1])

    queue = [(estimate(start), 0, start)]
    distance = {start: 0}
    previous = {}
    while queue:
        _, cost, node = heapq.heappop(queue)
        if cost != distance[node]:
            continue
        if node == goal:
            nodes = [node]
            while node in previous:
                node = previous[node]
                nodes.append(node)
            return [pose(node) for node in reversed(nodes)]
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbor = node[0] + dx, node[1] + dy
            if not (0 <= neighbor[0] < size[0] and 0 <= neighbor[1] < size[1]):
                continue
            if cost + 1 >= distance.get(neighbor, math.inf):
                continue
            _, lower = certify_edge(pose(node), pose(neighbor), radius)
            if lower >= CLEARANCE:
                distance[neighbor] = cost + 1
                previous[neighbor] = node
                heapq.heappush(queue, (cost + 1 + estimate(neighbor), cost + 1, neighbor))
    return []


def shortcut(path, radius):
    reduced = [path[0]]
    index = 0
    while index < len(path) - 1:
        for candidate in range(len(path) - 1, index, -1):
            _, lower = certify_edge(path[index], path[candidate], radius)
            if lower >= CLEARANCE:
                reduced.append(path[candidate])
                index = candidate
                break
        else:
            raise RuntimeError("disconnected certified path")
    return np.array(reduced)


def trajectory(path):
    times = [0.0]
    poses = [path[0].tolist()]
    velocities = [[0.0, 0.0]]
    for start, end in pairwise(path):
        dq = end - start
        duration = 1.5 * float(np.max(np.abs(dq))) / SPEED
        elapsed = times[-1]
        for s in np.linspace(0, 1, 41)[1:]:
            times.append(elapsed + float(s * duration))
            poses.append((start + (3 * s**2 - 2 * s**3) * dq).tolist())
            velocities.append((6 * s * (1 - s) * dq / duration).tolist())
    return {
        "waypoint_q_deg": np.rad2deg(path).tolist(),
        "duration_s": times[-1],
        "speed_limit_rad_s": SPEED,
        "peak_speed_rad_s": float(np.max(np.abs(velocities))),
        "samples": [[t, *q, *v] for t, q, v in zip(times, poses, velocities, strict=True)],
        "sample_columns": ["time_s", "q1_rad", "q2_rad", "dq1_rad_s", "dq2_rad_s"],
    }


def check_planning(radius):
    start, goal = np.deg2rad([START_DEG, GOAL_DEG])
    start_clearance, goal_clearance = (
        float(c) for c in link_clearance(np.array([start, goal]), radius)
    )
    direct_sampled, direct_lower = certify_edge(start, goal, radius)
    result = {
        "obstacle_center_m": OBSTACLE.tolist(),
        "obstacle_radius_m": radius,
        "joint_limits_deg": JOINT_LIMITS_DEG,
        "start_q_deg": START_DEG,
        "goal_q_deg": GOAL_DEG,
        "start_clearance_m": start_clearance,
        "goal_clearance_m": goal_clearance,
        "direct_sampled_min_m": direct_sampled,
        "direct_clearance_lower_bound_m": direct_lower,
        "required_clearance_m": CLEARANCE,
    }
    if min(start_clearance, goal_clearance) < CLEARANCE:
        return {**result, "status": "blocked", "reason": "endpoint_below_required_clearance"}
    if direct_lower >= CLEARANCE:
        path = [start, goal]
    else:
        path = grid_plan(radius)
    if not path:
        return {**result, "status": "blocked", "reason": "no_certified_grid_path"}
    reduced = shortcut(path, radius)
    lower_bound = min(certify_edge(a, b, radius)[1] for a, b in pairwise(reduced))
    timed = trajectory(reduced)
    if lower_bound < CLEARANCE or timed["peak_speed_rad_s"] > SPEED + 1e-12:
        raise RuntimeError("trajectory verification failed")
    return {
        **result,
        "status": "passed",
        "grid_step_deg": GRID_STEP_DEG,
        "points_before_shortcuts": len(path),
        "route_clearance_lower_bound_m": lower_bound,
        **timed,
    }


def pendulum_feedback(kp):
    """Integrate a point-mass pendulum using semi-implicit Euler."""
    mass, length, damping = 1.0, 0.5, 0.12
    inertia = mass * length**2
    kd, target, dt = 0.6, 0.65, 0.002
    angle, velocity = 0.2, 0.0
    peak = angle
    gravity_scale = mass * GRAVITY * length
    for _ in range(3000):
        torque = gravity_scale * math.sin(target) + kp * (target - angle) - kd * velocity
        acceleration = (torque - damping * velocity - gravity_scale * math.sin(angle)) / inertia
        velocity += dt * acceleration
        angle += dt * velocity
        peak = max(peak, angle)
    error = abs(angle - target)
    if not math.isfinite(peak) or error >= 0.005 or abs(velocity) >= 0.005:
        raise RuntimeError("feedback convergence verification failed")
    return {
        "status": "passed",
        "kp_Nm_per_rad": kp,
        "kd_Nm_s_per_rad": kd,
        "point_mass_kg": mass,
        "length_m": length,
        "damping_Nm_s_per_rad": damping,
        "dt_s": dt,
        "duration_s": 3000 * dt,
        "initial_angle_rad": 0.2,
        "target_angle_rad": target,
        "final_angle_rad": angle,
        "final_velocity_rad_s": velocity,
        "final_error_rad": error,
        "overshoot_rad": peak - target,
    }


def arm_dynamics():
    """Compute inverse dynamics for point masses at the elbow and TCP."""
    m1, m2 = 0.7, 0.5
    q, velocity, acceleration = np.deg2rad([30, 60]), np.array([0.4, -0.2]), np.array([0.6, 0.3])

    def terms(position):
        j1 = np.array([[-L1 * np.sin(position[0]), 0], [L1 * np.cos(position[0]), 0]])
        j2 = jacobian(position)
        mass_matrix = m1 * (j1.T @ j1) + m2 * (j2.T @ j2)
        gravity = GRAVITY * (m1 * j1[1] + m2 * j2[1])
        return mass_matrix, gravity

    matrix, gravity = terms(q)
    coupling = m2 * L1 * L2 * np.sin(q[1])
    v1, v2 = velocity
    bias = coupling * np.array([-2 * v1 * v2 - v2**2, v1**2])
    torque = matrix @ acceleration + bias + gravity

    def energy(position, speed):
        inertia, _ = terms(position)
        elbow, tcp = link_points(position)
        return 0.5 * speed @ inertia @ speed + GRAVITY * (m1 * elbow[1] + m2 * tcp[1])

    epsilon = 1e-6
    power_fd = (
        energy(q + epsilon * velocity, velocity + epsilon * acceleration)
        - energy(q - epsilon * velocity, velocity - epsilon * acceleration)
    ) / (2 * epsilon)
    power = torque @ velocity
    error = abs(power_fd - power)
    if np.min(np.linalg.eigvalsh(matrix)) <= 0 or error >= 1e-7:
        raise RuntimeError("dynamics verification failed")
    return {
        "status": "passed",
        "point_masses_kg": [m1, m2],
        "q_deg": np.rad2deg(q).tolist(),
        "velocity_rad_s": velocity.tolist(),
        "acceleration_rad_s2": acceleration.tolist(),
        "mass_matrix_kg_m2": matrix.tolist(),
        "velocity_bias_Nm": bias.tolist(),
        "gravity_Nm": gravity.tolist(),
        "moving_torque_Nm": torque.tolist(),
        "hold_torque_Nm": gravity.tolist(),
        "power_W": float(power),
        "energy_derivative_W": float(power_fd),
        "power_balance_error_W": float(error),
    }


def draw_plan(planning):
    """Plot actual TCP positions and start/goal links, without an external renderer."""
    scale = 123

    def xy(points):
        return np.array([255, 247]) + scale * np.asarray(points) * np.array([1, -1])

    def points(coords):
        return " ".join(f"{x:.2f},{y:.2f}" for x, y in xy(coords))

    def polyline(coords, color, style=""):
        return (
            f'<polyline points="{points(coords)}" fill="none" stroke="{color}" '
            f'stroke-width="3" {style}/>'
        )

    x, y = xy(OBSTACLE)
    start, goal = np.deg2rad([START_DEG, GOAL_DEG])
    direct_q = np.linspace(start, goal, 101)
    direct = link_points(direct_q)[1]
    radius = planning["obstacle_radius_m"]
    clearance = link_clearance(direct_q, radius)
    witness = ""
    if np.min(clearance) < 0:
        elbow, tcp = link_points(direct_q[np.argmin(clearance)])
        witness = polyline([[0, 0], elbow, tcp], "#d95f49", 'stroke-dasharray="4 4"')
    route = ""
    if planning["status"] == "passed":
        samples = np.array(planning["samples"])
        route = polyline(link_points(samples[:, 1:3])[1], "#19726b")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 565 390" role="img"
aria-labelledby="arm-plan-title arm-plan-desc">
<title id="arm-plan-title">두 관절 팔의 충돌 검사와 우회 경로</title>
<desc id="arm-plan-desc">월드 좌표에서 두 TCP 경로와 출발·도착 자세를 표시합니다.
붉은 원판은 장애물입니다. 충돌이 있으면 해당 팔 자세도 붉은 점선으로 표시합니다.</desc>
<rect width="565" height="390" rx="14" fill="#f8fafb"/>
<path d="M24 247h512 M255 22v313" fill="none" stroke="#bdc7cd"/>
<circle cx="{x:.2f}" cy="{y:.2f}" r="{scale * radius:.2f}"
 fill="#f3c4ba" stroke="#aa3e2c" stroke-width="2"/>
{polyline(direct, "#aa3e2c", 'stroke-dasharray="7 5"')}
{route}
{witness}
{polyline([[0, 0], *link_points(start)], "#255494")}
{polyline([[0, 0], *link_points(goal)], "#575884")}
<circle cx="255" cy="247" r="5" fill="#27353c"/>
<g font-family="system-ui,sans-serif" font-size="14" fill="#27353c">
<text x="35" y="36" font-weight="bold">월드 좌표</text>
<text x="518" y="270">x (m)</text><text x="267" y="35">y (m)</text>
<text x="24" y="360" fill="#aa3e2c">붉은 점선 · 직접 보간과 충돌 자세</text>
<text x="24" y="380" fill="#19726b">녹색 · 검증된 TCP 경로</text>
<text x="310" y="380">파랑·보라 · 출발과 도착 자세</text>
</g></svg>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--obstacle-radius",
        type=float,
        default=0.12,
        metavar="M",
        help="radius of the world-frame obstacle in metres (default: 0.12)",
    )
    parser.add_argument(
        "--pendulum-kp",
        type=float,
        default=3.0,
        metavar="GAIN",
        help="pendulum proportional gain in N·m/rad (default: 3.0)",
    )
    args = parser.parse_args()
    if not 0 < args.obstacle_radius <= 2.0:
        parser.error("--obstacle-radius must be in (0, 2] m")
    if not 0 <= args.pendulum_kp <= 10.0:
        parser.error("--pendulum-kp must be in [0, 10]")
    result = {
        "pendulum_feedback": pendulum_feedback(args.pendulum_kp),
        "kinematics": check_kinematics(),
        "planning": check_planning(args.obstacle_radius),
        "dynamics": arm_dynamics(),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "arm.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    (args.output_dir / "arm.svg").write_text(draw_plan(result["planning"]), encoding="utf-8")


if __name__ == "__main__":
    main()
