import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from custom_msgs.msg import MotionState
import RPi.GPIO as GPIO
import traceback
from collections import deque
import numpy as np

class AMT102VEncoderNode(Node):
    """
    A ROS2 node to read and publish encoder values from an AMT102-V encoder using RPi.GPIO.
    """

    def __init__(self) -> None:
        super().__init__('amt102v_encoder')
        self.get_logger().info("Initializing AMT102V Encoder Node...")

        # Declare parameters for GPIO pins
        self.declare_parameter('channel_a_pin', 21)
        self.declare_parameter('channel_b_pin', 20)

        # Get parameters
        self.channel_a_pin = self.get_parameter('channel_a_pin').get_parameter_value().integer_value
        self.channel_b_pin = self.get_parameter('channel_b_pin').get_parameter_value().integer_value

        self.get_logger().info(f'channel_a_pin: {self.channel_a_pin}')
        self.get_logger().info(f'channel_b_pin: {self.channel_b_pin}')

        # Initialize encoder position
        self.position = 0
        self.last_A = 0  # Store the last state of channel A

        # Create Publisher
        self.history_len = 5
        self.input_buffer = deque(maxlen=self.history_len)
        # Initialize Publisher
        self.motor_state_publisher = self.create_publisher(MotionState, 'motor_state', 10)

        # Setup timer for publishing
        publish_rate = 100.0  # Hz
        self.publish_period = 1.0 / publish_rate
        self.timer = self.create_timer(self.publish_period, self.publish_motor_state)

        try:
            # Initialize RPi.GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.channel_a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.channel_b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Read initial channel A state
            self.last_A = GPIO.input(self.channel_a_pin)

            # Add event detects for both channels (typical for quadrature)
            GPIO.add_event_detect(self.channel_a_pin, GPIO.BOTH, callback=self.encoder_callback)
            GPIO.add_event_detect(self.channel_b_pin, GPIO.BOTH)

            self.get_logger().info("Encoder callbacks initialized.")

        except Exception as e:
            self.get_logger().error("Error during GPIO initialization.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())
            self.cleanup()
            raise

        self.get_logger().info("AMT102V Encoder Node started.")

    def encoder_callback(self, channel):
        """
        RPi.GPIO callback for both channel A and channel B events.
        Only 'channel' (pin number) is passed to this function by RPi.GPIO.
        """
        try:
            current_A = GPIO.input(self.channel_a_pin)
            current_B = GPIO.input(self.channel_b_pin)

            # Simple decode logic: check for rising edge on channel A, then check channel B
            if (self.last_A == 0) and (current_A == 1):
                # Rising edge on A
                if current_B == 0:
                    self.position += 1  # A leads B => CW
                else:
                    self.position -= 1  # B leads A => CCW

            # Update last_A
            self.last_A = current_A

        except Exception as e:
            self.get_logger().error("Error in encoder callback.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())


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

    def publish_motor_state(self) -> None:
        """
        Publishes the current encoder position at the configured rate.
        """
        pos = self.position * (3/8192) # unit radian
        
        # Compute Velocity
        self.input_buffer.append(pos)
        if len(self.input_buffer) < self.history_len:
            return
        velocity = self.velocity_5_point_backward(self.input_buffer) # unit radians/sec
        msg = MotionState()
        msg.position = pos
        msg.velocity = velocity
        self.motor_state_publisher.publish(msg)
        self.get_logger().debug(f'Published Motor Position: {pos}')
        self.get_logger().debug(f'Published Motor Velocity: {velocity}')

    def cleanup(self) -> None:
        """
        RPi.GPIO cleanup
        """
        self.get_logger().info("Cleaning up encoder node resources...")
        try:
            GPIO.cleanup()
        except Exception as e:
            self.get_logger().error("Error during GPIO cleanup.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())
        self.get_logger().info("Cleanup complete.")

    def destroy_node(self) -> None:
        self.cleanup()
        super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    encoder_node = None
    try:
        encoder_node = AMT102VEncoderNode()
        rclpy.spin(encoder_node)
    except KeyboardInterrupt:
        if encoder_node:
            encoder_node.get_logger().info("Encoder reading stopped by user.")
    except Exception as e:
        if encoder_node:
            encoder_node.get_logger().error("Unhandled exception in main.")
            encoder_node.get_logger().error(str(e))
            encoder_node.get_logger().error(traceback.format_exc())
    finally:
        if encoder_node is not None:
            encoder_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
