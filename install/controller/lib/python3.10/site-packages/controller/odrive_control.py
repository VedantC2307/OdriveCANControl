#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from custom_msgs.srv import ODriveCommand  # 이 부분이 올바르게 수정되었는지 확인
import odrive
from odrive.enums import *
import time

class ODriveController(Node):
    def __init__(self):
        super().__init__('odrive_controller')
        
        # ODrive 객체
        self.drive = None
        
        # 서비스 서버 생성
        self.srv = self.create_service(ODriveCommand, 'odrive/command', self.command_callback)
        self.get_logger().info('ODrive controller service started')
        
    def connect_drive(self):
        """ODrive 연결"""
        if self.drive is None:
            self.get_logger().info('Connecting to ODrive...')
            self.drive = odrive.find_any()
            self.get_logger().info(f'Found ODrive. Serial number: {str(self.drive.serial_number)}')
        return True

    def clear_errors(self):
        """에러 클리어"""
        try:
            self.drive.clear_errors()
            time.sleep(0.5)
            return True, "Errors cleared successfully"
        except Exception as e:
            return False, f"Error clearing errors: {str(e)}"

    def calibrate_encoder(self):
        """엔코더 오프셋 캘리브레이션"""
        try:
            # 먼저 IDLE 상태로
            self.drive.axis0.requested_state = AXIS_STATE_IDLE
            time.sleep(0.5)
            
            # 캘리브레이션 시작
            self.drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
            
            # 캘리브레이션 완료 대기
            start_time = time.time()
            while self.drive.axis0.current_state != AXIS_STATE_IDLE:
                time.sleep(0.1)
                if time.time() - start_time > 10.0:  # 10초 타임아웃
                    return False, "Calibration timeout"
                    
            if self.drive.axis0.encoder.is_ready:
                return True, "Encoder calibration successful"
            else:
                return False, "Encoder not ready after calibration"
                
        except Exception as e:
            return False, f"Calibration error: {str(e)}"

    def set_idle_mode(self):
        """아이들 모드 설정"""
        try:
            self.drive.axis0.requested_state = AXIS_STATE_IDLE
            time.sleep(0.5)
            if self.drive.axis0.current_state == AXIS_STATE_IDLE:
                return True, "Idle mode set successfully"
            else:
                return False, "Failed to set idle mode"
        except Exception as e:
            return False, f"Error setting idle mode: {str(e)}"

    def set_closed_loop_mode(self):
        """클로즈드 루프 모드 설정"""
        try:
            self.drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            time.sleep(0.5)
            if self.drive.axis0.current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
                return True, "Closed loop mode set successfully"
            else:
                return False, "Failed to set closed loop mode"
        except Exception as e:
            return False, f"Error setting closed loop mode: {str(e)}"

    def initialize_sequence(self):
        """전체 초기화 시퀀스"""
        try:
            # 1. Connect
            if not self.connect_drive():
                return False, "Failed to connect to ODrive"
                
            # 2. Clear errors
            success, message = self.clear_errors()
            if not success:
                return False, message
                
            # 3. Calibrate encoder
            success, message = self.calibrate_encoder()
            if not success:
                return False, message
                
            # 4. Set closed loop mode
            success, message = self.set_closed_loop_mode()
            if not success:
                return False, message
                
            return True, "Initialization sequence completed successfully"
            
        except Exception as e:
            return False, f"Initialization error: {str(e)}"

    def command_callback(self, request, response):
        """서비스 콜백 함수"""
        if self.drive is None and request.command != "initialize":
            response.success = False
            response.message = "ODrive not connected. Please initialize first."
            return response

        # 명령어 처리
        if request.command == "initialize":
            response.success, response.message = self.initialize_sequence()
        elif request.command == "clear_error":
            response.success, response.message = self.clear_errors()
        elif request.command == "set_idle":
            response.success, response.message = self.set_idle_mode()
        elif request.command == "set_closed_loop":
            response.success, response.message = self.set_closed_loop_mode()
        else:
            response.success = False
            response.message = f"Unknown command: {request.command}"

        return response

def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = ODriveController()
        rclpy.spin(node)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()