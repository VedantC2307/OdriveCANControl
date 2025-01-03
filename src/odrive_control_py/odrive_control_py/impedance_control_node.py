import rclpy
from rclpy.node import Node
from odrive_can.msg import ControlMessage, ControllerStatus
from std_msgs.msg import Float32
from sensor_msgs.msg import JointState
from rclpy.qos import QoSProfile

class ImpedanceControl(Node):
    def __init__(self):
        super().__init__('Impedance_Control')
        self.get_logger().info('Starting node')


        # Declare and load impedance parameters
        self.declare_parameters(
            namespace='',
            parameters=[
                ('impedance_params.I', None),
                ('impedance_params.B', None),
                ('impedance_params.K', None),
            ]
        )
        
        self.I = self.get_parameter('impedance_params.I').value
        self.B = self.get_parameter('impedance_params.B').value
        self.K = self.get_parameter('impedance_params.K').value

        self.get_logger().info(f'Loaded Impedance Params: I={self.I}, B={self.B}, K={self.K}')

        # Subscribe to position values (e.g., from a motor encoder)
        self.subscription = self.create_subscription(
            JointState,  # Message type
            'motor_state',  # Topic name
            self.state_callback,  # Callback function
            10  # QoS profile
        )

        self.imp_publisher = self.create_publisher(
            Float32,
            'impedance_torque',
            10
        )

        self.publish_rate = 100.0  # Hz
        self.publish_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(self.publish_period, self.ImpedanceControl)  # 100 Hz processing


        ## Equilibrium position
        self.position_e = 0.0
        self.velocity_e = 0.0
        self.acceleration_e = 0.0

    def state_callback(self, msg):
        """Callback to receive position values and convert to radians."""

        self.position = msg.position
        self.velocity = msg.velocity


    def ImpedanceControl(self):
        """
        Calculate torque based on impedance control.
        """
        # Calculate impedance control torque
        imp_torque = self.B * (self.velocity - self.velocity_e) + self.K * (self.position - self.position_e)
        
        imp_torque_msg = Float32()
        imp_torque_msg.data = imp_torque  # 토크 값 설정
        self.imp_publisher.publish(imp_torque_msg)  # 메시지 Publish
        self.get_logger().info(f'Published Torque Command: {imp_torque}')

def main():
    rclpy.init()
    simple_control = ImpedanceControl()
    rclpy.spin(simple_control)
    ImpedanceControl.destroy_node()
    # ODriveControl.close_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
