# Code not tested yet 

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
import RPi.GPIO as GPIO

class AMT102VEncoderNode(Node):
    def __init__(self):
        super().__init__('amt102v_encoder')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('channel_a_pin', 17),
                ('channel_b_pin', 27),
            ]
        )

        self.channel_a_pin = self.get_parameter('channel_a_pin').value
        self.channel_b_pin = self.get_parameter('channel_b_pin').value

        self.position = 0
        self.direction = 0

        self.encoder_publisher = self.create_publisher(Int64, 'encoder_position', 10)
        self.timer = self.create_timer(0.1, self.publish_encoder_position)  # Faster timer interval for real-time updates

        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Set up pins as inputs with pull-up resistors
        GPIO.setup(self.channel_a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.channel_b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Add interrupt events for both channels
        GPIO.add_event_detect(self.channel_a_pin, GPIO.BOTH, callback=self.encoder_callback, bouncetime=1)
        GPIO.add_event_detect(self.channel_b_pin, GPIO.BOTH, callback=self.encoder_callback, bouncetime=1)

    def encoder_callback(self, channel):
        a = GPIO.input(self.channel_a_pin)
        b = GPIO.input(self.channel_b_pin)

        if channel == self.channel_a_pin:
            if b != a:
                self.position += 1
                self.direction = 1
            else:
                self.position -= 1
                self.direction = -1
        elif channel == self.channel_b_pin:
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
        GPIO.remove_event_detect(self.channel_a_pin)
        GPIO.remove_event_detect(self.channel_b_pin)
        GPIO.cleanup()

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
