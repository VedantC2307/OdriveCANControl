#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import serial
import re
import time

class GoniometerNode(Node):
    def __init__(self):
        super().__init__('goniometer_node')
        
        # Create a publisher for the serial data
        self.publisher = self.create_publisher(Bool, 'recording_flag', 10)
        
        # Configure serial port - you may need to adjust these parameters
        self.serial_port = serial.Serial(
            port='/dev/ttyUSB0',  # Change this to match your serial port
            baudrate=115200,
            timeout=1.0
        )

        # Create a timer that will call our callback every 0.1 seconds
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.get_logger().info(' node has started')

    # def timer_callback(self):
    #     if self.serial_port.in_waiting:
    #         try:
    #             # Read a line from serial
    #             line = self.serial_port.readline()
    #             # print(line)
                    
    #             # Decode using ASCII and strip \r\n
    #             decoded_line = line.decode('ascii').strip()
                
    #             # Convert the string directly to integer
    #             value = int(decoded_line)
    #             print("Time:", time.time())
    #             print("Value:", value)

    #             msg = Int32()
    #             msg.data = value
    #             # self.publisher.publish(msg)
    #             self.get_logger().debug(f'Published: {value}')
            
    #         except Exception as e:
    #             self.get_logger().error(f'Error reading serial data: {str(e)}')

    def timer_callback(self):
        try:
            # Check if there's data available
            if self.serial_port.in_waiting:
                # Read all available data but keep only the last line
                lines = []
                while self.serial_port.in_waiting:
                    line = self.serial_port.readline()
                    lines.append(line)
                
                # Process only the most recent line
                if lines:
                    latest_line = lines[-1]
                    decoded_line = latest_line.decode('ascii').strip()
                    
                    # Convert to integer
                    value = int(decoded_line)
                    current_time = time.time()
                    
                    print(f"Time: {current_time}, Value: {value}")

                    if value == 0:
                        # If the value is 0, set the flag to False
                        value_flag = False
                    else:
                        # If the value is not 0, set the flag to True
                        value_flag = True
                    
                    # Publish the value
                    msg = Bool()
                    msg.data = value_flag
                    # self.publisher.publish(msg)
                    self.get_logger().debug(f'Published: {value}')
        
        except Exception as e:
            self.get_logger().error(f'Error processing serial data: {str(e)}')


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