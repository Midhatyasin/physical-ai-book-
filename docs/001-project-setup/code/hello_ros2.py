#!/usr/bin/env python3
"""
ROS 2 Greeting Node - Your First Physical AI Program

This node demonstrates the basic structure of a ROS 2 node.
Run this with: ros2 run my_package greeting_node
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from example_interfaces.msg import Int64


class GreetingNode(Node):
    """
    A simple ROS 2 node that publishes greeting messages.

    This demonstrates:
    - Node creation and initialization
    - Publisher creation for topic communication
    - Timer-based periodic publishing
    - Logger usage for debugging
    """

    def __init__(self):
        super().__init__('greeting_node')
        self.counter = 0

        # Create a publisher for String messages
        # QoS (Quality of Service) depth = 10 messages
        self.publisher = self.create_publisher(
            String,
            'greetings',
            10  # QoS history depth
        )

        # Create a subscriber to receive commands
        self.subscriber = self.create_subscription(
            Int64,
            'reset_counter',
            self.reset_callback,
            10
        )

        # Create a timer to publish every second (1 Hz)
        self.timer = self.create_timer(1.0, self.publish_greeting)

        self.get_logger().info('Greeting Node initialized!')

    def publish_greeting(self):
        """Publish a greeting message with a counter."""
        self.counter += 1
        msg = String()
        msg.data = f'Hello from ROS 2! Message #{self.counter}'

        self.publisher.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')

    def reset_callback(self, msg: Int64):
        """Handle reset commands from other nodes."""
        self.get_logger().info(f'Resetting counter to {msg.data}')
        self.counter = msg.data


def main(args=None):
    """
    Main entry point for the greeting node.

    This demonstrates the standard ROS 2 node lifecycle:
    1. Initialize rclpy
    2. Create and spin the node
    3. Clean up on shutdown
    """
    rclpy.init(args=args)

    node = GreetingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node interrupted by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
