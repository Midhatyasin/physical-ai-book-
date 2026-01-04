#!/usr/bin/env python3
"""
Trajectory Planning for Smooth Robot Motion.
"""

import numpy as np
import math


class TrajectoryPlanner:
    """Generate smooth trajectories."""

    def cubic_polynomial(self, t, T, q0, qf, v0, vf):
        """Cubic polynomial trajectory."""
        a0 = q0
        a1 = v0
        a2 = (3 * (qf - q0) / T**2) - (2 * v0 + vf) / T
        a3 = (-2 * (qf - q0) / T**3) + (v0 + vf) / T**2

        q = a0 + a1 * t + a2 * t**2 + a3 * t**3
        v = a1 + 2 * a2 * t + 3 * a3 * t**2
        a = 2 * a2 + 6 * a3 * t
        return q, v, a

    def quintic_polynomial(self, t, T, q0, qf, v0, vf):
        """Quintic polynomial with zero accel at boundaries."""
        T2, T3, T4, T5 = T**2, T**3, T**4, T**5

        a = np.array([
            [T3, T4, T5],
            [3*T2, 4*T3, 5*T4],
            [6*T, 12*T2, 20*T3]
        ])
        b = np.array([qf - q0 - v0*T, vf - v0, 0])

        a3, a4, a5 = np.linalg.solve(a, b)

        q = q0 + v0*t + a3*t**3 + a4*t**4 + a5*t**5
        v = v0 + 3*a3*t**2 + 4*a4*t**3 + 5*a5*t**4
        a = 6*a3*t + 12*a4*t**2 + 20*a5*t**3
        return q, v, a


class JointTrajectory:
    """Plan multi-joint trajectories."""

    def __init__(self, n_joints):
        self.n_joints = n_joints
        self.planner = TrajectoryPlanner()

    def plan(self, start, end, duration=1.0, n_points=100):
        """Plan trajectory from start to end configuration."""
        times = np.linspace(0, duration, n_points)
        traj = {
            'time': times,
            'positions': np.zeros((n_points, self.n_joints)),
            'velocities': np.zeros((n_points, self.n_joints)),
            'accelerations': np.zeros((n_points, self.n_joints))
        }

        for j in range(self.n_joints):
            q, v, a = self.planner.quintic_polynomial(
                times, duration, start[j], end[j], 0, 0
            )
            traj['positions'][:, j] = q
            traj['velocities'][:, j] = v
            traj['accelerations'][:, j] = a

        return traj


if __name__ == "__main__":
    planner = JointTrajectory(n_joints=3)
    traj = planner.plan([0, 0, 0], [math.pi/2, math.pi/4, -math.pi/6])

    print("Joint Trajectory Planning Demo")
    print(f"Trajectory points: {len(traj['time'])}")
    print(f"Max velocity: {np.max(np.abs(traj['velocities'])):.3f} rad/s")
    print(f"Max acceleration: {np.max(np.abs(traj['accelerations'])):.3f} rad/s²")
