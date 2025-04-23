import rclpy
from rclpy.node import Node
from custom_msgs.msg import MotionState # Replace this with the actual MotionState message import

class MotorStatePublisher(Node):
    def __init__(self):
        super().__init__('motor_state_publisher')
        self.motor_state_publisher = self.create_publisher(MotionState, 'motor_state', 10)  # Replace Int32 with MotionState
        self.global_rate = 100
        self.timer = self.create_timer(1/self.global_rate, self.publish_motor_state)
        self.counter = 0.0

    def publish_motor_state(self):
        msg = MotionState()  # Replace Int32 with MotionState
        msg.position = self.counter  # Modify this according to MotionState structure
        msg.velocity = 2.5
        self.motor_state_publisher.publish(msg)
        self.get_logger().info(f'Publishing: {self.counter}')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = MotorStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
