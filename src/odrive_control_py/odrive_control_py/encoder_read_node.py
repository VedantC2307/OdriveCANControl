# Code not tested yet 
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
import pigpio


class AMT102VEncoderNode(Node):
    def __init__(self):
        super().__init__('amt102v_encoder')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('channel_a_pin', 20),
                ('channel_b_pin', 21),
            ]
        )

        self.channel_a_pin = self.get_parameter('channel_a_pin').value
        self.channel_b_pin = self.get_parameter('channel_b_pin').value

        self.position = 0
        self.direction = 0

        self.encoder_publisher = self.create_publisher(Int64, 'encoder_position', 10)
        self.timer = self.create_timer(0.005, self.publish_encoder_position)  # Faster timer interval for real-time updates

        # Initialize pigpio
        self.pi = pigpio.pi()
        if not self.pi.connected:
            self.get_logger().error("Failed to connect to pigpio daemon.")
            raise RuntimeError("Failed to connect to pigpio daemon.")

        # Set up pins as inputs with pull-up resistors
        self.pi.set_mode(self.channel_a_pin, pigpio.INPUT)
        self.pi.set_mode(self.channel_b_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.channel_a_pin, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.channel_b_pin, pigpio.PUD_UP)

        # Add callbacks for edge detection
        self.pi.callback(self.channel_a_pin, pigpio.EITHER_EDGE, self.encoder_callback)
        self.pi.callback(self.channel_b_pin, pigpio.EITHER_EDGE, self.encoder_callback)

    def encoder_callback(self, gpio, level, tick):
        a = self.pi.read(self.channel_a_pin)
        b = self.pi.read(self.channel_b_pin)

        if gpio == self.channel_a_pin:
            if b != a:
                self.position += 1
                self.direction = 1
            else:
                self.position -= 1
                self.direction = -1
        elif gpio == self.channel_b_pin:
            if a != b:
                self.position -= 1
                self.direction = -1
            else:
                self.position += 1
                self.direction = 1

    def publish_encoder_position(self):
        msg = Int64()
        msg.data = self.position
        self.encoder_publisher.publish(msg)
        self.get_logger().info(f'Encoder Position: {self.position}, Direction: {self.direction}')

    def cleanup(self):
        self.pi.stop()


def main(args=None):
    rclpy.init(args=args)

    encoder_node = AMT102VEncoderNode()

    try:
        rclpy.spin(encoder_node)
    except KeyboardInterrupt:
        encoder_node.get_logger().info("Encoder reading stopped by user")
    finally:
        encoder_node.cleanup()
        encoder_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
