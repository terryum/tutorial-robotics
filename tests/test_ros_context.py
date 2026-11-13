"""Native Jazzy regression: service/action spins must use the lesson context."""

import pytest


@pytest.mark.parametrize("lesson", ["sim-ros-01", "sim-ros-03"])
def test_ros_lesson_context_can_run_and_close_twice(lesson, tmp_path):
    pytest.importorskip("rclpy", reason="native ROS 2 Jazzy environment required")
    from pai_lab.lessons.ros import run

    for attempt in range(2):
        output = tmp_path / str(attempt)
        output.mkdir()
        result = run(lesson, output, seed=7, samples=8)
        assert all(result.checks.values()), result.checks
        assert result.metric == 0.0
        assert len(result.rows) == 8
