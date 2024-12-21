import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
import pigpio
import traceback
import threading


class AMT102VEncoderNode(Node):
    """
    A ROS2 node to read and publish encoder values from an AMT102-V encoder using the pigpio library.

    Parameters (ROS2 Parameters):
        channel_a_pin (int): GPIO pin number connected to encoder channel A. Default: 20
        channel_b_pin (int): GPIO pin number connected to encoder channel B. Default: 21
        publish_rate (float): Frequency (in Hz) at which the encoder position is published. Default: 100.0

    Publishes:
        'encoder_position' (std_msgs/msg/Int64): The current encoder position (relative).
    """

    def __init__(self) -> None:
        super().__init__('amt102v_encoder')
        self.get_logger().info("Initializing AMT102V Encoder Node...")

        # Declare and get parameters
        self.declare_parameter('channel_a_pin', 20)
        self.declare_parameter('channel_b_pin', 21)
        self.declare_parameter('publish_rate', 200.0)  # Publish at 100 Hz by default

        self.channel_a_pin = self._validate_int_param('channel_a_pin')
        self.channel_b_pin = self._validate_int_param('channel_b_pin')
        self.publish_rate = self._validate_float_param('publish_rate')
        
        # Ensure publish_rate is positive
        if self.publish_rate <= 0:
            self.get_logger().warn(
                f"Invalid publish_rate {self.publish_rate}, defaulting to 100 Hz.")
            self.publish_rate = 100.0

        self.position = 0  # Initialize encoder position
        self.position_lock = threading.Lock()  # Lock to ensure thread-safe access to position

        # Initialize Publisher
        self.encoder_publisher = self.create_publisher(Int64, 'encoder_position', 10)

        # Set a timer for publishing the encoder position
        # Convert Hz to period in seconds
        publish_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(publish_period, self.publish_encoder_position)

        self.pi = None  # pigpio instance
        self.callback_a = None
        self.callback_b = None

        try:
            # Initialize pigpio connection
            self.pi = pigpio.pi()
            if not self.pi.connected:
                self.get_logger().error("Failed to connect to pigpio daemon. Ensure pigpiod is running.")
                raise RuntimeError("Failed to connect to pigpio daemon.")
            self.get_logger().info("Connected to pigpio daemon.")

            # Configure the GPIO pins for encoder input with pull-ups
            self.pi.set_mode(self.channel_a_pin, pigpio.INPUT)
            self.pi.set_mode(self.channel_b_pin, pigpio.INPUT)
            self.pi.set_pull_up_down(self.channel_a_pin, pigpio.PUD_UP)
            self.pi.set_pull_up_down(self.channel_b_pin, pigpio.PUD_UP)
            self.get_logger().info(f"Configured GPIO pins {self.channel_a_pin} (A) and {self.channel_b_pin} (B) as inputs with pull-up resistors.")

            # Add callbacks for encoder channels
            # The callback will handle incrementing or decrementing the encoder position
            self.callback_a = self.pi.callback(self.channel_a_pin, pigpio.EITHER_EDGE, self.encoder_callback)
            self.callback_b = self.pi.callback(self.channel_b_pin, pigpio.EITHER_EDGE, self.encoder_callback)
            self.get_logger().info("Encoder callbacks initialized.")

        except Exception as e:
            self.get_logger().error("Error during initialization.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())
            self.cleanup()
            raise

        self.get_logger().info("AMT102V Encoder Node started.")

    def _validate_int_param(self, param_name: str) -> int:
        """
        Validate that a given ROS parameter is an integer.
        """
        param_value = self.get_parameter(param_name).value
        if not isinstance(param_value, int):
            self.get_logger().warn(f"Parameter '{param_name}' should be an integer. Using default value.")
            # fallback to default
            if param_name == 'channel_a_pin':
                return 20
            elif param_name == 'channel_b_pin':
                return 21
        return param_value

    def _validate_float_param(self, param_name: str) -> float:
        """
        Validate that a given ROS parameter is a float.
        """
        param_value = self.get_parameter(param_name).value
        if not isinstance(param_value, float):
            self.get_logger().warn(f"Parameter '{param_name}' should be a float. Using default value.")
            if param_name == 'publish_rate':
                return 100.0
        return param_value

    def encoder_callback(self, gpio: int, level: int, tick: int) -> None:
        """
        Callback function triggered on either rising or falling edge of encoder channels.

        Quadrature decoding logic:
        - Read the current states of both channels A and B.
        - If the transition on one channel leads or lags the other, we determine the direction.
        
        This logic works by comparing the states of the two pins at each interrupt:
        - If 'A' leads 'B', count up.
        - If 'B' leads 'A', count down.
        """
        try:
            current_a_state = self.pi.read(self.channel_a_pin)
            current_b_state = self.pi.read(self.channel_b_pin)

            # Determine direction based on which pin triggered and the relative states
            increment = 0
            if gpio == self.channel_a_pin:
                # If channel A changed, direction depends on channel B state relative to A
                if current_b_state != current_a_state:
                    increment = 1
                else:
                    increment = -1
            elif gpio == self.channel_b_pin:
                # If channel B changed, direction depends on channel A state relative to B
                if current_a_state == current_b_state:
                    increment = 1
                else:
                    increment = -1

            # Safely update position
            with self.position_lock:
                self.position += increment

        except Exception as e:
            self.get_logger().error("Error in encoder callback.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())

    def publish_encoder_position(self) -> None:
        """
        Publishes the current encoder position at the configured rate.
        """
        with self.position_lock:
            pos = self.position

        msg = Int64()
        msg.data = pos
        self.encoder_publisher.publish(msg)
        self.get_logger().debug(f'Published Encoder Position: {pos}')

    def cleanup(self) -> None:
        """
        Releases pigpio resources and cancels callbacks.
        """
        self.get_logger().info("Cleaning up encoder node resources...")
        try:
            if self.callback_a:
                self.callback_a.cancel()
            if self.callback_b:
                self.callback_b.cancel()
            if self.pi and self.pi.connected:
                self.pi.stop()
                self.get_logger().info("Disconnected from pigpio daemon.")
        except Exception as e:
            self.get_logger().error("Error during cleanup.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())
        self.get_logger().info("Cleanup complete.")

    def destroy_node(self) -> None:
        """
        Override destroy_node to ensure cleanup is always called.
        """
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
