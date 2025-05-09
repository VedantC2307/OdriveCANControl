#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.parameter import Parameter
from message_filters import ApproximateTimeSynchronizer, Subscriber
from custom_msgs.srv import ODriveCommand
from custom_msgs.msg import FrictionComp, ImpedanceTorque, MotionState
from std_msgs.msg import Float32MultiArray, Bool, Int64
from std_srvs.srv import SetBool
import numpy as np
import os
import csv
from datetime import datetime
import signal
import threading

class DataCollectorNode(Node):
    def __init__(self):
        super().__init__('data_collector_node')
        
        # Define callback groups to ensure proper concurrency
        self.timer_callback_group = ReentrantCallbackGroup()
        self.service_callback_group = MutuallyExclusiveCallbackGroup()
        
        # Add flag to detect forced shutdown
        self._force_shutdown = False
        
        # Parameters
        self.declare_parameter('save_dir', '/home/vedant/ODriveControl/src/data_logging/data_logging')
        self.declare_parameter('buffer_size', 100)  # Number of samples to buffer before writing
        self.declare_parameter('sync_slop', 0.01)   # Time tolerance for message synchronization in seconds
        self.declare_parameter('use_synchronizer', False)  # New parameter to control whether to use synchronizer
        
        # Get parameters
        self.save_dir = self.get_parameter('save_dir').value
        self.subject_name = 'subject1'  # Fixed subject name as requested
        self.buffer_size = self.get_parameter('buffer_size').value
        self.sync_slop = self.get_parameter('sync_slop').value
        self.use_synchronizer = self.get_parameter('use_synchronizer').value
        
        # Format subject name and ensure directory exists
        self.subject_dir = os.path.join(self.save_dir, self.subject_name)
        if not os.path.exists(self.subject_dir):
            os.makedirs(self.subject_dir)
            self.get_logger().info(f'Created directory: {self.subject_dir}')
        
        # File handling variables
        self.current_trial = 1
        self.is_recording = False  # This now only tracks the recording flag value, not whether we're collecting data
        self.csv_file = None
        self.csv_writer = None
        
        # Create data buffers for efficient batch writing
        self.data_buffer = {
            'timestamp': [],
            'position': [],
            'velocity': [],
            'tau_fcomp': [],
            'tau_imp': [],
            'Goniometer': [],
            'recording_flag': []
        }
        self.buffer_lock = threading.Lock()
                                                                                                        
        # Set up QoS profiles
        self.reliable_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            durability=QoSDurabilityPolicy.VOLATILE
        )
        
        # Add a Bool topic subscriber for controlling recording (similar to encoder offset)
        self.recording_flag_sub = self.create_subscription(
            Bool,
            'recording_flag',  # Topic that will control recording
            self.recording_flag_callback,
            10
        )
        self.get_logger().info('Subscribed to recording_flag topic for controlling data recording')
        
        # Option 1: Use synchronized subscribers if all topics are available
        if self.use_synchronizer:
            self.get_logger().info('Using synchronized message collection from multiple topics')
            # Create synchronized subscribers
            self.motor_sub = Subscriber(self, MotionState, 'motor_state', qos_profile=self.reliable_qos)
            self.friction_sub = Subscriber(self, FrictionComp, 'friction_comp_torque', qos_profile=self.reliable_qos)
            self.impedance_sub = Subscriber(self, ImpedanceTorque, 'impedance_torque', qos_profile=self.reliable_qos)
            
            # Synchronize the messages by timestamp
            self.sync = ApproximateTimeSynchronizer(
                [self.motor_sub, self.friction_sub, self.impedance_sub],
                queue_size=30,
                slop=self.sync_slop,
                allow_headerless=True  # Add this parameter to allow messages without headers
            )
            self.sync.registerCallback(self.sync_callback)
        
        # Option 2: Direct subscription to motor state only (for encoder-only operation)
        else:
            self.get_logger().info('Using direct subscription to motor_state topic (encoder only mode)')
            self.motor_sub_direct = self.create_subscription(
                MotionState,
                'motor_state',
                self.motor_state_callback,
                qos_profile=self.reliable_qos
            )
        
        # Add goniometer subscriber regardless of synchronizer mode
        # self.goniometer_reading = 0.0  # Store latest goniometer value
        self.gposition = 0.0
        self.gvelocity = 0.0
        self.goniometer_sub = self.create_subscription(
            MotionState,
            'goniometer_state',
            self.goniometer_callback,
            self.reliable_qos
        )

        self.impedance_torque = 0.0
        self.impedance_sub = self.create_subscription(
            ImpedanceTorque, 
            'imp_torque',
            self.impedance_callback,
            self.reliable_qos
        )
        
        # Timer for periodically writing buffered data (at 10Hz - fine for flushing data)
        self.flush_timer = self.create_timer(
            0.1,  # 10Hz for flushing data to disk
            self.flush_data_callback,
            callback_group=self.timer_callback_group
        )
        
        # Register shutdown handlers
        self.register_shutdown_handlers()
        
        # Start collecting data immediately by creating a file
        self.create_new_file()
        
        self.get_logger().info('Data collector node initialized')
        self.get_logger().info(f'Always recording data for subject {self.subject_name}')
        self.get_logger().info(f'Publish to "recording_flag" topic to toggle recording flag value')

    def register_shutdown_handlers(self):
        """Register handlers to ensure proper file closure on shutdown"""
        # Use ROS lifecycle hooks
        self.add_on_set_parameters_callback(self.on_parameter_change)
        # Register SIGINT/SIGTERM handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle UNIX signals for clean shutdown"""
        self.get_logger().info(f'Received signal {sig}, shutting down gracefully')
        self.close_current_file()
        # Force exit after closing files
        self._force_shutdown = True
    
    def on_parameter_change(self, params):
        """Handle parameter changes during runtime"""
        for param in params:
            if (param.name == 'subject_name' and param.type_ == Parameter.Type.STRING):
                self.subject_name = param.value
                self.subject_dir = os.path.join(self.save_dir, self.subject_name)
                if not os.path.exists(self.subject_dir):
                    os.makedirs(self.subject_dir)
        return True
    
    def create_new_file(self):
        """Create a new CSV file for data recording - only values, no metadata"""
        try:
            filename = os.path.join(self.subject_dir, f'trial_{self.current_trial}.csv')
            
            # Ensure the file is closed if it exists
            if self.csv_file is not None:
                self.csv_file.close()
            
            # Create new CSV file
            self.csv_file = open(filename, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            
            # Write header row only - modified for selected fields
            header = [
            'timestamp',
            'position',
            'velocity',
            'tau_fcomp',
            'tau_imp',
            'Goniometer',
            'recording_flag'
        ]
            self.csv_writer.writerow(header)
            
            self.get_logger().info(f'Created new file: {filename}')
            
        except Exception as e:
            self.get_logger().error(f'Failed to create CSV file: {str(e)}')
            return False
            
        return True

    def close_current_file(self):
        """Close the current CSV file and flush all remaining data"""
        # Always flush remaining data regardless of recording flag status
        self.flush_data_to_disk(force=True)
        
        # Close the file
        if self.csv_file is not None:
            try:
                self.csv_file.flush()
                self.csv_file.close()
                self.csv_file = None
                self.csv_writer = None
                self.get_logger().info(f'Closed trial_{self.current_trial}.csv')
                self.current_trial += 1
            except Exception as e:
                self.get_logger().error(f'Error closing file: {str(e)}')

    def recording_flag_callback(self, msg):
        """Callback to handle recording flag topic messages"""
        # Simply update the recording flag value - no need to create/close files
        # Data collection is continuous regardless of flag value
        if msg.data and not self.is_recording:
            # Set recording flag to 1
            self.is_recording = True
            self.get_logger().info("Recording flag set to 1")
        elif not msg.data and self.is_recording:
            # Set recording flag to 0
            self.is_recording = False
            self.get_logger().info("Recording flag set to 0")
        # No else needed - just maintain current state

    def goniometer_callback(self, msg):
        """Store the latest goniometer reading"""
        self.gposition = msg.position
        self.gvelocity = msg.velocity

    def impedance_callback(self, msg):
        """Store the latest goniometer reading"""
        self.impedance_torque = float(msg.tau_imp)

    def motor_state_callback(self, msg):
        """Direct callback for motor state messages when not using synchronizer"""
        try:
            # Use ROS time for precise timestamping
            timestamp = self.get_clock().now().nanoseconds / 1e9  # Convert to seconds
            
            # Lock the buffer during update to prevent race conditions
            with self.buffer_lock:
                self.data_buffer['timestamp'].append(timestamp)
                self.data_buffer['position'].append(msg.position)
                self.data_buffer['velocity'].append(msg.velocity)
                self.data_buffer['tau_fcomp'].append(0.0)  # Default value
                self.data_buffer['tau_imp'].append(self.impedance_torque)    # Default value
                self.data_buffer['Goniometer'].append(self.gposition)
                self.data_buffer['recording_flag'].append(self.is_recording)
                
                # If buffer size threshold is reached, trigger a flush
                if len(self.data_buffer['timestamp']) >= self.buffer_size:
                    self.flush_data_to_disk()
                    
        except Exception as e:
            self.get_logger().error(f'Error in motor_state_callback: {str(e)}')

    # def sync_callback(self, motor_msg, friction_msg, impedance_msg):
    #     """Process synchronized messages from all subscribed topics - always collecting data"""
    #     try:
    #         # Use ROS time for precise timestamping
    #         timestamp = self.get_clock().now().nanoseconds / 1e9  # Convert to seconds
            
    #         # Lock the buffer during update to prevent race conditions
    #         with self.buffer_lock:
    #             self.data_buffer['timestamp'].append(timestamp)
    #             # self.data_buffer['position'].append(motor_msg.position)
    #             # self.data_buffer['velocity'].append(motor_msg.velocity)
    #             # self.data_buffer['tau_fcomp'].append(friction_msg.tau_fcomp)
    #             # self.data_buffer['tau_imp'].append(impedance_msg.tau_imp)
    #             self.data_buffer['Goniometer'].append(self.goniometer_reading)
    #             self.data_buffer['recording_flag'].append(self.is_recording)
                
    #             # If buffer size threshold is reached, trigger a flush
    #             if len(self.data_buffer['timestamp']) >= self.buffer_size:
    #                 self.flush_data_to_disk()
                    
    #     except Exception as e:
    #         self.get_logger().error(f'Error in sync_callback: {str(e)}')

    def flush_data_callback(self):
        """Timer callback to periodically flush data to disk"""
        # Always flush data, not just during active recording
        self.flush_data_to_disk()

    def flush_data_to_disk(self, force=False):
        """Write buffered data to the CSV file"""
        # Always save data regardless of recording flag - just check if file is available
        if self.csv_file is None or self.csv_writer is None:
            return
            
        # Check if there's data to write
        with self.buffer_lock:
            buffer_size = len(self.data_buffer['timestamp'])
            if buffer_size == 0:
                return
                
            # Only write if we have enough data or if forced
            if buffer_size < 10 and not force:
                return
                
            try:
                # Write data rows to CSV - modified for selected fields only
                for i in range(buffer_size):
                    row = [
                        self.data_buffer['timestamp'][i],
                        self.data_buffer['position'][i],
                        self.data_buffer['velocity'][i],
                        self.data_buffer['tau_fcomp'][i],  # Default value
                        self.data_buffer['tau_imp'][i],    # Default value
                        self.data_buffer['Goniometer'][i],
                        1 if self.data_buffer['recording_flag'][i] else 0
                    ]
                    self.csv_writer.writerow(row)
                
                # Flush to disk
                self.csv_file.flush()
                
                # Log that we're writing data
                self.get_logger().debug(f"Wrote {buffer_size} rows to CSV file")
                
                # Clear the buffers after successful write
                for key in self.data_buffer:
                    self.data_buffer[key] = []
                    
            except Exception as e:
                self.get_logger().error(f'Error writing to CSV file: {str(e)}')

    def __del__(self):
        """Destructor to ensure files are closed"""
        self.close_current_file()

def main(args=None):
    rclpy.init(args=args)
    
    try:
        data_collector = DataCollectorNode()
        
        # Use a MultiThreadedExecutor for better performance
        executor = rclpy.executors.MultiThreadedExecutor()
        executor.add_node(data_collector)
        
        try:
            # Check for shutdown flag during spin
            while rclpy.ok():
                executor.spin_once(timeout_sec=0.1)
                if data_collector._force_shutdown:
                    data_collector.get_logger().info("Forced shutdown detected, exiting...")
                    break
        except KeyboardInterrupt:
            pass
        finally:
            # Ensure clean shutdown
            data_collector.close_current_file()
            executor.shutdown()
            data_collector.destroy_node()
            rclpy.shutdown()
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        rclpy.shutdown()

if __name__ == '__main__':
    main()