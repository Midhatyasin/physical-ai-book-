#!/usr/bin/env python3
"""
Formation Control using Leader-Follower approach.
Implements line, V-shape, and circle formations.
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class RobotPose:
    """Robot pose representation."""
    x: float
    y: float
    theta: float

    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.x, self.y, self.theta])


class FormationController:
    """Multi-robot formation controller."""

    def __init__(self, robots: List[str], formation_type: str = "line",
                 spacing: float = 1.0):
        """
        Initialize formation controller.

        Args:
            robots: List of robot names/IDs
            formation_type: line, v_shape, or circle
            spacing: Distance between robots in formation
        """
        self.robots = robots
        self.n_robots = len(robots)
        self.formation_type = formation_type
        self.spacing = spacing

    def compute_formation_poses(self, leader_pose: RobotPose) -> Dict[str, RobotPose]:
        """
        Compute target poses for all followers based on leader position.

        Args:
            leader_pose: Current pose of the leader robot

        Returns:
            Dictionary mapping robot names to target poses
        """
        formations = {
            "line": self._line_formation,
            "v_shape": self._v_formation,
            "circle": self._circle_formation,
            "wedge": self._wedge_formation
        }

        if self.formation_type not in formations:
            raise ValueError(f"Unknown formation: {self.formation_type}")

        return formations[self.formation_type](leader_pose)

    def _line_formation(self, leader_pose: RobotPose) -> Dict[str, RobotPose]:
        """Compute line formation behind leader."""
        poses = {}

        # Leader is first robot
        leader_name = self.robots[0]
        poses[leader_name] = leader_pose

        # Followers line up behind leader
        for i, robot_name in enumerate(self.robots[1:], 1):
            # Position behind leader based on formation
            offset_x = -i * self.spacing
            offset_y = 0

            # Rotate offset by leader orientation
            cos_t = math.cos(leader_pose.theta)
            sin_t = math.sin(leader_pose.theta)

            new_x = leader_pose.x + offset_x * cos_t - offset_y * sin_t
            new_y = leader_pose.y + offset_x * sin_t + offset_y * cos_t

            poses[robot_name] = RobotPose(new_x, new_y, leader_pose.theta)

        return poses

    def _v_formation(self, leader_pose: RobotPose) -> Dict[str, RobotPose]:
        """Compute V-shaped formation (flocking style)."""
        poses = {}
        poses[self.robots[0]] = leader_pose

        cos_t = math.cos(leader_pose.theta)
        sin_t = math.sin(leader_pose.theta)

        # Left and right sides of V
        left_count = (self.n_robots - 1) // 2
        right_count = (self.n_robots - 1) - left_count

        left_idx = 1
        right_idx = 1 + left_count

        # Create left side
        for i in range(left_count):
            offset_x = -(i + 1) * self.spacing * 0.7
            offset_y = (i + 1) * self.spacing

            new_x = leader_pose.x + offset_x * cos_t - offset_y * sin_t
            new_y = leader_pose.y + offset_x * sin_t + offset_y * cos_t

            robot_name = self.robots[left_idx]
            poses[robot_name] = RobotPose(new_x, new_y, leader_pose.theta)
            left_idx += 1

        # Create right side
        for i in range(right_count):
            offset_x = -(i + 1) * self.spacing * 0.7
            offset_y = -(i + 1) * self.spacing

            new_x = leader_pose.x + offset_x * cos_t - offset_y * sin_t
            new_y = leader_pose.y + offset_x * sin_t + offset_y * cos_t

            robot_name = self.robots[right_idx]
            poses[robot_name] = RobotPose(new_x, new_y, leader_pose.theta)
            right_idx += 1

        return poses

    def _circle_formation(self, leader_pose: RobotPose) -> Dict[str, RobotPose]:
        """Compute circular formation around leader."""
        poses = {}
        poses[self.robots[0]] = leader_pose

        radius = (self.n_robots - 1) * self.spacing / (2 * math.pi)

        for i, robot_name in enumerate(self.robots[1:], 1):
            angle = leader_pose.theta + (i - 1) * 2 * math.pi / (self.n_robots - 1)

            new_x = leader_pose.x + radius * math.cos(angle)
            new_y = leader_pose.y + radius * math.sin(angle)
            new_theta = angle + math.pi/2

            poses[robot_name] = RobotPose(new_x, new_y, new_theta)

        return poses

    def _wedge_formation(self, leader_pose: RobotPose) -> Dict[str, RobotPose]:
        """Compute wedge/arrowhead formation."""
        poses = {}
        poses[self.robots[0]] = leader_pose

        cos_t = math.cos(leader_pose.theta)
        sin_t = math.sin(leader_pose.theta)

        rows = int(math.sqrt(self.n_robots - 1)) + 1
        col = 0

        for i, robot_name in enumerate(self.robots[1:], 1):
            row = i // rows
            col = i % rows if i % rows != 0 else rows - 1

            offset_x = -(row + 1) * self.spacing * 0.8
            offset_y = (col - rows/2) * self.spacing

            new_x = leader_pose.x + offset_x * cos_t - offset_y * sin_t
            new_y = leader_pose.y + offset_x * sin_t + offset_y * cos_t

            poses[robot_name] = RobotPose(new_x, new_y, leader_pose.theta)

        return poses


class FormationTrackingController:
    """Track formation while avoiding collisions."""

    def __init__(self, formation_controller: FormationController,
                 max_velocity: float = 1.0,
                 collision_radius: float = 0.5):
        self.formation = formation_controller
        self.max_velocity = max_velocity
        self.collision_radius = collision_radius

    def compute_velocities(self, leader_pose: RobotPose,
                           current_poses: Dict[str, RobotPose]) -> Dict[str, np.ndarray]:
        """
        Compute velocity commands for formation tracking.

        Args:
            leader_pose: Current leader position
            current_poses: Current poses of all robots

        Returns:
            Dictionary mapping robots to velocity commands
        """
        target_poses = self.formation.compute_formation_poses(leader_pose)
        velocities = {}

        for robot_name in self.formation.robots:
            if robot_name not in current_poses:
                continue

            target = target_poses[robot_name]
            current = current_poses[robot_name]

            # Position error
            dx = target.x - current.x
            dy = target.y - current.y

            # Proportional velocity
            k_p = 2.0
            vx = k_p * dx
            vy = k_p * dy

            # Limit velocity
            velocity = np.array([vx, vy])
            if np.linalg.norm(velocity) > self.max_velocity:
                velocity = velocity / np.linalg.norm(velocity) * self.max_velocity

            # Collision avoidance
            for other_name, other_pose in current_poses.items():
                if other_name == robot_name:
                    continue

                dist = math.sqrt((current.x - other_pose.x)**2 +
                                (current.y - other_pose.y)**2)

                if dist < self.collision_radius:
                    # Push away from nearby robot
                    push_x = current.x - other_pose.x
                    push_y = current.y - other_pose.y
                    push_dist = math.sqrt(push_x**2 + push_y**2)

                    if push_dist > 0:
                        push_strength = (self.collision_radius - dist) / dist
                        velocity[0] += push_x * push_strength
                        velocity[1] += push_y * push_strength

            velocities[robot_name] = velocity

        return velocities


if __name__ == "__main__":
    print("Formation Control - Leader Follower")
    print("=" * 50)

    # Create formation controller with 5 robots
    robots = ["robot_0", "robot_1", "robot_2", "robot_3", "robot_4"]

    for formation_type in ["line", "v_shape", "circle", "wedge"]:
        controller = FormationController(robots, formation_type=formation_type,
                                        spacing=1.5)

        # Leader at origin facing forward
        leader = RobotPose(x=0, y=0, theta=0)

        poses = controller.compute_formation_poses(leader)

        print(f"\n{formation_type.upper()} Formation:")
        for name, pose in poses.items():
            print(f"  {name}: ({pose.x:.2f}, {pose.y:.2f}, {pose.theta:.2f})")
