# import rclpy
# from rclpy.node import Node
# import numpy as np
# from std_msgs.msg import Int64
# from odrive_can.msg import ControlMessage

# class FrictionCompensationNode(Node):
#     def __init__(self):
#         super().__init__('friction_compensation_node')

#         # Placeholder for subscription to position values (e.g., from a motor encoder)
#         self.subscription = self.create_subscription(
#             Int64,  # Replace with appropriate message type
#             'encoder_position',  # Replace with the actual topic name
#             self.position_callback,
#             10  # QoS profile
#         )

#         # Placeholder for publisher to send torque commands
#         self.publisher = self.create_publisher(
#             ControlMessage,  
#             '/odrive_axis0/control_message',  
#             10  # QoS profile
#         )

#         self.position_data = []  # Buffer to store incoming position data
#         self.timer = self.create_timer(0.05, self.process_data)  # 100 Hz processing

#     def velocity_5_point_backward(self, position):
#         """
#         Calculate velocity using the 5-point backward difference method.
#         """
#         coefficients = np.array([-25, 48, -36, 16, -3]) / 12.0

#         if len(position) < 5:
#             return np.zeros(len(position))

#         velocity = np.zeros_like(position)
#         velocity[4:] = np.convolve(position, coefficients[::-1], mode='valid')

#         self.get_logger().info(f'Calculated Velocity: {velocity[-1]}')

#         return velocity

#     def friction_compensation(self, velocity):
#         """
#         Compute friction compensation torque based on velocity.
#         """
#         return np.where(abs(velocity) > 0.2, 0.38 * np.sign(velocity), 0)

#     def position_callback(self, msg):
#         """Callback to receive position values."""
#         # Placeholder to process incoming position messages
#         # Append new position to buffer (modify as needed for actual data type)
#         self.position_data.append(msg.data)

#         # Keep buffer size manageable
#         if len(self.position_data) > 5:  # Adjust as per requirements
#             self.position_data.pop(0)

#         self.get_logger().info(f'Published position data: {self.position_data}')

#     def process_data(self):
#         """Process the buffered position data and publish torque commands."""
#         if len(self.position_data) < 5:
#             return  # Wait for sufficient data

#         # Convert position data to numpy array
#         position_array = np.array(self.position_data)

#         # Step 1: Compute velocity
#         velocity = self.velocity_5_point_backward(position_array)

#         # Step 2: Compute compensation torque
#         compensation_torque = self.friction_compensation(velocity)

#         # Step 3: Combine with input torque (placeholder for actual input torque logic)
#         input_torque = 0.0  # Example constant input torque
#         total_torque = input_torque + compensation_torque[-1]  # Use the latest value

#         # Step 4: Publish the torque command
#         # torque_msg = Float32()  # Replace with appropriate message type
#         # torque_msg.data = float(total_torque)
#         # self.publisher.publish(torque_msg)

#         # create_msg = ControlMessage()
#         # create_msg.control_mode = 1  # Torque = 1, Velocity = 2 Position = 3
#         # create_msg.input_mode = 1  # Passthrough = 1
#         # create_msg.input_pos = 0.0
#         # create_msg.input_vel = 0.0
#         # create_msg.input_torque = total_torque

#         # self.get_logger().info(f'Publishing: {total_torque}')

#         # self.publisher.publish(create_msg)

#         # self.get_logger().info(f'Published Torque Command: {total_torque}')


# def main(args=None):
#     rclpy.init(args=args)

#     node = FrictionCompensationNode()
#     rclpy.spin(node)

#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Int64
from odrive_can.msg import ControlMessage

class FrictionCompensationNode(Node):
    def __init__(self):
        super().__init__('friction_compensation_node')

        # Subscribe to position values (e.g., from a motor encoder)
        self.subscription = self.create_subscription(
            Int64,  # Message type
            'encoder_position',  # Topic name
            self.position_callback,
            10  # QoS profile
        )

        # Publisher to send torque commands
        self.publisher = self.create_publisher(
            ControlMessage,  
            '/odrive_axis0/control_message',  
            10  # QoS profile
        )

        self.position_data = []  # Buffer to store incoming position data
        self.timer = self.create_timer(0.05, self.process_data)  # 20 Hz processing

    def velocity_5_point_backward(self, position):
        """
        Calculate velocity using the 5-point backward difference method.
        """
        coefficients = np.array([-25, 48, -36, 16, -3]) / 12.0

        if len(position) < 5:
            return 0.0  # Return 0.0 if insufficient data for velocity calculation
        
        # self.get_logger().info(f'Calculated Position: {position}')

        # Compute velocity using the 5-point backward difference
        velocity = np.dot(position[-5:], coefficients)
        self.get_logger().info(f'Calculated Velocity: {velocity}')

        return velocity

    def friction_compensation(self, velocity):
        """
        Compute friction compensation torque based on velocity.
        """
        if abs(velocity) > 0.2:
            return 0.38 * np.sign(velocity)
        return 0.0

    def position_callback(self, msg):
        """Callback to receive position values."""
        self.position_data.append(msg.data)

        # Maintain a fixed buffer size of 5
        if len(self.position_data) > 5:
            self.position_data.pop(0)

        # self.get_logger().info(f'Updated Position Buffer: {self.position_data}')

    def process_data(self):
        """Process the buffered position data and publish torque commands."""
        if len(self.position_data) < 5:
            return  # Wait for sufficient data

        # Step 1: Compute velocity
        velocity = self.velocity_5_point_backward(self.position_data)

        # Step 2: Compute compensation torque
        compensation_torque = self.friction_compensation(velocity)

        # Step 3: Combine with input torque (placeholder for actual input torque logic)
        input_torque = 0.0  # Example constant input torque
        total_torque = input_torque + compensation_torque

        # Step 4: Publish the torque command
        # create_msg = ControlMessage()
        # create_msg.control_mode = 1  # Torque control
        # create_msg.input_mode = 1  # Passthrough
        # create_msg.input_pos = 0.0
        # create_msg.input_vel = 0.0
        # create_msg.input_torque = total_torque

        self.get_logger().info(f'Publishing Torque Command: {total_torque}')
        # self.publisher.publish(create_msg)


def main(args=None):
    rclpy.init(args=args)

    node = FrictionCompensationNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
