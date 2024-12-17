import rclpy
from rclpy.node import Node
from data_sync.srv import Trigger
import subprocess

class DataCollectionService(Node):

    def __init__(self):
        super().__init__('data_collection_service')
        self.srv = self.create_service(Trigger, 'start_stop_data_collection', self.start_stop_callback)
        self.bag_process = None
        self.get_logger().info("Service is Ready")

    def start_stop_callback(self, request, response):
        self.get_logger().info('New Message received %s' % request.start)
        if request.start:
            self.get_logger().info('Starting data collection...')

            # Start rosbag recording or other data collection here
            if self.bag_process is None:
                topic_name_1 = request.topic_name_1  
                topic_name_2 = request.topic_name_2 
                filename = f'/home/vedant/gaitlab_ws/bag_files/{request.filename}'

                if topic_name_2:
                    self.bag_process = subprocess.Popen(['ros2', 'bag', 'record', topic_name_1, topic_name_2, '-o', filename])
                    self.get_logger().info(f"Recording topics {topic_name_1} and {topic_name_2} to file {filename}...")
                else:
                    self.bag_process = subprocess.Popen(['ros2', 'bag', 'record', topic_name_1, '-o', filename])
                    self.get_logger().info(f"Recording topic {topic_name_1} to file {filename}...")

                response.success = True
            else:
                self.get_logger().info("Data collection already running...")
                response.success = False

        else:
            self.get_logger().info('Stopping data collection...')

            # Stop rosbag recording or other data collection here
            if self.bag_process is not None:
                self.bag_process.send_signal(subprocess.signal.SIGINT)  # Send SIGINT to stop recording
                self.bag_process.wait()
                self.bag_process = None
                self.get_logger().info("Stopping data collection and ROS bag recording...")
                response.success = True
            else:
                self.get_logger().info("Data collection is not active...")
                response.success = False

        return response

def main(args=None):
    rclpy.init()
    node = DataCollectionService()
    rclpy.spin(node)
    if node.bag_process is not None:
        node.bag_process.send_signal(subprocess.signal.SIGINT)
        node.bag_process.wait() 
    DataCollectionService.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
