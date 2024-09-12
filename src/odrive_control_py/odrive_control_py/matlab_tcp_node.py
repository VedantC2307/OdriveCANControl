import socket
import rclpy
from rclpy.node import Node
from data_sync.srv import Trigger  # Import the Trigger service type
import threading

class TCPROS2Bridge(Node):
    def __init__(self):
        super().__init__('tcp_ros2_bridge')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 12345
        self.server_socket.bind(('192.168.0.55', self.port))  # Adjust the host and port as needed
        self.server_socket.listen(1)
        self.bag_process = None
        self.get_logger().info(f'TCP Server listening on port {self.port}')
        
        # Create a service client to call the rosbag service
        self.cli = self.create_client(Trigger, 'start_stop_data_collection')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        # Start connection handling in a new thread
        self.connection_thread = threading.Thread(target=self.handle_connections, daemon=True)
        self.connection_thread.start()

    def handle_connections(self):
        while rclpy.ok():
            client_socket, addr = self.server_socket.accept()
            self.get_logger().info(f'Connected by {addr}')
            while True:
                data = client_socket.recv(256).decode('utf-8')
                if not data:
                    break
                self.handle_command(data)
            client_socket.close()

    def handle_command(self, command):
        parts = command.split(',')
        action = parts[0].strip()
        
        if action == "ROSBAG":
            trigger = parts[1].strip() if len(parts) > 1 else ""
            topic_name_1 = parts[2].strip() if len(parts) > 2 else ""
            topic_name_2 = parts[3].strip() if len(parts) == 5 else ""
            
            if len(parts) == 5:
                filename = parts[4].strip() 
            elif len(parts) == 4: 
                filename = parts[3].strip() 
            else:
                filename = ""
            
            self.rosbag_recording(trigger, topic_name_1, topic_name_2, filename)

        elif action == "MODE":
            control_mode = parts[1].strip()
            value = parts[2].strip()
            self.control_mode(control_mode, value)

        elif action == "STATE":
            state = parts[1].strip()
            self.motor_state(state)

        elif action == "CONTROLLER":
            controller = parts[1].strip()
            self.odrive_controller(controller)

        else:
            self.get_logger().warn(f'Unknown command: {command}')


    def rosbag_recording(self, trigger, topic_name_1, topic_name_2, filename):
        request = Trigger.Request()
        request.start = (trigger == 'True')
        request.topic_name_1 = topic_name_1
        request.topic_name_2 = topic_name_2
        request.filename = filename

        if request.start:
            if topic_name_2 != '':
                self.get_logger().info(f'Starting rosbag on topics {topic_name_1} and {topic_name_2} to file {filename}')
                # Call the service to start recording with 2 topics
            else:
                self.get_logger().info(f'Starting rosbag on topic {topic_name_1} to file {filename}')
            # Call the service to start recording with one topic
        else:
            self.get_logger().info('Stopping rosbag.')
            # Call the service to stop the recording

        self.future = self.cli.call_async(request)

    def control_mode(self, control_mode, value):
        if control_mode in ['Position', 'Velocity', 'Torque']:
            self.get_logger().info(f'Sending {control_mode} command {value}')
        else:
            self.get_logger().warn(f'Unknown control_mode: {control_mode}')

    def motor_state(self, state):
        if state == 'CLOSED':
            self.get_logger().info(f'Putting motor in {state} Loop')
        elif state == 'IDLE':
            self.get_logger().info(f'Putting motor in {state}')
        else:
            self.get_logger().warn(f'Unknown motor state: {state}')

    def odrive_controller(self, controller):
        if controller == 'True':
            self.get_logger().info("Starting Controller")
        else:
            self.get_logger().info("Stopping Controller")

    def destroy_node(self):
        # Close the server socket when the node is shutting down
        self.server_socket.close()
        self.get_logger().info('Server socket closed.')

        # Ensure the thread finishes before destroying the node
        if self.connection_thread.is_alive():
            self.connection_thread.join()

        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = TCPROS2Bridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
