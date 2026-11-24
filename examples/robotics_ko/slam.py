"""Two-dimensional LiDAR localization, occupancy mapping, and incremental SLAM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.optimize import least_squares
from scipy.spatial import cKDTree

DT = 0.20  # s per encoder update and instantaneous scan
WHEEL_RADIUS = 0.09  # m
TRACK = 0.36  # m between the wheels
CELL = 0.08  # m
BEAM_COUNT = 180
RANGE_MAX = 7.2  # m
ORIGIN = np.array([-1.0, -1.0])
START = np.array([1.10, 1.10, 0.0])  # surveyed initial position and heading
SHAPE = (100, 125)
ANGLES = np.linspace(-np.pi, np.pi, BEAM_COUNT, endpoint=False)
BEAMS = np.column_stack((np.cos(ANGLES), np.sin(ANGLES)))
RECTANGLES = (
    (0, 0, 8, 6),
    (2.45, 2.10, 3.20, 3.55),
    (5.05, 2.35, 5.75, 2.85),
    (4.15, 4.05, 4.70, 4.38),
)


def wall_segments():
    segments = []
    for x0, y0, x1, y1 in RECTANGLES:
        corners = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
        segments.extend(zip(corners, np.roll(corners, -1, axis=0), strict=True))
    return np.array(segments)


def rotate(points, yaw):
    c, s = np.cos(yaw), np.sin(yaw)
    return points @ np.array([[c, s], [-s, c]])


def world_points(pose, local):
    return rotate(local, pose[2]) + pose[:2]


def integrate(pose, wheels):
    distance = WHEEL_RADIUS * DT * (wheels[0] + wheels[1]) / 2
    turn = WHEEL_RADIUS * DT * (wheels[1] - wheels[0]) / TRACK
    # Exact constant wheel-speed integration, including the straight-line limit.
    arc = distance * np.sinc(turn / (2 * np.pi))
    mid = pose[2] + turn / 2
    return pose + np.array([arc * np.cos(mid), arc * np.sin(mid), turn])


def cross(a, b):
    return a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]


def scan(pose, walls, rng):
    direction = rotate(BEAMS, pose[2])
    a = walls[:, 0] - pose[:2]
    edge = walls[:, 1] - walls[:, 0]
    denominator = cross(direction[:, None, :], edge)
    parallel = np.abs(denominator) < 1e-12
    safe_denominator = np.where(parallel, 1.0, denominator)
    distance = cross(a, edge) / safe_denominator
    offset = cross(a, direction[:, None, :]) / safe_denominator
    valid = ~parallel & (distance > 0) & (offset >= 0) & (offset <= 1)
    first = np.where(valid, distance, np.inf).min(axis=1)
    hit = first < RANGE_MAX
    noisy = np.minimum(first, RANGE_MAX) + rng.normal(0, 0.006, BEAM_COUNT)
    return np.where(hit, np.clip(noisy, 0, RANGE_MAX), RANGE_MAX), hit


def simulate(walls, bias, seed):
    rng = np.random.default_rng(seed)
    truth = [START.copy()]
    wheel_log = [np.zeros(2)]
    for length in (5.56, 3.80, 5.56, 3.80):
        count = int(np.ceil(length / (0.9 * DT)))
        speed = length / (count * DT)
        for forward, yaw_rate, steps in ((speed, 0, count), (0, np.pi / (2 * 9 * DT), 9)):
            wheels = (
                np.array([forward - TRACK * yaw_rate / 2, forward + TRACK * yaw_rate / 2])
                / WHEEL_RADIUS
            )
            for _ in range(steps):
                truth.append(integrate(truth[-1], wheels))
                wheel_log.append(wheels * [1 - bias, 1 + bias] + rng.normal(0, 0.028, 2))
    ranges, hits = zip(*(scan(pose, walls, rng) for pose in truth), strict=True)
    return np.array(truth), np.array(wheel_log), np.array(ranges), np.array(hits)


def point_to_walls(points, walls):
    a = walls[:, 0]
    segments = walls[:, 1] - a
    relative = points[:, None, :] - a
    ratio = np.clip(np.sum(relative * segments, axis=-1) / np.sum(segments**2, axis=1), 0, 1)
    nearest = a + ratio[..., None] * segments
    return np.linalg.norm(points[:, None, :] - nearest, axis=-1).min(axis=1)


def localize(prior, local, known_walls):
    # An independent surveyed map is an input to localization.
    def residual(pose):
        return point_to_walls(world_points(pose, local), known_walls)

    return least_squares(residual, prior, loss="soft_l1", f_scale=0.045, max_nfev=25).x


class Occupancy:
    def __init__(self):
        self.log_odds = np.zeros(SHAPE, dtype=np.int16)

    def indices(self, points):
        xy = np.floor((points - ORIGIN) / CELL).astype(int)
        valid = ((xy >= 0) & (xy < [SHAPE[1], SHAPE[0]])).all(axis=1)
        return np.unique(np.ravel_multi_index((xy[valid, 1], xy[valid, 0]), SHAPE))

    def update(self, pose, ranges, hit):
        count = int(np.ceil(RANGE_MAX / (CELL / 3)))
        distances = np.arange(count) * (CELL / 3)
        free = distances[None, :] < (ranges - np.where(hit, CELL, 0.0))[:, None]
        vectors = (BEAMS[:, None, :] * distances[None, :, None])[free]
        empty_cells = self.indices(world_points(pose, vectors))
        filled_cells = self.indices(world_points(pose, (ranges[:, None] * BEAMS)[hit]))
        changed = self.log_odds.ravel()
        changed[empty_cells] -= 1
        changed[filled_cells] += 4
        np.clip(self.log_odds, -20, 20, out=self.log_odds)

    def hit_cells(self):
        return self.log_odds >= 4


class Submap:
    def __init__(self):
        self.points = []

    def update(self, points):
        # Keep sparse reference scans in the fixed frame established by START.
        self.points.append(points)

    def fit(self, prior, local):
        reference = np.concatenate(self.points)
        tree = cKDTree(reference)
        pose = prior.copy()
        # Estimate a local wall normal from the nearest existing map samples.
        for _ in range(6):
            transformed = world_points(pose, local)
            distance, neighbors = tree.query(transformed, k=8)
            safe = distance[:, 0] < 0.32
            if safe.sum() < 30:
                return pose
            targets = reference[neighbors[safe]]
            centers = targets.mean(axis=1)
            spread = targets - centers[:, None, :]
            variances, basis = np.linalg.eigh(spread.transpose(0, 2, 1) @ spread)
            walls = (variances[:, 0] < 0.18 * variances[:, 1]) & (variances[:, 1] > 1e-5)
            if walls.sum() < 25:
                return pose
            normals = basis[walls, :, 0]
            points = local[safe][walls]
            centers = centers[walls]

            optimized = least_squares(
                point_to_lines,
                pose,
                args=(points, centers, normals),
                loss="soft_l1",
                f_scale=0.035,
                max_nfev=10,
            ).x
            if np.linalg.norm(optimized - pose) < 1e-4:
                return optimized
            pose = optimized
        return pose


def point_to_lines(candidate, points, centers, normals):
    displacement = world_points(candidate, points) - centers
    return np.sum(displacement * normals, axis=1)


def estimate_localized(wheels, ranges, hits, known_walls):
    odometry = [START.copy()]
    localized = [START.copy()]
    for wheel, scan_ranges, hit in zip(wheels[1:], ranges[1:], hits[1:], strict=True):
        odometry.append(integrate(odometry[-1], wheel))
        local = (BEAMS * scan_ranges[:, None])[hit]
        localized.append(localize(integrate(localized[-1], wheel), local, known_walls))
    return np.array(odometry), np.array(localized)


def estimate_slam(wheels, ranges, hits):
    estimated = [START.copy()]
    submap, grid = Submap(), Occupancy()
    for i, (wheel, scan_ranges, hit) in enumerate(zip(wheels, ranges, hits, strict=True)):
        local = (BEAMS * scan_ranges[:, None])[hit]
        if i:
            prior = integrate(estimated[-1], wheel)
            estimated.append(submap.fit(prior, local))
        if i % 6 == 0:
            submap.update(world_points(estimated[-1], local))
        grid.update(estimated[-1], scan_ranges, hit)
    return np.array(estimated), grid


def infer_occupancy(poses, ranges, hits):
    grid = Occupancy()
    for pose, scan_ranges, hit in zip(poses, ranges, hits, strict=True):
        grid.update(pose, scan_ranges, hit)
    return grid


def wall_raster(walls):
    row, col = np.indices(SHAPE)
    centers = ORIGIN + CELL * (np.column_stack((col.ravel(), row.ravel())) + 0.5)
    return (point_to_walls(centers, walls) <= 0.55 * CELL).reshape(SHAPE)


def map_metrics(grid, expected):
    # Wall thickness and grid rounding can differ by one cell.
    wall = grid.hit_cells()
    precision = float(np.mean(distance_transform_edt(~expected)[wall] <= 1))
    recall = float(np.mean(distance_transform_edt(~wall)[expected] <= 1))
    return {
        "occupied_cells": int(wall.sum()),
        "wall_precision_1_cell": precision,
        "wall_recall_1_cell": recall,
        "wall_f1_1_cell": 2 * precision * recall / max(precision + recall, 1e-12),
        "exact_cell_iou": float((wall & expected).sum() / (wall | expected).sum()),
    }


def pose_metrics(truth, candidate):
    position_error = np.linalg.norm(truth[:, :2] - candidate[:, :2], axis=1)
    angle_error = (truth[:, 2] - candidate[:, 2] + np.pi) % (2 * np.pi) - np.pi
    return {
        "position_rmse_m": float(np.sqrt(np.mean(position_error**2))),
        "heading_rmse_deg": float(np.rad2deg(np.sqrt(np.mean(angle_error**2)))),
        "final_position_error_m": float(position_error[-1]),
    }


def write_figures(output, walls, trajectories, mapping_truth, mapping_slam, ranges, hits):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(11, 4), layout="constrained")
    for a, b in walls:
        axes[0].plot([a[0], b[0]], [a[1], b[1]], color="#8792a3", zorder=1)
    styles = ("#172235", "#d23c42", "#167dba", "#008563")
    for (name, values), color in zip(trajectories.items(), styles, strict=True):
        style = "-" if name in {"Truth", "Odometry"} else ":"
        axes[0].plot(*values[:, :2].T, label=name, zorder=2, color=color, linestyle=style)
    axes[0].legend(fontsize=7, loc="upper center")
    extent = [ORIGIN[0], ORIGIN[0] + CELL * SHAPE[1], ORIGIN[1], ORIGIN[1] + CELL * SHAPE[0]]
    for axis, grid, title in zip(
        axes[1:],
        (mapping_truth, mapping_slam),
        ("Mapping with known poses", "Incremental SLAM map"),
        strict=True,
    ):
        axis.imshow(grid.log_odds, cmap="gray_r", origin="lower", extent=extent, vmin=-20, vmax=20)
        axis.set_title(title, fontsize=10)
    for axis in axes:
        axis.set(xlabel="x (m)", ylabel="y (m)", aspect="equal", xlim=(-0.3, 8.3), ylim=(-0.3, 6.3))
    fig.savefig(output / "slam-map.png", dpi=130)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(6, 5), layout="constrained")
    endpoints = BEAMS * ranges[:, None]
    for endpoint in endpoints[::3]:
        axis.plot([0, endpoint[0]], [0, endpoint[1]], color="#9aabb7", alpha=0.30)
    axis.scatter(*endpoints[hits].T, color="#008563", s=10, label="Obstacle return")
    axis.scatter(*endpoints[~hits].T, color="#d23c42", s=20, marker="x", label="No return")
    axis.scatter(0, 0, color="#172235", marker=">", s=35, label="LiDAR at scan time")
    axis.set(xlabel="LiDAR x (m)", ylabel="LiDAR y (m)", aspect="equal")
    axis.legend(fontsize=8)
    fig.savefig(output / "slam-scan.png", dpi=140)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--encoder-bias", type=float, default=0.012)
    args = parser.parse_args()
    if not np.isfinite(args.encoder_bias) or abs(args.encoder_bias) > 0.03:
        parser.error("--encoder-bias must lie between -0.03 and 0.03")
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    walls = wall_segments()
    truth, wheels, ranges, hits = simulate(walls, args.encoder_bias, seed=7)
    odometry, localized = estimate_localized(wheels, ranges, hits, walls)
    mapping = infer_occupancy(truth, ranges, hits)  # known-pose exercise only
    estimated, slam = estimate_slam(wheels, ranges, hits)
    expected = wall_raster(walls)
    report = {
        "seed": 7,
        "encoder_bias": args.encoder_bias,
        "scan_count": len(ranges),
        "first_scan_hit_count": int(hits[0].sum()),
        "beam_count": BEAM_COUNT,
        "first_scan_nearest_m": float(ranges[0].min()),
        "range_max_m": RANGE_MAX,
        "time_step_s": DT,
        "cell_m": CELL,
        "odometry": pose_metrics(truth, odometry),
        "localization": pose_metrics(truth, localized),
        "mapping": map_metrics(mapping, expected),
        "slam": {**pose_metrics(truth, estimated), **map_metrics(slam, expected)},
        "thresholds": {
            "localization_rmse_m_max": 0.02,
            "slam_rmse_m_max": 0.05,
            "mapping_wall_f1_min": 0.9,
            "slam_wall_f1_min": 0.9,
            "mapping_exact_iou_min": 0.75,
            "slam_exact_iou_min": 0.75,
        },
    }
    thresholds = report["thresholds"]
    report["passed"] = (
        report["localization"]["position_rmse_m"] <= thresholds["localization_rmse_m_max"]
        and report["slam"]["position_rmse_m"] <= thresholds["slam_rmse_m_max"]
        and report["slam"]["position_rmse_m"] < report["odometry"]["position_rmse_m"]
        and report["mapping"]["wall_f1_1_cell"] >= thresholds["mapping_wall_f1_min"]
        and report["slam"]["wall_f1_1_cell"] >= thresholds["slam_wall_f1_min"]
        and report["mapping"]["exact_cell_iou"] >= thresholds["mapping_exact_iou_min"]
        and report["slam"]["exact_cell_iou"] >= thresholds["slam_exact_iou_min"]
    )
    (output / "slam.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    np.savez_compressed(
        output / "slam-trace.npz",
        time_s=DT * np.arange(len(truth)),
        truth=truth,
        wheels_rad_s=wheels,
        ranges_m=ranges,
        hit=hits,
        angles_rad=ANGLES,
        odometry=odometry,
        localized=localized,
        slam=estimated,
        map_truth_pose=mapping.log_odds,
        map_slam=slam.log_odds,
    )
    write_figures(
        output,
        walls,
        {"Truth": truth, "Odometry": odometry, "Known map": localized, "SLAM": estimated},
        mapping,
        slam,
        ranges[0],
        hits[0],
    )
    print(json.dumps(report, allow_nan=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
