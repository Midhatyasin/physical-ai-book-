#!/usr/bin/env python3
"""
Color-based Object Tracking for Robotics
Simple but effective tracking for manipulation and navigation tasks
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List


class ColorTracker:
    """Track objects by color in real-time."""

    def __init__(self, hue_range: Tuple[int, int],
                 saturation_range: Tuple[int, int],
                 value_range: Tuple[int, int],
                 min_area: int = 500):
        """
        Initialize tracker with HSV color ranges.

        Args:
            hue_range: (min_hue, max_hue) - typically 0-180 in OpenCV
            saturation_range: (min_sat, max_sat) - 0-255
            value_range: (min_val, max_val) - 0-255
            min_area: Minimum contour area to track
        """
        self.lower_hsv = np.array([hue_range[0], saturation_range[0], value_range[0]])
        self.upper_hsv = np.array([hue_range[1], saturation_range[1], value_range[1]])
        self.min_area = min_area

    @classmethod
    def from_color_name(cls, color_name: str, **kwargs) -> 'ColorTracker':
        """Create tracker for common colors."""
        color_ranges = {
            'red': ((0, 10), (100, 255), (100, 255)),
            'orange': ((5, 15), (100, 255), (100, 255)),
            'yellow': ((20, 30), (100, 255), (100, 255)),
            'green': ((40, 80), (50, 255), (50, 255)),
            'blue': ((100, 130), (100, 255), (100, 255)),
            'purple': ((130, 160), (50, 255), (50, 255)),
            'white': ((0, 0), (0, 30), (200, 255)),
            'black': ((0, 0), (0, 255), (0, 30)),
        }

        if color_name.lower() not in color_ranges:
            raise ValueError(f"Unknown color: {color_name}. Available: {list(color_ranges.keys())}")

        hue_range, sat_range, val_range = color_ranges[color_name.lower()]
        return cls(hue_range, sat_range, val_range, **kwargs)

    def track(self, frame: np.ndarray) -> Tuple[Optional[Tuple[int, int]],
                                                Optional[Tuple[int, int]],
                                                Optional[np.ndarray]]:
        """
        Track target color in frame.

        Args:
            frame: BGR image from camera

        Returns:
            (center, size, mask) or (None, None, None) if not found
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)

        # Morphological cleanup
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None, None, None

        # Find largest contour
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < self.min_area:
            return None, None, None

        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest)
        center_x = x + w // 2
        center_y = y + h // 2

        return (center_x, center_y), (w, h), mask

    def draw_tracking(self, frame: np.ndarray,
                      center: Optional[Tuple[int, int]],
                      size: Optional[Tuple[int, int]]) -> np.ndarray:
        """Draw tracking visualization."""
        if center is None or size is None:
            return frame

        x, y = center
        w, h = size

        # Draw bounding box
        top_left = (x - w // 2, y - h // 2)
        bottom_right = (x + w // 2, y + h // 2)

        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Draw center point
        cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)

        # Draw crosshair
        cv2.line(frame, (x - 15, y), (x + 15, y), (0, 0, 255), 1)
        cv2.line(frame, (x, y - 15), (x, y + 15), (0, 0, 255), 1)

        return frame


class MultiColorTracker:
    """Track multiple colors simultaneously."""

    def __init__(self):
        self.trackers: Dict[str, ColorTracker] = {}

    def add_tracker(self, name: str, tracker: ColorTracker):
        """Add a color tracker."""
        self.trackers[name] = tracker

    def track_all(self, frame: np.ndarray) -> Dict[str, Tuple]:
        """Track all registered colors."""
        results = {}
        for name, tracker in self.trackers.items():
            center, size, mask = tracker.track(frame)
            results[name] = (center, size, mask)
        return results

    def draw_all(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """Draw all tracking results."""
        img = frame.copy()
        for name, (center, size, _) in results.items():
            img = self.trackers[name].draw_tracking(img, center, size)

            # Add label
            if center:
                cv2.putText(img, name, (center[0] + 20, center[1]),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        return img


def run_tracking_demo(color: str = 'red'):
    """Run color tracking demo."""
    tracker = ColorTracker.from_color_name(color)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print(f"Tracking {color} objects...")
    print("Press 'q' to quit, 's' to switch color")

    colors = ['red', 'green', 'blue', 'yellow']
    color_idx = colors.index(color)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Track
        center, size, mask = tracker.track(frame)
        result = tracker.draw_tracking(frame, center, size)

        cv2.imshow('Color Tracking', result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            color_idx = (color_idx + 1) % len(colors)
            color = colors[color_idx]
            tracker = ColorTracker.from_color_name(color)
            print(f"Switched to tracking: {color}")

    cap.release()
    cv2.destroyAllWindows()


def get_tracking_command(tracker: ColorTracker,
                         frame_width: int = 640,
                         frame_height: int = 480) -> Tuple[str, float]:
    """
    Get navigation command from tracking result.

    Returns:
        (direction, speed) tuple
    """
    center, size, _ = tracker.track(None)  # Would need actual frame

    if center is None:
        return 'STOP', 0.0

    # Horizontal position
    frame_center = frame_width // 2
    error = center[0] - frame_center

    # Vertical position
    if center[1] < frame_height * 0.3:
        command = 'FORWARD'
    elif center[1] > frame_height * 0.7:
        command = 'BACKWARD'
    else:
        command = 'STOP'

    # Turning based on horizontal error
    turn_rate = error / frame_center  # -1 to 1
    speed = 0.5 if command == 'FORWARD' else 0.0

    return f"{command} + {'LEFT' if turn_rate < -0.1 else 'RIGHT' if turn_rate > 0.1 else 'STRAIGHT'}", speed


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run_tracking_demo(sys.argv[1])
    else:
        run_tracking_demo('red')
