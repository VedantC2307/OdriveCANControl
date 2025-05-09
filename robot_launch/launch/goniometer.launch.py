from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Launch arguments for data recording
    save_dir_arg = DeclareLaunchArgument(
        'save_dir',
        default_value='/home/vedant/ODriveControl/src/data_logging/data_logging',
        description='Directory to save recorded data'
    )
    
    subject_name_arg = DeclareLaunchArgument(
        'subject_name',
        default_value='subject1',
        description='Subject name for data recording'
    )
    
    buffer_size_arg = DeclareLaunchArgument(
        'buffer_size',
        default_value='100',
        description='Buffer size for data recording (samples)'
    )
    
    sync_slop_arg = DeclareLaunchArgument(
        'sync_slop',
        default_value='0.01',
        description='Time tolerance for message synchronization (seconds)'
    )
    
    # Auto start recording flag
    auto_start_recording_arg = DeclareLaunchArgument(
        'auto_start_recording',
        default_value='false',
        description='Automatically start recording on node startup'
    )

    # impedance configuration file
    config_file = os.path.join(
        get_package_share_directory('controller'),
        'config',
        'impedance_params.yaml'
    )

    goniometer_node = Node(
        package="encoder",
        executable="goniometer",
        name="goniometer_node",
        output="screen"
    )

    encoder_node = Node(
        package="encoder",
        executable="encoder_node",
        name="AMT102_encoder_node",
        output="screen"
    )

    # Friction Compensation node
    friction_compensation_node = Node(
        package="controller",
        executable="friction_compensation_node",
        name="friction_compensation_node",
        output="screen"
    )

    # Impedance Control 노드 (파라미터 파일 포함)
    impedance_control_node = Node(
        package="controller",
        executable="Impedance_Control",
        name="Impedance_Control",
        output="screen",
        parameters=[config_file]  # impedance 파라미터 설정 파일 로드
    )

    # ODrive Controller 노드
    odrive_controller_node = Node(
        package="controller",
        executable="odrive_controller",
        name="ODrive_Controller",
        output="screen"
    )

    # Data logging node with updated parameters
    data_logging_node = Node(
        package="data_logging",
        executable="data_logging_goniometer",
        name="Data_Recording_node",
        output="screen",
        parameters=[{
            'save_dir': LaunchConfiguration('save_dir'),
            'subject_name': LaunchConfiguration('subject_name'),
            'buffer_size': LaunchConfiguration('buffer_size'),
            'sync_slop': LaunchConfiguration('sync_slop')
        }]
    )

    recording_node = Node(
        package="data_logging",
        executable="recording_flag",
        name="recording_flag_node",
        output="screen",
    )


    return LaunchDescription([
        # Launch arguments
        save_dir_arg,
        subject_name_arg,
        buffer_size_arg,
        sync_slop_arg,
    
        # Nodes
        goniometer_node,
        # encoder_node,
        # friction_compensation_node,
        # impedance_control_node,
        # odrive_controller_node,
        #recording_node,
        data_logging_node,
    ])