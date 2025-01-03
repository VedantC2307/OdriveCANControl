import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from sensor_msgs.msg import JointState
import pigpio
import traceback
import threading
import numpy as np
from collections import deque


class AMT102VEncoderNode(Node):
    """
    A ROS2 node to read and publish encoder values from an AMT102-V encoder using the pigpio library.

    Publishes:
        'encoder_position' (std_msgs/msg/Int64): The current encoder position (relative).
    """
    def __init__(self) -> None:
        super().__init__('amt102v_encoder')
        self.get_logger().info("Initializing AMT102V Encoder Node...")

        self.position = 0  # Initialize encoder position
        self.position_lock = threading.Lock()  # Lock to ensure thread-safe access to position

        # Initialize Publisher
        self.state_publisher = self.create_publisher(JointState, 'motor_state', 10)

        # Default publish rate
        publish_rate = 100.0  # Hz
        publish_period = 1.0 / publish_rate
        self.timer = self.create_timer(publish_period, self.publish_motor_state)

        self.pi = None  # pigpio instance
        self.callback_a = None
        self.callback_b = None

        # Default GPIO pins for encoder please use variable names instead of hardcoding
        self.channel_a_pin = 20
        self.channel_b_pin = 21

        # Position buffer
        self.position_buffer = deque(maxlen=5)  # Buffer to store incoming position data

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


    def publish_motor_state(self):
        """모터 상태를 계산하고 Publish."""
        # 시뮬레이션 또는 센서 데이터

        # JointState 메시지 생성
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()  # 현재 시간
        msg.name = ['motor_1']  # 모터 이름
        msg.position = [self.position]
        msg.velocity = [self.velcotiy]
        msg.effort = []  # 토크 값이 없다면 빈 리스트로 설정

        # 메시지 Publish
        self.state_publisherß.publish(msg)
        self.get_logger().info(f'Published Motor State: position={self.motor_position}, velocity={self.motor_velocity}')


    def encoder_callback(self, gpio: int, level: int, tick: int) -> None:
        """
        Callback function triggered on either rising or falling edge of encoder channels.

        Quadrature decoding logic:
        - Read the current states of both channels A and B.
        - If the transition on one channel leads or lags the other, we determine the direction.
        """
        try:
            # can use self.channel_a_pin = 20, self.channel_b_pin = 21 right?
            current_a_state = self.pi.read(21)  # GPIO pin for channel A
            current_b_state = self.pi.read(20)  # GPIO pin for channel B

            increment = 0
            if gpio == 21:  # If channel A changed
                increment = 1 if current_b_state != current_a_state else -1
            elif gpio == 20:  # If channel B changed
                increment = 1 if current_a_state == current_b_state else -1

            with self.position_lock:
                self.position += increment


            ## Put Velocity Calculation here
            self.position_buffer.append(self.position)
            self.velcotiy = self.velocity_5_point_backward(self.position_buffer)
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
