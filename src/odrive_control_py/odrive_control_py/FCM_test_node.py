import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Int64, Float32
from sensor_msgs.msg import JointState
from odrive_can.msg import ControlMessage
from collections import deque

class FrictionCompensationNode(Node):
    def __init__(self):
        super().__init__('friction_compensation_node')

        # Subscribe to position values (e.g., from a motor encoder)
        self.subscription = self.create_subscription(
            JointState,  # Message type
            'motor_state',  # Topic name
            self.state_callback,  # Callback function
            10  # QoS profile
        )

        # Publisher to publish friction compensation torque
        self.fcomp_publisher = self.create_publisher(
            Float32,  # Float32 메시지 타입
            'friction_comp_torque',  # 토픽 이름
            10  # QoS 프로파일
        )
        ## Friction model gain
        self.comp_gain = 0.0525

        self.publish_rate = 100.0  # Hz
        self.publish_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(self.publish_period, self.process_data)  # 100 Hz processing


    def friction_compensation(self, velocity):
        """
        Compute friction compensation torque based on velocity.
        """
        if abs(velocity) > 0.2:
            return 0.38 * np.sign(velocity) ## this part we need to check
        return 0.0

    def state_callback(self, msg):
        """Callback to receive position values and convert to radians."""

        self.position = msg.position
        self.velocity = msg.velocity


    def process_data(self):
        """Process the buffered position data and publish torque commands."""

        # Step 1: Compute compensation torque
        compensation_torque = self.comp_gain * self.friction_compensation(self.velocity)

        # Publish the compensation torque
        # We will not publish this torque directly to the motor because we will combine all torque from impedance and friction compensation and send it to motor
        torque_msg = Float32()
        torque_msg.data = compensation_torque  # 토크 값 설정
        self.fcomp_publisher.publish(torque_msg)  # 메시지 Publish
        self.get_logger().info(f'Published Torque Command: {compensation_torque}')

def main(args=None):
    rclpy.init(args=args)

    node = FrictionCompensationNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
