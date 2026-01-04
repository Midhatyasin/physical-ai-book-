#!/usr/bin/env python3
"""
Forward Kinematics using Denavit-Hartenberg parameters.
"""

import numpy as np
import math


class ForwardKinematics:
    """Compute forward kinematics for robotic arms."""

    def __init__(self, dh_params):
        self.dh_params = dh_params

    def transform_matrix(self, theta, d, a, alpha):
        """Create DH transformation matrix."""
        c, s = math.cos(theta), math.sin(theta)
        ca, sa = math.cos(alpha), math.sin(alpha)

        return np.array([
            [c, -s * ca, s * sa, a * c],
            [s, c * ca, -c * sa, a * s],
            [0, sa, ca, d],
            [0, 0, 0, 1]
        ])

    def compute_fk(self, joint_positions):
        """Compute forward kinematics."""
        T = np.eye(4)
        for i, theta in enumerate(joint_positions):
            theta_i, d_i, a_i, alpha_i = self.dh_params[i]
            T_i = self.transform_matrix(theta_i + theta, d_i, a_i, alpha_i)
            T = T @ T_i
        return T

    def get_position(self, joint_positions):
        """Extract 3D position."""
        T = self.compute_fk(joint_positions)
        return T[0:3, 3]


if __name__ == "__main__":
    dh_params = [[0, 0, 0.3, 0], [0, 0, 0.25, 0]]
    fk = ForwardKinematics(dh_params)
    pos = fk.get_position([math.pi/4, math.pi/6])
    print(f"End-effector position: {pos}")
