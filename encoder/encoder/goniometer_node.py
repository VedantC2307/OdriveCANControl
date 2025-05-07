#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
import serial
import re

class GoniometerNode(Node):
    def __init__(self):
        super().__init__('goniometer_node')
        
        # Create a publisher for the serial data
        self.publisher = self.create_publisher(Int64, 'goniometer_reading', 10)
        
        # Configure serial port - you may need to adjust these parameters
        self.serial_port = serial.Serial(
            port='/dev/ttyACM0',  # Change this to match your serial port
            baudrate=115200,
            timeout=1.0
        )
        
        # Create a timer that will call our callback every 0.1 seconds
        self.timer = self.create_timer(0.001, self.timer_callback)
        self.get_logger().info('Goniometer node has started')

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

                msg = Int64()
                msg.data = value
                self.publisher.publish(msg)
                self.get_logger().debug(f'Published: {value}')
            
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