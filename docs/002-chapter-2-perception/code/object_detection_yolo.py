#!/usr/bin/env python3
"""
Object Detection using YOLOv8 for Robotics
Real-time detection with filtering for robot-relevant objects
"""

import cv2
from ultralytics import YOLO
import numpy as np
from typing import List, Dict, Optional


class RobotObjectDetector:
    """Object detector optimized for robotics applications."""

    # Classes commonly relevant for manipulation
    ROBOT_RELEVANT_CLASSES = [
        'person', 'cup', 'bottle', 'bowl', 'knife',
        'spoon', 'fork', 'banana', 'apple', 'orange',
        'chair', 'laptop', 'mouse', 'keyboard', 'cell phone'
    ]

    def __init__(self, model_size='n', confidence_threshold=0.5):
        """
        Initialize detector.

        Args:
            model_size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (xl)
            confidence_threshold: Minimum confidence for detection
        """
        model_name = f'yolov8{model_size}.pt'
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold

        # Map class names to IDs
        self.class_to_id = {name: i for i, name in enumerate(self.model.names)}

    def detect(self, image) -> List[Dict]:
        """
        Detect objects in image.

        Returns:
            List of detections with: bbox, confidence, class_name, class_id
        """
        results = self.model(image, conf=self.confidence_threshold)
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    'bbox': box.xyxy[0].cpu().numpy().tolist(),
                    'confidence': float(box.conf[0].cpu().numpy()),
                    'class_name': self.model.names[int(box.cls[0].cpu().numpy())],
                    'class_id': int(box.cls[0].cpu().numpy())
                }
                detections.append(detection)

        return detections

    def detect_relevant_only(self, image) -> List[Dict]:
        """Detect only robot-relevant objects."""
        all_detections = self.detect(image)
        relevant = [
            d for d in all_detections
            if d['class_name'] in self.ROBOT_RELEVANT_CLASSES
        ]
        return relevant

    def draw_detections(self, image, detections, draw_all=True):
        """Draw bounding boxes on image."""
        img = image.copy()

        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            conf = det['confidence']
            class_name = det['class_name']

            # Draw box
            color = (0, 255, 0)  # Green
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Draw label
            label = f'{class_name}: {conf:.2f}'
            cv2.putText(img, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return img

    def get_closest_relevant(self, image) -> Optional[Dict]:
        """Get the closest (largest) relevant object."""
        relevant = self.detect_relevant_only(image)
        if not relevant:
            return None

        # Sort by bounding box area (proxy for closeness)
        for det in relevant:
            x1, y1, x2, y2 = det['bbox']
            det['area'] = (x2 - x1) * (y2 - y1)

        return max(relevant, key=lambda d: d['area'])


def run_realtime_detection():
    """Run real-time detection from webcam."""
    detector = RobotObjectDetector(model_size='n', confidence_threshold=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Starting real-time object detection...")
    print("Press 'q' to quit, 'r' to toggle relevant-only mode")

    relevant_only = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect
        if relevant_only:
            detections = detector.detect_relevant_only(frame)
        else:
            detections = detector.detect(frame)

        # Draw
        result_frame = detector.draw_detections(frame, detections)

        # Show relevant-only status
        status = f"Relevant Only: {relevant_only} | Objects: {len(detections)}"
        cv2.putText(result_frame, status, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow('Robot Object Detection', result_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            relevant_only = not relevant_only

    cap.release()
    cv2.destroyAllWindows()


def detect_from_image(image_path):
    """Detect objects in a static image."""
    detector = RobotObjectDetector(model_size='n')

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image: {image_path}")
        return

    print(f"Processing: {image_path}")

    detections = detector.detect(image)
    print(f"Found {len(detections)} objects:")

    for det in detections:
        print(f"  - {det['class_name']}: {det['confidence']:.2%}")

    # Draw and save
    result = detector.draw_detections(image, detections)
    cv2.imwrite('detection_result.jpg', result)
    print("Result saved to: detection_result.jpg")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        detect_from_image(sys.argv[1])
    else:
        run_realtime_detection()
