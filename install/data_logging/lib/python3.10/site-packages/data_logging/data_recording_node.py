import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from odrive_can.msg import ControllerStatus, ControlMessage, CollectedData  # Assuming CollectedData message type
import pandas as pd
from datetime import datetime
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import numpy as np

class InfoCollectorNode(Node):
    def __init__(self):
        super().__init__('info_collector')
        
        # QoS Profile for better reliability
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Parameters
        self.declare_parameter('dt', 0.1)
        self.dt = self.get_parameter('dt').value
        
        # Callback groups for thread safety
        self.callback_group = MutuallyExclusiveCallbackGroup()
        
        # Initialize subscribers with QoS profiles
        self.sub_encoder_position = self.create_subscription(
            Int64,
            'encoder_position',
            self.callback_encoder_position,
            qos_profile,
            callback_group=self.callback_group
        )
        
        self.sub_controller_status = self.create_subscription(
            ControllerStatus,
            'odrive_axis0/controller_status',
            self.callback_controller_status,
            qos_profile,
            callback_group=self.callback_group
        )
        
        self.sub_control_message = self.create_subscription(
            ControlMessage,
            'odrive_axis0/control_message',
            self.callback_control_message,
            qos_profile,
            callback_group=self.callback_group
        )
        
        # Initialize publisher for collected data
        self.pub_collected_data = self.create_publisher(
            CollectedData,
            'collected_data',
            qos_profile
        )
        
        # Data storage
        self.data = pd.DataFrame(columns=[
            'timestamp', 'encoder_position', 'pos_estimate', 'vel_estimate',
            'torque_target', 'torque_estimate', 'iq_setpoint', 'iq_measured',
            'active_errors', 'axis_state', 'procedure_result', 'trajectory_done_flag',
            'control_mode', 'input_mode', 'input_pos', 'input_vel', 'input_torque'
        ])
        
        # Initialize placeholders for latest data
        self.latest_data = {col: np.nan for col in self.data.columns if col != 'timestamp'}
        
        # Create timer for periodic data publishing
        self.create_timer(self.dt, self.publish_data, callback_group=self.callback_group)
        
        self.get_logger().info('Info Collector Node initialized')

    def callback_encoder_position(self, msg):
        self.latest_data['encoder_position'] = msg.data
        self.update_data()

    def callback_controller_status(self, msg):
        self.latest_data.update({
            'pos_estimate': msg.pos_estimate,
            'vel_estimate': msg.vel_estimate,
            'torque_target': msg.torque_target,
            'torque_estimate': msg.torque_estimate,
            'iq_setpoint': msg.iq_setpoint,
            'iq_measured': msg.iq_measured,
            'active_errors': msg.active_errors,
            'axis_state': msg.axis_state,
            'procedure_result': msg.procedure_result,
            'trajectory_done_flag': msg.trajectory_done_flag
        })
        self.update_data()

    def callback_control_message(self, msg):
        self.latest_data.update({
            'control_mode': msg.control_mode,
            'input_mode': msg.input_mode,
            'input_pos': msg.input_pos,
            'input_vel': msg.input_vel,
            'input_torque': msg.input_torque
        })
        self.update_data()

    def update_data(self):
        timestamp = self.get_clock().now().to_msg()
        new_row = {'timestamp': timestamp, **self.latest_data}
        self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)

    def publish_data(self):
        if not self.data.empty:
            msg = CollectedData()
            latest_row = self.data.iloc[-1]
            
            # Populate the message with the latest data
            # Note: Adjust these fields based on your CollectedData message definition
            msg.timestamp = latest_row['timestamp']
            msg.encoder_position = latest_row['encoder_position']
            msg.pos_estimate = latest_row['pos_estimate']
            # ... populate other fields ...
            
            self.pub_collected_data.publish(msg)

    def save_data_to_csv(self, filename='data_log.csv'):
        try:
            self.data.to_csv(filename, index=False)
            self.get_logger().info(f'Data successfully saved to {filename}')
        except Exception as e:
            self.get_logger().error(f'Failed to save data: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = InfoCollectorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.save_data_to_csv()
        node.get_logger().info('Saving data and shutting down...')
    except Exception as e:
        node.get_logger().error(f'Unexpected error: {str(e)}')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()