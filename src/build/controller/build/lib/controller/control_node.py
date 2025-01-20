import rclpy
from rclpy.node import Node
from odrive_can.msg import ControlMessage, ControllerStatus
from std_msgs.msg import Float32
from rclpy.qos import QoSProfile

class ODriveControl(Node):
    def __init__(self):
        super().__init__('odrive_control')
        self.get_logger().info('Starting node')

        self.subscription = self.create_subscription(
            ControllerStatus,
            '/odrive_axis0/controller_status',
            self.control_callback,
            10
        )

        self.publisher = self.create_publisher(
            ControlMessage,
            '/odrive_axis0/control_message',
            10
        )

        self.position_value = None  # Store the last received position value

    def control_callback(self, msg):
        # Received logger
        self.get_logger().info('Implementing Control Callback')

        try:
            self.position_value = msg.vel_estimate
            self.get_logger().info(f'Received: {self.position_value}')

            # Call the impedance control logic after receiving position value
            self.impedance_control_logic_callback(self.position_value)
        except AttributeError as e:
            self.get_logger().info(f'Message attribute error: {e}')

    def impedance_control_logic_callback(self, position_value):
        self.get_logger().info('Implementing Control logic loop')

        # Some control logic with torque value as output



        # Impedance control logic
        position = position_value
        self.get_logger().info(f'Received: {position}')

        torque = 0.0

        # Send Torque message
        create_msg = ControlMessage()
        create_msg.control_mode = 2  # Torque = 1, Velocity = 2 Position = 3
        create_msg.input_mode = 1  # Passthrough = 1
        create_msg.input_pos = 0.0
        create_msg.input_vel = 0.2
        create_msg.input_torque = torque

        self.get_logger().info(f'Publishing: {create_msg}')

        self.publisher.publish(create_msg)


    # def close_node(self):
    #     # Set the input_vel to 0 before shutting down
    #     self.get_logger().info('Shutting down node, setting input_vel to 0.')

    #     create_msg = ControlMessage()
    #     create_msg.control_mode = 2  # Torque = 1, Velocity = 2, Position = 3
    #     create_msg.input_mode = 1  # Passthrough = 1
    #     create_msg.input_pos = 0.0
    #     create_msg.input_vel = 0.0  # Set velocity to 0
    #     create_msg.input_torque = 0.0

    #     self.get_logger().info(f'Publishing: {create_msg} before shutdown')

    #     # Publish the message
    #     self.publisher.publish(create_msg)

    #     # Call the original destroy_node method to clean up
    #     super().destroy_node()

def main():
    rclpy.init()
    simple_control = ODriveControl()
    rclpy.spin(simple_control)
    ODriveControl.destroy_node()
    # ODriveControl.close_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
