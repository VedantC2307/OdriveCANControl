from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    #Launch the motor control server node
    # Odrive_server_node = Node(
    #     package='app_server',
    #     executable='odrive_server_app',
    #     name='Odrive_control_server',
    #     output='screen',
    # )

    # encoder_node = Node(
    #     package="encoder",
    #     executable="encoder_node",
    #     name="AMT102_encoder_node",
    #     output="screen"
    # )

    odrive_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('odrive_can'),
            '/launch/example.launch.yaml'
        ])
    )

    # frictionCompensation_node = Node(
    #     package="controller",
    #     executable="FC_node",
    #     name="Friction_Compensation_node",
    #     output="screen"
    # )

    return LaunchDescription([
        # Odrive_server_node,
        # encoder_node,
        odrive_launch
        # frictionCompensation_node
        
    ])