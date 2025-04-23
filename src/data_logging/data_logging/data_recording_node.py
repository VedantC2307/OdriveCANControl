#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.parameter import Parameter
from message_filters import ApproximateTimeSynchronizer, Subscriber
from custom_msgs.srv import ODriveCommand
from custom_msgs.msg import FrictionComp, ImpedanceTorque, MotionState
from std_msgs.msg import Float32MultiArray, Bool
from std_srvs.srv import SetBool
import h5py
import numpy as np
import os
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
        self.declare_parameter('save_dir', '/home/vedant/gaitlab_ws/OdriveCANControl/src/data_logging/data_logging/data')
        self.declare_parameter('subject_name', 'subject1')  # Changed from subject_number to subject_name
        self.declare_parameter('buffer_size', 100)  # Number of samples to buffer before writing
        self.declare_parameter('sync_slop', 0.01)   # Time tolerance for message synchronization in seconds
        
        # Get parameters
        self.save_dir = self.get_parameter('save_dir').value
        self.subject_name = self.get_parameter('subject_name').value  # Use subject_name directly
        self.buffer_size = self.get_parameter('buffer_size').value
        self.sync_slop = self.get_parameter('sync_slop').value
        
        # Format subject name and ensure directory exists
        # No need to format the subject name, use it directly
        self.subject_dir = os.path.join(self.save_dir, self.subject_name)
        if not os.path.exists(self.subject_dir):
            os.makedirs(self.subject_dir)
            self.get_logger().info(f'Created directory: {self.subject_dir}')
        
        # File handling variables
        self.current_trial = 1
        self.is_recording = False
        self.h5_file = None
        self.data_group = None
        
        # Create data buffers for efficient batch writing
        self.data_buffer = {
            'timestamp': [],
            'position': [],
            'velocity': [],
            'tau_fcomp': [],
            'tau_imp': []
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
        
        # Create synchronized subscribers
        self.motor_sub = Subscriber(self, MotionState, 'motor_state', qos_profile=self.reliable_qos)
        self.friction_sub = Subscriber(self, FrictionComp, 'friction_comp_torque', qos_profile=self.reliable_qos)
        self.impedance_sub = Subscriber(self, ImpedanceTorque, 'impedance_torque', qos_profile=self.reliable_qos)
        
        # Synchronize the messages by timestamp
        self.sync = ApproximateTimeSynchronizer(
            [self.motor_sub, self.friction_sub, self.impedance_sub],
            queue_size=30,
            slop=self.sync_slop
        )
        self.sync.registerCallback(self.sync_callback)
        
        # Timer for periodically writing buffered data (at 10Hz - fine for flushing data)
        self.flush_timer = self.create_timer(
            0.1,  # 10Hz for flushing data to disk
            self.flush_data_callback,
            callback_group=self.timer_callback_group
        )
        
        # Register shutdown handlers
        self.register_shutdown_handlers()
        
        self.get_logger().info('Data collector node initialized')
        self.get_logger().info(f'Recording data for subject {self.subject_name}')
        self.get_logger().info(f'Use service "toggle_recording" or publish to "recording_flag" topic to control recording')

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
        """Create a new HDF5 file with chunked datasets for efficient writing"""
        try:
            filename = os.path.join(self.subject_dir, f'trial_{self.current_trial}.h5')
            
            # Ensure the file is closed if it exists
            if self.h5_file is not None:
                self.h5_file.close()
            
            # Create new file with chunked datasets
            self.h5_file = h5py.File(filename, 'w')
            self.data_group = self.h5_file.create_group("TrialData")
            
            # Define chunk size - optimize for 100Hz data
            chunk_size = 100  # 1 second of data at 100Hz
            
            # Pre-create datasets with chunked storage for better performance
            self.data_group.create_dataset(
                'timestamp',
                shape=(0,),
                maxshape=(None,),
                dtype='float64',
                chunks=(chunk_size,)
            )
            
            self.data_group.create_dataset(
                'position',
                shape=(0,),
                maxshape=(None,),
                dtype='float64',
                chunks=(chunk_size,)
            )
            
            self.data_group.create_dataset(
                'velocity',
                shape=(0,),
                maxshape=(None,),
                dtype='float64',
                chunks=(chunk_size,)
            )
            
            self.data_group.create_dataset(
                'tau_fcomp',
                shape=(0,),
                maxshape=(None,),
                dtype='float64',
                chunks=(chunk_size,)
            )
            
            self.data_group.create_dataset(
                'tau_imp',
                shape=(0,),
                maxshape=(None,),
                dtype='float64',
                chunks=(chunk_size,)
            )
            
            # Store metadata
            self.data_group.attrs['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data_group.attrs['subject'] = self.subject_name
            self.data_group.attrs['trial'] = self.current_trial
            
            self.get_logger().info(f'Created new file: {filename}')
            
        except Exception as e:
            self.get_logger().error(f'Failed to create HDF5 file: {str(e)}')
            return False
            
        return True

    def close_current_file(self):
        """Close the current HDF5 file and flush all remaining data"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        # Flush any remaining data in the buffer
        self.flush_data_to_disk(force=True)
        
        # Close the file
        if self.h5_file is not None:
            try:
                # Add end time metadata
                if self.data_group is not None:
                    self.data_group.attrs['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.h5_file.flush()
                self.h5_file.close()
                self.h5_file = None
                self.data_group = None
                self.get_logger().info(f'Closed trial_{self.current_trial}.h5')
                self.current_trial += 1
            except Exception as e:
                self.get_logger().error(f'Error closing file: {str(e)}')

    # def toggle_recording_callback(self, request, response):
    #     """Handle service requests to toggle recording state"""
    #     if request.data:  # Start recording
    #         if not self.is_recording:
    #             if self.create_new_file():
    #                 self.is_recording = True
    #                 # Clear any old data from buffer
    #                 with self.buffer_lock:
    #                     for key in self.data_buffer:
    #                         self.data_buffer[key] = []
    #                 response.message = f"Started recording trial_{self.current_trial}"
    #                 response.success = True
    #             else:
    #                 response.message = "Failed to create recording file"
    #                 response.success = False
    #         else:
    #             response.message = "Already recording"
    #             response.success = False
    #     else:  # Stop recording
    #         if self.is_recording:
    #             self.close_current_file()
    #             response.message = "Stopped recording"
    #             response.success = True
    #         else:
    #             response.message = "Not recording"
    #             response.success = False
    #     return response

    def recording_flag_callback(self, msg):
        """Callback to handle recording flag topic messages"""
        if msg.data:  # Start recording
            if not self.is_recording:
                if self.create_new_file():
                    self.is_recording = True
                    # Clear any old data from buffer
                    with self.buffer_lock:
                        for key in self.data_buffer:
                            self.data_buffer[key] = []
                    self.get_logger().info(f"Started recording trial_{self.current_trial}")
                else:
                    self.get_logger().error("Failed to create recording file")
            else:
                self.get_logger().info("Already recording")
        else:  # Stop recording
            if self.is_recording:
                self.close_current_file()
                self.get_logger().info("Stopped recording")
            else:
                self.get_logger().info("Not recording")

    def sync_callback(self, motor_msg, friction_msg, impedance_msg):
        """Process synchronized messages from all subscribed topics"""
        if not self.is_recording:
            return
            
        try:
            # Use ROS time for precise timestamping
            timestamp = self.get_clock().now().nanoseconds / 1e9  # Convert to seconds
            
            # Lock the buffer during update to prevent race conditions
            with self.buffer_lock:
                self.data_buffer['timestamp'].append(timestamp)
                self.data_buffer['position'].append(motor_msg.position)
                self.data_buffer['velocity'].append(motor_msg.velocity)
                self.data_buffer['tau_fcomp'].append(friction_msg.tau_fcomp)
                self.data_buffer['tau_imp'].append(impedance_msg.tau_imp)
                
                # If buffer size threshold is reached, trigger a flush
                if len(self.data_buffer['timestamp']) >= self.buffer_size:
                    self.flush_data_to_disk()
                    
        except Exception as e:
            self.get_logger().error(f'Error in sync_callback: {str(e)}')

    def flush_data_callback(self):
        """Timer callback to periodically flush data to disk"""
        if self.is_recording:
            self.flush_data_to_disk()

    def flush_data_to_disk(self, force=False):
        """Write buffered data to the HDF5 file"""
        if not self.is_recording and not force:
            return
            
        if self.h5_file is None or self.data_group is None:
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
                # Convert buffer lists to numpy arrays for efficient writing
                timestamp_array = np.array(self.data_buffer['timestamp'], dtype=np.float64)
                position_array = np.array(self.data_buffer['position'], dtype=np.float64)
                velocity_array = np.array(self.data_buffer['velocity'], dtype=np.float64)
                tau_fcomp_array = np.array(self.data_buffer['tau_fcomp'], dtype=np.float64)
                tau_imp_array = np.array(self.data_buffer['tau_imp'], dtype=np.float64)
                
                # Resize datasets and append new data
                dataset = self.data_group['timestamp']
                old_size = dataset.shape[0]
                dataset.resize((old_size + buffer_size,))
                dataset[old_size:] = timestamp_array
                
                dataset = self.data_group['position']
                dataset.resize((old_size + buffer_size,))
                dataset[old_size:] = position_array
                
                dataset = self.data_group['velocity']
                dataset.resize((old_size + buffer_size,))
                dataset[old_size:] = velocity_array
                
                dataset = self.data_group['tau_fcomp']
                dataset.resize((old_size + buffer_size,))
                dataset[old_size:] = tau_fcomp_array
                
                dataset = self.data_group['tau_imp']
                dataset.resize((old_size + buffer_size,))
                dataset[old_size:] = tau_imp_array
                
                # Periodically flush to disk to ensure data is saved
                if buffer_size >= self.buffer_size or force:
                    self.h5_file.flush()
                
                # Clear the buffers after successful write
                for key in self.data_buffer:
                    self.data_buffer[key] = []
                    
            except Exception as e:
                self.get_logger().error(f'Error writing to HDF5 file: {str(e)}')

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