#!/usr/bin/env python3
"""
Stereo Vision and Depth Estimation
Implements basic stereo matching for depth perception
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class StereoDepthEstimator:
    """Estimate depth from stereo image pairs."""

    def __init__(self, focal_length: float, baseline: float):
        """
        Initialize stereo estimator.

        Args:
            focal_length: Camera focal length in pixels
            baseline: Distance between cameras in meters
        """
        self.focal_length = focal_length
        self.baseline = baseline

        # Create stereo matcher
        self.stereo = cv2.StereoBM_create(
            numDisparities=64,
            blockSize=15
        )

    def compute_disparity(self, left_img: np.ndarray, right_img: np.ndarray) -> np.ndarray:
        """
        Compute disparity map from stereo pair.

        Args:
            left_img: Left grayscale image
            right_img: Right grayscale image

        Returns:
            Disparity map
        """
        # Ensure grayscale
        if len(left_img.shape) == 3:
            left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
        else:
            left_gray = left_img

        if len(right_img.shape) == 3:
            right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
        else:
            right_gray = right_img

        # Compute disparity
        disparity = self.stereo.compute(left_gray, right_gray)

        return disparity

    def disparity_to_depth(self, disparity: np.ndarray) -> np.ndarray:
        """
        Convert disparity to depth.

        Depth = (f * B) / disparity

        Args:
            disparity: Disparity map

        Returns:
            Depth map in meters
        """
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            depth = (self.focal_length * self.baseline) / (disparity + 0.0001)

        # Set invalid regions to 0
        depth[disparity <= 0] = 0

        return depth

    def create_depth_colormap(self, depth: np.ndarray, max_depth: float = 10.0) -> np.ndarray:
        """
        Create color-coded depth map.

        Args:
            depth: Depth map in meters
            max_depth: Maximum depth to display (meters)

        Returns:
            Color-coded depth image (BGR)
        """
        # Normalize depth
        depth_normalized = np.clip(depth, 0, max_depth)
        depth_normalized = depth_normalized / max_depth * 255
        depth_normalized = depth_normalized.astype(np.uint8)

        # Apply JET colormap (close=blue, far=red)
        depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)

        # Add depth legend
        cv2.putText(depth_colored, "Close", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(depth_colored, f"{max_depth}m Far", (10, depth_colored.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return depth_colored


class RGBDProcessor:
    """Process RGB-D data from sensors like RealSense or Kinect."""

    def __init__(self, camera_matrix: np.ndarray):
        """
        Initialize with camera intrinsics.

        Args:
            camera_matrix: 3x3 camera matrix
        """
        self.K = camera_matrix
        self.fx = camera_matrix[0, 0]
        self.fy = camera_matrix[1, 1]
        self.cx = camera_matrix[0, 2]
        self.cy = camera_matrix[1, 2]

    def depth_to_pointcloud(self, depth_image: np.ndarray) -> np.ndarray:
        """
        Convert depth image to point cloud.

        Args:
            depth_image: H x W depth map in meters

        Returns:
            N x 3 array of 3D points
        """
        h, w = depth_image.shape
        x, y = np.meshgrid(np.arange(w), np.arange(h))

        # Normalize to camera coordinates
        x_norm = (x - self.cx) / self.fx
        y_norm = (y - self.cy) / self.fy

        # Compute 3D coordinates
        X = x_norm * depth_image
        Y = y_norm * depth_image
        Z = depth_image

        # Stack into point cloud
        points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])

        # Remove invalid points
        valid = Z.flatten() > 0
        points = points[valid]

        return points

    def filter_roi(self, points: np.ndarray,
                   x_range: Tuple[float, float],
                   y_range: Tuple[float, float],
                   z_range: Tuple[float, float]) -> np.ndarray:
        """Filter point cloud by axis-aligned bounding box."""
        x_valid = (points[:, 0] >= x_range[0]) & (points[:, 0] <= x_range[1])
        y_valid = (points[:, 1] >= y_range[0]) & (points[:, 1] <= y_range[1])
        z_valid = (points[:, 2] >= z_range[0]) & (points[:, 2] <= z_range[1])

        return points[x_valid & y_valid & z_valid]


def demo_stereo():
    """Demo function showing stereo processing."""
    print("Stereo Depth Estimation Demo")
    print("=" * 50)

    # Create sample images (in practice, load real stereo pair)
    h, w = 480, 640
    left_img = np.random.randint(0, 256, (h, w), dtype=np.uint8)
    right_img = np.random.randint(0, 256, (h, w), dtype=np.uint8)

    # Initialize estimator
    estimator = StereoDepthEstimator(focal_length=700, baseline=0.06)

    # Compute disparity
    disparity = estimator.compute_disparity(left_img, right_img)
    print(f"Disparity range: [{disparity.min()}, {disparity.max()}]")

    # Convert to depth
    depth = estimator.disparity_to_depth(disparity)
    print(f"Depth range: [{depth.min():.2f}, {depth.max():.2f}] meters")

    # Create visualization
    depth_colored = estimator.create_depth_colormap(depth, max_depth=5.0)
    cv2.imwrite('stereo_depth_visualization.jpg', depth_colored)
    print("Saved: stereo_depth_visualization.jpg")


if __name__ == "__main__":
    demo_stereo()
