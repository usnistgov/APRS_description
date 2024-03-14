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
    robot_urdf_docs = {name:xacro.process_file(os.path.join(get_package_share_directory('aprs_description'), 'urdf', f'aprs_{name}.urdf.xacro')) for name in robot_names}
    robot_descriptions = {name:{"robot_description":robot_urdf_docs[name].toprettyxml(indent='  ')} for name in robot_names}

    robot_state_publishers = {}
    for name in robot_names:
        robot_state_publishers[name] = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=f"{name}_publisher",
            output="both",
            parameters=[{"use_sim_time": True}, robot_descriptions[name]],
        )

    world_path = os.path.join(get_package_share_directory('aprs_description'), 'worlds', 'lab.sdf')
    
    gz = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(get_package_share_directory('ros_gz_sim'),
                              'launch', 'gz_sim.launch.py')]),
            launch_arguments=[('gz_args', [' -r -v 4 '+ world_path])])

    gz_spawners = {}
    for name in robot_names:
        gz_spawners[name] = Node(
            package='ros_gz_sim',
            executable='create',
            output='screen',
            namespace=f"{name}_spawner",
            arguments=['-string', robot_urdf_docs[name].toxml(),
                    '-name', f'aprs_{name}',
                    '-allow_renaming', 'true'],
        )
    
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        name="joint_state_broadcaster_spawner",
        arguments=["joint_state_broadcaster"],
        parameters=[
            {"use_sim_time": True},
        ],
    )
    
    ur_controller = Node(
        package="controller_manager",
        executable="spawner",
        name="ur_controller_spawner",
        arguments=["ur_joint_trajectory_controller"],
        parameters=[
            {"use_sim_time": True},
        ],
    )
    
    fanuc_controller = Node(
        package="controller_manager",
        executable="spawner",
        name="fanuc_controller_spawner",
        arguments=["fanuc_joint_trajectory_controller"],
        parameters=[
            {"use_sim_time": True},
        ],
    )
    
    franka_controller = Node(
        package="controller_manager",
        executable="spawner",
        name="franka_controller_spawner",
        arguments=["franka_joint_trajectory_controller"],
        parameters=[
            {"use_sim_time": True},
        ],
    )
    
    motoman_controller = Node(
        package="controller_manager",
        executable="spawner",
        name="motoman_controller_spawner",
        arguments=["motoman_joint_trajectory_controller"],
        parameters=[
            {"use_sim_time": True},
        ],
    )

    nodes_to_start = [
        gz,
        joint_state_broadcaster,
        ur_controller,
        fanuc_controller,
        franka_controller,
        motoman_controller
    ] + [robot_state_publishers[name] for name in robot_names] + [gz_spawners[name] for name in robot_names]

    return nodes_to_start


def generate_launch_description():
    declared_arguments = []

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])