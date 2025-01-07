import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Int32, Float32
from custom_msgs.msg import MotionState

class FrictionCompensationNode(Node):
    def __init__(self):
        super().__init__('friction_compensation_node')

        # Subscribe to position values (e.g., from a motor encoder)
        self.subscription = self.create_subscription(
            Int32,  # Message type
            'encoder_position',  # Topic name
            self.position_callback,
            10  # QoS profile
        )

        # Publisher to send torque commands
        self.publisher = self.create_publisher(
            MotionState,  
            'motor_state',  
            10  # QoS profile
        )

        self.position_data = []  # Buffer to store incoming position data
        self.counts_to_rads = 0.0

        self.publish_rate = 100.0  # Hz
        self.publish_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(self.publish_period, self.process_data)  # 20 Hz processing

    def velocity_5_point_backward(self, position):
        """
        Calculate velocity using the 5-point backward difference method.
        """
        coefficients = np.array([-25, 48, -36, 16, -3]) / (12.0 * self.publish_period)

        if len(position) < 5:
            return 0.0  # Return 0.0 if insufficient data for velocity calculation
        
        # self.get_logger().info(f'Calculated Position: {position}')

        # Compute velocity using the 5-point backward difference
        velocity = np.dot(position, coefficients)
        self.get_logger().info(f'Calculated Velocity: {velocity}')

        return velocity

    def friction_compensation(self, velocity):
        """
        Compute friction compensation torque based on velocity.
        """
        if abs(velocity) > 0.2:
            return 0.38 * np.sign(velocity)
        return 0.0

    def position_callback(self, msg):
        """Callback to receive position values in radians."""
        counts = msg.data
        self.counts_to_rads = counts * (3/8192) 
        self.position_data.append(self.counts_to_rads)
        # Maintain a fixed buffer size of 5
        if len(self.position_data) > 5:
            self.position_data.pop(0)

        self.get_logger().info(f'Updated Position Buffer: {self.position_data}')
        self.get_logger().info(f'Updated counts to radians: {self.counts_to_rads}')


    def process_data(self):
        """Process the buffered position data and publish torque commands."""
        gain = 0.0525
        if len(self.position_data) < 5:
            return  # Wait for sufficient data
        
        # Step 1: Compute velocity
        velocity = self.velocity_5_point_backward(self.position_data)

        # Step 2: Compute compensation torque
        compensation_torque = gain * self.friction_compensation(velocity)

        # Step 3: Combine with input torque (placeholder for actual input torque logic)
        input_torque = 0.0  # Example constant input torque
        total_torque = input_torque + compensation_torque

        msg = MotionState()
        msg.position = float(self.counts_to_rads)  # Single position value
        msg.velocity = float(velocity)  # Single velocity value
        self.publisher.publish(msg)

        # Step 4: Publish the torque command
        # create_msg = ControlMessage()
        # create_msg.control_mode = 1  # Torque control
        # create_msg.input_mode = 1  # Passthrough
        # create_msg.input_pos = 0.0
        # create_msg.input_vel = 0.0
        # create_msg.input_torque = total_torque

        # self.get_logger().info(f'Publishing Torque Command: {total_torque}')
        # self.publisher.publish(create_msg)


def main(args=None):
    rclpy.init(args=args)

    node = FrictionCompensationNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
