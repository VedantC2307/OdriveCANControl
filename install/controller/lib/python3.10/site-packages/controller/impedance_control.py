import rclpy
from rclpy.node import Node
from custom_msgs.msg import MotionState, ImpedanceTorque
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
        
        # 파라미터 선언
        self.declare_parameter('B', 1.0)
        self.declare_parameter('K', 1.0)
        self.declare_parameter('I', 1.0)
        
        # 파라미터 가져오기
        self.B = self.get_parameter('B').value
        self.K = self.get_parameter('K').value
        self.I = self.get_parameter('I').value
        self.get_logger().info(f'Loaded Impedance Params: I={self.I}, B={self.B}, K={self.K}')
        
        # Subscribe to position values (e.g., from a motor encoder)
        self.subscription = self.create_subscription(
            MotionState,
            'motor_state',
            self.motor_state_callback,
            10  # QoS profile
        )
        
        self.publish_rate = 100.0  # Hz
        self.publish_period = 1.0 / self.publish_rate
        self.imp_publisher = self.create_publisher(ImpedanceTorque, 'imp_torque', 10)
        self.timer = self.create_timer(self.publish_period, self.ImpedanceControl)  # 100 Hz processing
        
        # Equilibrium position
        # 상태 변수 초기화
        self.position = 0.0      # 현재 위치
        self.velocity = 0.0      # 현재 속도
        self.position_e = 0.0    # 목표 위치
        self.velocity_e = 0.0    # 목표 속도
        self.error_sum = 0.0     # 적분 오차
        self.acceleration_e = 0.0

    def motor_state_callback(self, msg):
        """Callback to receive position values in radians."""
        self.position = msg.position
        self.velocity = msg.velocity
        #self.get_logger().info(f'Updated Position Buffer: {self.position}')
        #self.get_logger().info(f'Updated counts to radians: {self.velocity}')

    def ImpedanceControl(self):
        """Calculate torque based on impedance control."""
        # Calculate impedance control torque
        imp_torque = self.B * (self.velocity - self.velocity_e) + self.K * (self.position - self.position_e)
        imp_torque_msg = ImpedanceTorque()
        imp_torque_msg.tau_imp = imp_torque  # 토크 값 설정
        self.imp_publisher.publish(imp_torque_msg)  # 메시지 Publish
        #self.get_logger().info(f'Published Torque Command: {imp_torque}')

def main():
    rclpy.init()
    simple_control = ImpedanceControl()
    rclpy.spin(simple_control)
    simple_control.destroy_node()  # 수정: ImpedanceControl.destroy_node() -> simple_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()