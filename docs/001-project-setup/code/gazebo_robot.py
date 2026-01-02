#!/usr/bin/env python3
"""
Gazebo Robot Model Generator

This script generates a simple 2-wheeled robot model for Gazebo simulation.
Save the output as a .sdf file and load it in Gazebo.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom


def create_robot_sdf(name: str = "simple_robot", num_wheels: int = 2) -> str:
    """
    Create a simple robot SDF model for Gazebo.

    Args:
        name: Name for the robot model
        num_wheels: Number of wheels (2 or 4)

    Returns:
        XML string representing the robot SDF
    """
    # Create root element
    sdf = ET.Element('sdf', attrib={'version': '1.11'})
    model = ET.SubElement(sdf, 'model', attrib={'name': name})

    # Add chassis
    chassis = ET.SubElement(model, 'link', attrib={'name': 'chassis'})
    ET.SubElement(chassis, 'pose').text = '0 0 0.1 0 0 0'

    collision = ET.SubElement(chassis, 'collision', attrib={'name': 'collision'})
    geometry_c = ET.SubElement(collision, 'geometry')
    box_c = ET.SubElement(geometry_c, 'box')
    ET.SubElement(box_c, 'size').text = '0.5 0.3 0.1'

    visual = ET.SubElement(chassis, 'visual', attrib={'name': 'visual'})
    geometry_v = ET.SubElement(visual, 'geometry')
    box_v = ET.SubElement(geometry_v, 'box')
    ET.SubElement(box_v, 'size').text = '0.5 0.3 0.1'

    # Add wheels
    wheel_positions = [0.2, -0.2] if num_wheels == 2 else [0.2, 0.2, -0.2, -0.2]
    wheel_y_positions = [0, 0] if num_wheels == 2 else [0.15, -0.15, 0.15, -0.15]

    for i in range(num_wheels):
        wheel_name = f'wheel_{i}'
        link = ET.SubElement(model, 'link', attrib={'name': wheel_name})

        x_pos = wheel_positions[i % 2]
        y_pos = wheel_y_positions[i] if num_wheels == 4 else 0

        ET.SubElement(link, 'pose').text = f'{x_pos} {y_pos} 0.05 0 0 0'

        collision_w = ET.SubElement(link, 'collision', attrib={'name': f'{wheel_name}_collision'})
        geometry_wc = ET.SubElement(collision_w, 'geometry')
        cylinder_wc = ET.SubElement(geometry_wc, 'cylinder')
        ET.SubElement(cylinder_wc, 'radius').text = '0.05'
        ET.SubElement(cylinder_wc, 'length').text = '0.05'

        visual_w = ET.SubElement(link, 'visual', attrib={'name': f'{wheel_name}_visual'})
        geometry_wv = ET.SubElement(visual_w, 'geometry')
        cylinder_wv = ET.SubElement(geometry_wv, 'cylinder')
        ET.SubElement(cylinder_wv, 'radius').text = '0.05'
        ET.SubElement(cylinder_wv, 'length').text = '0.05'

        # Add joint for this wheel
        joint = ET.SubElement(model, 'joint', attrib={
            'name': f'{wheel_name}_joint',
            'type': 'revolute'
        })
        ET.SubElement(joint, 'parent').text = 'chassis'
        ET.SubElement(joint, 'child').text = wheel_name
        ET.SubElement(joint, 'pose').text = f'{x_pos} {y_pos} 0 0 0 0'
        axis = ET.SubElement(joint, 'axis')
        ET.SubElement(axis, 'xyz').text = '0 1 0'

    return prettify_xml(sdf)


def prettify_xml(elem: ET.Element) -> str:
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def main():
    """Generate and save a robot model."""
    print("Generating robot model for Gazebo...")

    sdf_content = create_robot_sdf(name="my_robot", num_wheels=2)

    # Save to file
    with open("my_robot.sdf", "w") as f:
        f.write(sdf_content)

    print("Robot model saved to my_robot.sdf")
    print("\nTo view in Gazebo:")
    print("  gz sim -u my_robot.sdf")
    print("\nOr use with ROS 2:")
    print("  ros2 run gazebo_ros SpawnEntity.py -file my_robot.sdf")


if __name__ == "__main__":
    main()
