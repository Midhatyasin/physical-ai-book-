#!/usr/bin/env python3
"""
Simple Python example for Physical AI book.
Demonstrates basic Python concepts used throughout the book.
"""

def calculate_workspace_bounds(arm_length: float, reach: float) -> dict:
    """
    Calculate the reachable workspace for a robot arm.

    Args:
        arm_length: Length of the robot arm segment
        reach: Maximum reach distance

    Returns:
        Dictionary containing workspace bounds
    """
    import math

    radius = min(arm_length, reach)
    area = math.pi * radius ** 2

    return {
        "min_radius": 0.0,
        "max_radius": radius,
        "workspace_area": area,
        "workspace_type": "circular" if arm_length > 0 else "point"
    }


class RobotJoint:
    """Represents a single joint in a robot arm."""

    def __init__(self, name: str, max_angle: float = 180.0):
        self.name = name
        self.max_angle = max_angle
        self.current_angle = 0.0

    def set_angle(self, angle: float) -> bool:
        """
        Set the joint to a specific angle.

        Args:
            angle: Desired angle in degrees

        Returns:
            True if successful, False if angle out of bounds
        """
        if -self.max_angle <= angle <= self.max_angle:
            self.current_angle = angle
            return True
        return False

    def get_state(self) -> dict:
        """Get the current state of the joint."""
        return {
            "name": self.name,
            "current_angle": self.current_angle,
            "within_bounds": -self.max_angle <= self.current_angle <= self.max_angle
        }


def main():
    """Main entry point for demonstration."""
    print("=" * 50)
    print("Physical AI - Python Basics Example")
    print("=" * 50)

    # Calculate workspace bounds
    arm = calculate_workspace_bounds(arm_length=0.5, reach=0.8)
    print(f"Robot arm workspace: {arm}")

    # Test joint control
    joint = RobotJoint(name="shoulder_joint", max_angle=180)
    joint.set_angle(45)
    print(f"Joint state: {joint.get_state()}")


if __name__ == "__main__":
    main()
