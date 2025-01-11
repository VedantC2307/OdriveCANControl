#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import socket
from odrive_can.srv import AxisState
# from ros_odrive.odrive_node.srv import AxisState


class MotorControlServer(Node):
    def __init__(self):
        super().__init__('motor_control_server')
        
        # Create service client
        self.axis_state_client = self.create_client(AxisState, '/odrive_axis0/request_axis_state')
        
        # TCP Server setup
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = '0.0.0.0'  # Listen on all available interfaces
        self.port = 1234
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.server_socket.setblocking(False)  # Make socket non-blocking
        
        self.get_logger().info(f'Server listening on {self.host}:{self.port}')
        
        # Client socket
        self.client_socket = None
        self.client_address = None
        
        # Motor states
        self.IDLE_STATE = 1
        self.CLOSED_LOOP_STATE = 8
        self.ENCODER_OFFSET_CALIBRATION = 7
        
        # Create timer for checking connections and messages
        self.create_timer(0.1, self.check_socket)  # 10Hz timer
    
    def check_socket(self):
        # Check for new connections if no client is connected
        if self.client_socket is None:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                self.client_socket.setblocking(False)
                self.get_logger().info(f'Connected to client at {self.client_address}')
            except BlockingIOError:
                # No connection available
                return
            except Exception as e:
                self.get_logger().error(f'Error accepting connection: {str(e)}')
                return
        
        # Check for messages from connected client
        try:
            data = self.client_socket.recv(1024)
            if data:
                message = data.decode('utf-8')
                self.get_logger().info(f'Received message: {message}')
                
                # Check if it's a motor state command
                ## IDLE = 1
                ## FULL_CALIBRATION_SEQUENCE = 3 (MOTOR_CALIBRATION then ENCODER_OFFSET_CALIBRATION)
                ## MOTOR_CALIBRATION = 4
                ## ENCODER_OFFSET_CALIBRATION = 7
                ## CLOSED_LOOP = 8
                
                if "CLOSED LOOP" in message:
                    self.set_motor_state(self.CLOSED_LOOP_STATE)
                elif "IDLE" in message:
                    self.set_motor_state(self.IDLE_STATE)
                elif "ENCODER_OFFSET_CALIBRATION" in message:
                    self.set_motor_state(self.ENCODER_OFFSET_CALIBRATION)
            else:
                # Connection closed by client
                self.get_logger().info('Client disconnected')
                self.client_socket.close()
                self.client_socket = None
                self.client_address = None
                
        except BlockingIOError:
            # No data available
            pass
        except Exception as e:
            self.get_logger().error(f'Error handling client: {str(e)}')
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
                self.client_address = None
    
    def set_motor_state(self, state):
        # Wait for service to be available
        while not self.axis_state_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Service not available, waiting...')
        
        # Create request
        request = AxisState.Request()
        request.axis_requested_state = state
        
        # Call service
        try:
            future = self.axis_state_client.call_async(request)
            rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
            if future.result() is not None:
                self.get_logger().info(f'Successfully set motor state to {state}')
            else:
                self.get_logger().error('Failed to set motor state')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    server = MotorControlServer()
    
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        if server.client_socket:
            server.client_socket.close()
        server.server_socket.close()
        server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()