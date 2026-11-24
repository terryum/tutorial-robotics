"""Design feedback and estimate state for the offline point-mass pendulum."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from matplotlib.figure import Figure
from scipy.linalg import expm, solve_discrete_are, solve_discrete_lyapunov

# Use the point-mass pendulum from arm.py, linearized about the downward equilibrium.
MASS_KG, LENGTH_M, DAMPING, GRAVITY = 1.0, 0.5, 0.12, 9.81
DT, DURATION = 0.02, 6.0
STEPS = round(DURATION / DT)
DROPOUT_START = 2.0


def pendulum_model():
    """Return discrete A and B for [angle, angular velocity] and held torque."""
    inertia = MASS_KG * LENGTH_M**2
    gravity_torque = MASS_KG * GRAVITY * LENGTH_M
    continuous_a = np.array([[0.0, 1.0], [-gravity_torque / inertia, -DAMPING / inertia]])
    continuous_b = np.array([[0.0], [1.0 / inertia]])

    # Exponentiate the joint state of the pendulum and its constant input.
    augmented = np.zeros((3, 3))
    augmented[:2, :2] = continuous_a
    augmented[:2, 2:] = continuous_b
    discrete = expm(DT * augmented)
    return discrete[:2, :2], discrete[:2, 2:]


def feedback_response(a, b, gain, q, input_weight, initial):
    """Simulate one controller and evaluate its infinite-horizon cost."""
    closed_loop = a - b @ gain
    radius = float(np.max(np.abs(np.linalg.eigvals(closed_loop))))
    if radius >= 1.0:
        raise RuntimeError("feedback is not asymptotically stable")

    states = np.empty((STEPS + 1, 2))
    states[0] = initial
    for k in range(STEPS):
        states[k + 1] = closed_loop @ states[k]
    torque = -(states @ gain.T)[:, 0]

    # For x[k+1] = F x[k], solve P = F.T @ P @ F + stage_weight.
    state_cost = solve_discrete_lyapunov(closed_loop.T, q)
    torque_cost = solve_discrete_lyapunov(closed_loop.T, input_weight * gain.T @ gain)
    state_cost_sum = float(initial @ state_cost @ initial)
    torque_cost_sum = float(initial @ torque_cost @ initial)
    outside_band = np.flatnonzero(np.any(np.abs(states) > [0.01, 0.05], axis=1))
    settling_step = int(outside_band[-1]) + 1  # The shared initial angle is outside the band.
    return (
        states,
        torque,
        {
            "gain": gain[0].tolist(),
            "spectral_radius": radius,
            "state_cost": state_cost_sum,
            "torque_cost": torque_cost_sum,
            "total_cost": state_cost_sum + torque_cost_sum,
            "peak_abs_torque_Nm": float(np.max(np.abs(torque))),
            "min_angle_rad": float(np.min(states[:, 0])),
            "settling_time_s": settling_step * DT if settling_step <= STEPS else None,
        },
    )


def lqr_experiment(a, b, time, input_weight):
    initial = np.array([0.2, 0.0])
    q = np.diag([20.0, 1.0])
    r = np.array([[input_weight]])
    p = solve_discrete_are(a, b, q, r)
    gain = np.linalg.solve(r + b.T @ p @ b, b.T @ p @ a)
    residual = a.T @ p @ a - a.T @ p @ b @ gain + q - p
    residual_norm = float(np.linalg.norm(residual))

    pd_states, pd_torque, pd = feedback_response(
        a, b, np.array([[3.0, 0.6]]), q, input_weight, initial
    )
    lqr_states, lqr_torque, lqr = feedback_response(a, b, gain, q, input_weight, initial)
    if residual_norm >= 1e-8 or lqr["total_cost"] > pd["total_cost"] + 1e-10:
        raise RuntimeError("Riccati residual or common-cost comparison failed")
    if not np.isclose(lqr["total_cost"], initial @ p @ initial, rtol=1e-10, atol=1e-10):
        raise RuntimeError("LQR cost disagrees with the Riccati solution")

    figure = Figure(figsize=(8, 6), layout="constrained")
    axes = figure.subplots(3, 1, sharex=True)
    for ax, pd_values, lqr_values, label in zip(
        axes,
        (*pd_states.T, pd_torque),
        (*lqr_states.T, lqr_torque),
        ("Angle (rad)", "Angular velocity (rad/s)", "Torque (N·m)"),
        strict=True,
    ):
        drawstyle = "steps-post" if ax is axes[-1] else "default"
        ax.plot(
            time,
            pd_values,
            label="Existing PD gains",
            color="#697484",
            linestyle="--",
            drawstyle=drawstyle,
        )
        ax.plot(time, lqr_values, label="LQR", color="#00615f", drawstyle=drawstyle)
        ax.set_ylabel(label)
        ax.grid(alpha=0.25)
    axes[0].legend(loc="upper right")
    axes[-1].set_xlabel("Time (s)")
    figure.suptitle(f"Feedback near the downward equilibrium · input weight R = {input_weight:g}")

    summary = {
        "initial_state": initial.tolist(),
        "state_weight_Q": q.tolist(),
        "input_weight_R": input_weight,
        "riccati_P": p.tolist(),
        "riccati_residual_frobenius": residual_norm,
        "settling_band": {"angle_rad": 0.01, "angular_velocity_rad_s": 0.05},
        "pd": pd,
        "lqr": lqr,
    }
    header = "time_s,pd_angle_rad,pd_velocity_rad_s,pd_torque_Nm,lqr_angle_rad,lqr_velocity_rad_s,lqr_torque_Nm"
    trace = np.column_stack((time, pd_states, pd_torque, lqr_states, lqr_torque))
    return summary, header, trace, figure


def kalman_experiment(a, b, time, dropout_seconds):
    seed = 17
    rng = np.random.default_rng(seed)
    h = np.array([[1.0, 0.0]])  # Observe angle only.
    process_std = np.array([0.0015, 0.015])
    process_covariance = np.diag(process_std**2)
    measurement_std = 0.03
    r = np.array([[measurement_std**2]])
    initial_covariance = np.diag([0.2**2, 0.5**2])
    true_state = np.empty((STEPS + 1, 2))
    true_state[0] = [0.2, 0.1]
    prediction_only = np.zeros_like(true_state)
    torque = 0.22 * np.sin(2 * np.pi * 0.55 * time)
    process_noise = rng.normal(scale=process_std, size=(STEPS, 2))
    measurement_noise = rng.normal(scale=measurement_std, size=STEPS + 1)
    for k in range(STEPS):
        known_input = b[:, 0] * torque[k]
        true_state[k + 1] = a @ true_state[k] + known_input + process_noise[k]
        prediction_only[k + 1] = a @ prediction_only[k] + known_input

    measurements = (true_state @ h.T)[:, 0] + measurement_noise
    first_missing = round(DROPOUT_START / DT)
    missing_count = round(dropout_seconds / DT)
    first_restored = first_missing + missing_count
    measurements[first_missing:first_restored] = np.nan

    estimates = np.empty_like(true_state)
    priors = np.empty_like(true_state)
    posterior_covariances = np.empty((STEPS + 1, 2, 2))
    prior_covariances = np.empty_like(posterior_covariances)
    estimate = prediction_only[0].copy()
    covariance = initial_covariance.copy()
    identity = np.eye(2)
    for k, measurement in enumerate(measurements):
        if k > 0:
            estimate = a @ estimate + b[:, 0] * torque[k - 1]
            covariance = a @ covariance @ a.T + process_covariance
        priors[k] = estimate
        prior_covariances[k] = covariance
        if np.isfinite(measurement):
            innovation_covariance = h @ covariance @ h.T + r
            gain = np.linalg.solve(innovation_covariance, h @ covariance).T
            estimate = estimate + gain @ (np.array([measurement]) - h @ estimate)
            # Joseph form retains symmetry and positive semidefiniteness in finite precision.
            correction = identity - gain @ h
            covariance = correction @ covariance @ correction.T + gain @ r @ gain.T
        estimates[k] = estimate
        posterior_covariances[k] = covariance

    missing = slice(first_missing, first_restored)
    if not (
        np.array_equal(estimates[missing], priors[missing])
        and np.array_equal(posterior_covariances[missing], prior_covariances[missing])
    ):
        raise RuntimeError("measurement correction was applied during a dropout")

    covariances = np.concatenate((prior_covariances, posterior_covariances))
    symmetry_error = float(np.max(np.abs(covariances - covariances.transpose(0, 2, 1))))
    minimum_eigenvalue = float(np.min(np.linalg.eigvalsh(covariances)))
    prediction_rmse = np.sqrt(np.mean((prediction_only - true_state) ** 2, axis=0))
    kalman_rmse = np.sqrt(np.mean((estimates - true_state) ** 2, axis=0))
    if symmetry_error > 1e-12 or minimum_eigenvalue < -1e-12:
        raise RuntimeError("invalid Kalman covariance")
    if np.any(kalman_rmse >= prediction_rmse):
        raise RuntimeError("Kalman RMSE did not improve on prediction alone")

    variances = np.diagonal(posterior_covariances, axis1=1, axis2=2)
    prior_variances = np.diagonal(prior_covariances, axis1=1, axis2=2)
    sigma = np.sqrt(variances)
    figure = Figure(figsize=(8, 7), layout="constrained")
    axes = figure.subplots(3, 1, sharex=True)
    for i, (ax, label) in enumerate(
        zip(axes[:2], ("Angle (rad)", "Angular velocity (rad/s)"), strict=True)
    ):
        ax.plot(time, true_state[:, i], label="Simulated truth", color="#1b2838")
        ax.plot(
            time, prediction_only[:, i], label="Prediction only", color="#b45819", linestyle="--"
        )
        ax.plot(time, estimates[:, i], label="Kalman estimate", color="#00615f")
        ax.set_ylabel(label)
    axes[0].scatter(time, measurements, s=7, alpha=0.55, label="Angle sensor", color="#7e56a5")
    axes[0].legend(loc="upper right", ncols=2)
    axes[2].plot(time, sigma[:, 0], color="#00615f")
    axes[2].set_ylabel("Angle σ (rad)", color="#00615f")
    velocity_axis = axes[2].twinx()
    velocity_axis.plot(time, sigma[:, 1], color="#7e56a5", linestyle="--")
    velocity_axis.set_ylabel("Velocity σ (rad/s)", color="#7e56a5")
    for ax in axes:
        if missing_count:
            ax.axvspan(
                time[first_missing], time[first_restored], color="#f2ce95", alpha=0.42, zorder=0
            )
        ax.grid(alpha=0.25)
    axes[-1].set_xlabel("Time (s)")
    figure.suptitle(f"State estimation with an angle sensor · dropout {dropout_seconds:g} s")

    summary = {
        "seed": seed,
        "true_initial_state": true_state[0].tolist(),
        "initial_prior_state": prediction_only[0].tolist(),
        "initial_prior_covariance": initial_covariance.tolist(),
        "observation_H": h.tolist(),
        "process_covariance": process_covariance.tolist(),
        "angle_sensor_std_rad": measurement_std,
        "dropout_start_s": DROPOUT_START,
        "dropout_duration_s": dropout_seconds,
        "missing_measurements": missing_count,
        "skipped_corrections_verified": True,
        "covariance_max_asymmetry": symmetry_error,
        "covariance_min_eigenvalue": minimum_eigenvalue,
        "prediction_only_rmse": prediction_rmse.tolist(),
        "kalman_rmse": kalman_rmse.tolist(),
        "std_before_dropout": sigma[first_missing - 1].tolist(),
        "std_at_last_missing_sample": sigma[first_restored - 1].tolist() if missing_count else None,
        "std_at_first_available_sample": sigma[first_restored].tolist(),
    }
    header = (
        "time_s,torque_Nm,true_angle_rad,true_velocity_rad_s,measured_angle_rad,"
        "measurement_used,prediction_only_angle_rad,prediction_only_velocity_rad_s,"
        "prior_angle_rad,prior_velocity_rad_s,kalman_angle_rad,kalman_velocity_rad_s,"
        "prior_angle_variance_rad2,prior_velocity_variance_rad2_s2,"
        "posterior_angle_variance_rad2,posterior_velocity_variance_rad2_s2"
    )
    trace = np.column_stack(
        (
            time,
            torque,
            true_state,
            measurements,
            np.isfinite(measurements),
            prediction_only,
            priors,
            estimates,
            prior_variances,
            variances,
        )
    )
    return summary, header, trace, figure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    lqr = subparsers.add_parser("lqr", help="compare LQR and PD with a common cost")
    lqr.add_argument("--input-weight", type=float, default=0.1, help="positive R (default: 0.1)")
    kalman = subparsers.add_parser("kalman", help="estimate state with an angle sensor")
    kalman.add_argument(
        "--dropout-seconds",
        type=float,
        default=0.5,
        help="outage at t=2 s, in 0.02 s steps (default: 0.5)",
    )
    for mode in (lqr, kalman):
        mode.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    a, b = pendulum_model()
    time = DT * np.arange(STEPS + 1)
    if args.mode == "lqr":
        if not math.isfinite(args.input_weight) or args.input_weight <= 0:
            lqr.error("--input-weight must be positive and finite")
        summary, header, trace, figure = lqr_experiment(a, b, time, args.input_weight)
    else:
        duration = args.dropout_seconds
        if not 0 <= duration <= DURATION - DROPOUT_START:
            kalman.error("--dropout-seconds must be in [0, 4]")
        if not math.isclose(duration, DT * round(duration / DT), rel_tol=0, abs_tol=1e-12):
            kalman.error("--dropout-seconds must be a multiple of 0.02 s")
        summary, header, trace, figure = kalman_experiment(a, b, time, duration)

    summary = {
        "status": "passed",
        "mode": args.mode,
        "dt_s": DT,
        "duration_s": DURATION,
        "discrete_A": a.tolist(),
        "discrete_B": b.tolist(),
        **summary,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.output_dir / "trace.csv", trace, delimiter=",", header=header, comments="")
    figure.savefig(args.output_dir / "plot.png", dpi=130)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{args.mode} passed: {args.output_dir / 'summary.json'}")


if __name__ == "__main__":
    main()
