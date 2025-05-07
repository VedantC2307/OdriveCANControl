import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Int32, Float32
from custom_msgs.msg import MotionState, FriCompTorque
class FrictionCompensationNode(Node):
    def __init__(self):
        super().__init__('friction_compensation_node')


        # Publisher to send torque commands
        self.subscription = self.create_subscription(
            MotionState,  
            'motor_state',  
            self.motor_state_callback,
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

    def motor_state_callback(self, msg):
        """Callback to receive position values in radians."""
        self.position = msg.position
        self.velocity = msg.velocity

        self.get_logger().info(f'Updated Position Buffer: {self.position}')
        self.get_logger().info(f'Updated counts to radians: {self.velocity}')


    def process_data(self):
        """Process the buffered position data and publish torque commands."""
        gain = 0.0525
        # Step 2: Compute compensation torque
        compensation_torque = gain * self.friction_compensation(self.velocity) # Unit is currnt

        # Step 3: Publish the fricition comp torque
        msg = FriCompTorque()
        msg.tau_fcomp = compensation_torque
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing Fircition Torque: {compensation_torque}')
        # self.publisher.publish(create_msg)

def main(args=None):
    rclpy.init(args=args)

    node = FrictionCompensationNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
