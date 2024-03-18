import os
import xacro

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

def launch_setup(context, *args, **kwargs):
    robot_names = ["fanuc", "franka", "motoman", "ur"]

    # urdf = os.path.join(get_package_share_directory('aprs_description'), 'urdf', 'aprs_lab_robots.urdf.xacro')
    
    # doc = xacro.process_file(urdf)

    # robot_description_content = doc.toprettyxml(indent='  ')

    # print(robot_description_content)

    # robot_description = {"robot_description": robot_description_content}

    robot_urdf_docs = {name:xacro.process_file(os.path.join(get_package_share_directory('aprs_description'), 'urdf', f'aprs_{name}.urdf.xacro')) for name in robot_names}
    robot_descriptions = {name:{"robot_description":robot_urdf_docs[name].toprettyxml(indent='  ')} for name in robot_names}

    robot_state_publishers = []
    for robot_name in robot_names:
        robot_state_publishers.append(Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=f"{robot_name}",
            output="both",
            parameters=[{"use_sim_time": True}, robot_descriptions[robot_name]],
        ))

    # robot_state_publisher_node = Node(
    #     package="robot_state_publisher",
    #     executable="robot_state_publisher",
    #     output="both",
    #     parameters=[{"use_sim_time": True}, robot_description],
    # )

    world_path = os.path.join(get_package_share_directory('aprs_description'), 'worlds', 'lab.sdf')
    
    gz = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(get_package_share_directory('ros_gz_sim'),
                              'launch', 'gz_sim.launch.py')]),
            launch_arguments=[('gz_args', [' -r -v 4 '+ world_path])])

    gz_spawners = []
    for robot_name in robot_names:
        gz_spawners.append(Node(
            package='ros_gz_sim',
            executable='create',
            output='screen',
            namespace=f"{robot_name}",
            name=f"{robot_name}_spawner",
            arguments=['-string', robot_urdf_docs[robot_name].toxml(),
                    '-name', f'aprs_{robot_name}',
                    '-allow_renaming', 'true'],
        ))

    # gz_spawn_entity = Node(
    #     package='ros_gz_sim',
    #     executable='create',
    #     output='screen',
    #     arguments=['-string', doc.toxml(),
    #                '-name', 'aprs_robots',
    #                '-allow_renaming', 'true'],
    # )
    
    controller_spawner_nodes = []
    for robot_name in robot_names:
        controller_spawner_nodes.append(Node(
            package="controller_manager",
            executable="spawner",
            name=f"controller_manager",
            namespace=f"{robot_name}",
            arguments=[f"{robot_name}_controller"],
            parameters=[
                {"use_sim_time": True},
            ],
        ))

    nodes_to_start = [
        gz,
        *controller_spawner_nodes,
        *robot_state_publishers,
        *gz_spawners
    ]

    return nodes_to_start


def generate_launch_description():
    declared_arguments = []

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])