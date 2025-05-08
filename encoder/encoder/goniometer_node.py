#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64,Float32
from custom_msgs.msg import MotionState
import serial
import re
import math
import numpy as np
from collections import deque

class GoniometerNode(Node):
    def __init__(self):
        super().__init__('goniometer_node')
        
        # Create a publisher for the serial data
        self.publisher = self.create_publisher(MotionState, 'goniometer_state', 10)
        
        # Configure serial port - you may need to adjust these parameters
        self.serial_port = serial.Serial(
            port='/dev/ttyACM0',  # Change this to match your serial port
            baudrate=115200,
            timeout=1.0
        )
        
        # Create a timer that will call our callback every 0.1 seconds
        self.timer = self.create_timer(0.0025, self.timer_callback)
        self.get_logger().info('Goniometer node has started')
        self.multiplier = 1
        self.buffer = deque(maxlen=5)

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
        # self.get_logger().info(f'Calculated Velocity: {velocity}')

        return velocity
    
    def timer_callback(self):
        if self.serial_port.in_waiting:
            try:
                # Read a line from serial
                line = self.serial_port.readline()
                # print(line)
                
                decoded_line = line.decode('utf-8').strip()
                # Use regex to extract the number after "Read: "
                # print(decoded_line)
                value = int(decoded_line.split(': ')[1])
                
                
                #     if len(self.buffer) == 10:
                #         self.offset = np.mean(np.array(self.buffer))
            # once we have 5 samples, compute offset
            # subtract offset to get calibrated reading
                calibrated = int(value)*self.multiplier
                self.buffer.append(calibrated)
                velocity = self.velocity_5_point_backward(self.buffer)
                msg = MotionState()
                msg.position = calibrated
                msg.velocity = velocity
                self.publisher.publish(msg)
                self.get_logger().info(f'Published: {calibrated},{velocity}')
            
            except Exception as e:
                self.get_logger().error(f'Error reading serial data: {str(e)}')

    def __del__(self):
        if hasattr(self, 'serial_port') and self.serial_port.is_open:
            self.serial_port.close()

def main(args=None):
    rclpy.init(args=args)
    node = GoniometerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()