#ros2 run odrive_control_py encoder_read_node --ros-args --params-file ./src/odrive_control_py/config/params.yaml
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from custom_msgs.msg import MotionState
# import pigpio
import traceback
import threading
import RPi.GPIO as GPIO 
import time 
from collections import deque
import numpy as np

class AMT102VEncoderNode(Node):
    """
    A ROS2 node to read and publish encoder values from an AMT102-V encoder using the pigpio library.

    Publishes:
        'encoder_position' (std_msgs/msg/Int64): The current encoder position (relative).
    """

    def __init__(self) -> None:
        super().__init__('amt102v_encoder')
        self.get_logger().info("Initializing AMT102V Encoder Node...")

        # Declare parameters for GPIO pins
        self.declare_parameter('channel_a_pin', 21)
        self.declare_parameter('channel_b_pin', 20)

        # Get parameters for GPIO pins
        channel_a_pin = self.get_parameter('channel_a_pin').get_parameter_value().integer_value
        channel_b_pin = self.get_parameter('channel_b_pin').get_parameter_value().integer_value

        self.get_logger().info(f'channel_a_pin:{channel_a_pin}')
        self.get_logger().info(f'channel_a_pin:{channel_b_pin}')

        self.position = 0  # Initialize encoder position
        self.position_lock = threading.Lock()  # Lock to ensure thread-safe access to position
        
        self.history_len = 5
        self.input_buffer = deque(maxlen=self.history_len)
        # Initialize Publisher
        self.motor_state_publisher = self.create_publisher(MotionState, 'motor_state', 10)

        # Default publish rate
        publish_rate = 100.0  # Hz
        publish_period = 1.0 / publish_rate
        self.timer = self.create_timer(publish_period, self.motor_state_publisher)

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
            self.pi.set_mode(channel_a_pin, pigpio.INPUT)
            self.pi.set_mode(channel_b_pin, pigpio.INPUT)
            self.pi.set_pull_up_down(channel_a_pin, pigpio.PUD_UP)
            self.pi.set_pull_up_down(channel_b_pin, pigpio.PUD_UP)
            self.get_logger().info(f"Configured GPIO pins {channel_a_pin} (A) and {channel_b_pin} (B) as inputs with pull-up resistors.")

            # Add callbacks for encoder channels
            self.callback_a = self.pi.callback(channel_a_pin, pigpio.EITHER_EDGE, self.encoder_callback)
            self.callback_b = self.pi.callback(channel_b_pin, pigpio.EITHER_EDGE, self.encoder_callback)
            self.get_logger().info("Encoder callbacks initialized.")

        except Exception as e:
            self.get_logger().error("Error during initialization.")
            self.get_logger().error(str(e))
            self.get_logger().error(traceback.format_exc())
            self.cleanup()
            raise

        self.get_logger().info("AMT102V Encoder Node started.")

    def encoder_callback(self, gpio: int, level: int, tick: int) -> None:
        """
        Callback function triggered on either rising or falling edge of encoder channels.

        Quadrature decoding logic:
        - Read the current states of both channels A and B.
        - If the transition on one channel leads or lags the other, we determine the direction.
        """
        try:
            current_a_state = self.pi.read(self.get_parameter('channel_a_pin').value)  # GPIO pin for channel A
            current_b_state = self.pi.read(self.get_parameter('channel_b_pin').value)  # GPIO pin for channel B

            increment = 0
            if gpio == self.get_parameter('channel_b_pin').value:  # If channel A changed
                increment = 1 if current_b_state != current_a_state else -1
            elif gpio == self.get_parameter('channel_b_pin').value:  # If channel B changed
                increment = 1 if current_a_state == current_b_state else -1

            self.position += increment
            # with self.position_lock:
            #     self.position += increment

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
        # with self.position_lock:
        #     pos = self.position
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


        # Compute velocity
        

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