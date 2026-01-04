#!/usr/bin/env python3
"""
Basic Image Processing Operations for Robot Vision
Covers: Color spaces, filtering, and basic transformations
"""

import cv2
import numpy as np


def load_and_convert_color_spaces(image_path):
    """Load image and convert between color spaces."""
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Convert to different color spaces
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

    return {
        'bgr': image,
        'gray': gray,
        'hsv': hsv,
        'lab': lab,
        'yuv': yuv
    }


def apply_filters(image, filter_type='gaussian'):
    """Apply various image filters."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    filters = {}

    # Gaussian Blur
    filters['gaussian'] = cv2.GaussianBlur(gray, (5, 5), 0)

    # Median Filter
    filters['median'] = cv2.medianBlur(gray, 5)

    # Bilateral Filter (edge-preserving)
    filters['bilateral'] = cv2.bilateralFilter(gray, 9, 75, 75)

    # Sharpening
    kernel_sharpen = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    filters['sharpen'] = cv2.filter2D(gray, -1, kernel_sharpen)

    # Sobel Edge Detection
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    filters['sobel'] = np.sqrt(sobel_x**2 + sobel_y**2).astype(np.uint8)

    # Laplacian
    filters['laplacian'] = cv2.Laplacian(gray, cv2.CV_64F)

    return filters


def color_segmentation(image, color_ranges):
    """
    Segment image by color ranges.

    Args:
        image: BGR image
        color_ranges: dict with {'color_name': (lower, upper) HSV bounds}

    Returns:
        dict with masks for each color
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    masks = {}

    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, lower, upper)
        # Clean up mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        masks[color_name] = mask

    return masks


def main():
    """Demo function."""
    print("Basic Image Processing for Robot Vision")
    print("=" * 50)

    # Example color ranges for common objects
    color_ranges = {
        'red': (np.array([0, 100, 100]), np.array([10, 255, 255])),
        'green': (np.array([40, 100, 100]), np.array([80, 255, 255])),
        'blue': (np.array([100, 100, 100]), np.array([130, 255, 255])),
        'yellow': (np.array([20, 100, 100]), np.array([30, 255, 255])),
    }

    print(f"Color ranges defined for: {list(color_ranges.keys())}")
    print("\nFunctions available:")
    print("- load_and_convert_color_spaces()")
    print("- apply_filters()")
    print("- color_segmentation()")


if __name__ == "__main__":
    main()
