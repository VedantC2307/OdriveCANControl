#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from custom_msgs.srv import ODriveCommand
from custom_msgs.msg import FrictionComp, ImpedanceTorque
import odrive
from odrive.enums import *
import time
import socket
from std_msgs.msg import Bool

class ODriveController(Node):
    def __init__(self):
        super().__init__('odrive_controller')
        
        # ODrive 객체
        self.drive = None
        self.current_control_mode = None

        # initialize torque values
        self.fcomp_tau = 0.0
        self.imp_tau = 0.0
        self.hold_torque = 0.0

        # 토크 명령 타이머 생성 (100Hz)
        self.publish_rate = 100.0  # Hz
        self.publish_period = 1.0 / self.publish_rate
        self.create_timer(self.publish_period, self.torque_command_callback)

        # 서비스 서버 생성
        self.srv = self.create_service(ODriveCommand, 'odrive/command', self.command_callback)
        self.get_logger().info('ODrive controller service started')

        # Publisher for encoder offset
        self.encoder_offset_publisher_ = self.create_publisher(Bool, 'encoder_offset_flag', 2)
        
        # Publisher for data recording
        self.recording_publisher_ = self.create_publisher(Bool, 'recording_flag', 2)
        self.get_logger().info('Created publisher for recording_flag to control data recording')

        # friction torque subscriber
        self.command_sub = self.create_subscription(
            FrictionComp,
            'friction_torque',
            self.friction_torque_callback,
            10
        )

        # imp torque subscriber
        self.command_sub2 = self.create_subscription(
            ImpedanceTorque,
            'imp_torque',
            self.imp_torque_callback,
            10
        )

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
        self.start_controller = False

    def friction_torque_callback(self, msg):
        self.get_logger().debug(f"Received friction torque: {msg.tau_fcomp}")
        self.fcomp_tau = msg.tau_fcomp
        #self.get_logger().info(f'Friction Comp Tau: {self.fcomp_tau}')

    def imp_torque_callback(self, msg):
        self.get_logger().debug(f"Received impedance torque: {msg.tau_imp}")
        self.imp_tau = -msg.tau_imp
        #self.get_logger().info(f'Impedance Tau: {self.imp_tau}')

    def encoder_offset_zero_callback(self):
        """Function to offset the encoder by publishing to the encoder topic"""
        self.get_logger().info("Attempting to zero encoder offset...")
        try:
            msg = Bool()
            msg.data = True  # Signal to offset the encoder value
            self.encoder_offset_publisher_.publish(msg)
            self.get_logger().info("Sent encoder offset command.")
            return True, "Encoder offset zeroed"
        except Exception as e:
            self.get_logger().error(f"Error zeroing encoder offset: {str(e)}")
            return False, f"Error zeroing encoder offset: {str(e)}"

    def connect_drive(self):
        """ODrive 연결"""
        if self.drive is None:
            self.get_logger().info('Connecting to ODrive...')
            self.drive = odrive.find_any()
            self.get_logger().info(f'Found ODrive. Serial number: {str(self.drive.serial_number)}')
        else:
            self.get_logger().debug('ODrive already connected.')
        return True

    def clear_errors(self):
        """에러 클리어"""
        self.get_logger().info("Clearing ODrive errors...")
        try:
            self.drive.clear_errors()
            time.sleep(0.5)
            self.get_logger().info("Errors cleared successfully.")
            return True, "Errors cleared successfully"
        except Exception as e:
            self.get_logger().error(f"Error clearing errors: {str(e)}")
            return False, f"Error clearing errors: {str(e)}"

    def calibrate_encoder(self):
        """엔코더 오프셋 캘리브레이션"""
        self.get_logger().info("Starting encoder calibration...")
        try:
            # 먼저 IDLE 상태로
            self.drive.axis0.requested_state = AXIS_STATE_IDLE
            time.sleep(0.5)
            
            # 캘리브레이션 시작
            self.drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
            self.get_logger().debug("Encoder calibration sequence started.")
            
            # 캘리브레이션 완료 대기
            start_time = time.time()
            while self.drive.axis0.current_state != AXIS_STATE_IDLE:
                time.sleep(0.2)
                if time.time() - start_time > 20.0:  # 20초 타임아웃
                    self.get_logger().error("Encoder calibration timeout.")
                    return False, "Calibration timeout"
            
            # Check if calibration was successful - use config.pre_calibrated instead of encoder.is_ready
            time.sleep(0.5)  # Give ODrive a moment to update status
            
            # The right way to check if encoder is calibrated is different in newer ODrive firmware
            if hasattr(self.drive.axis0, 'encoder') and hasattr(self.drive.axis0.encoder, 'is_ready'):
                encoder_ready = self.drive.axis0.encoder.is_ready
            elif hasattr(self.drive.axis0, 'config') and hasattr(self.drive.axis0.config, 'pre_calibrated'):
                encoder_ready = self.drive.axis0.config.pre_calibrated
            else:
                # If we can't check, we'll just assume it worked as the state transitioned back to IDLE
                encoder_ready = True
                self.get_logger().warning("Could not verify encoder calibration status. Assuming successful.")
            
            if encoder_ready:
                self.get_logger().info("Encoder calibration successful.")
                return True, "Encoder calibration successful"
            else:
                self.get_logger().error("Encoder not ready after calibration.")
                return False, "Encoder not ready after calibration"
                
        except Exception as e:
            self.get_logger().error(f"Calibration error: {str(e)}")
            return False, f"Calibration error: {str(e)}"

    def calibrate_motor(self):
        """Full calibration sequence for the motor"""
        self.get_logger().info("Starting motor calibration...")
        try:
            # First set to IDLE state
            self.drive.axis0.requested_state = AXIS_STATE_IDLE
            time.sleep(0.5)
            
            # Start motor calibration
            self.drive.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
            self.get_logger().debug("Motor calibration sequence started.")
            
            # Wait for calibration to complete
            start_time = time.time()
            while self.drive.axis0.current_state != AXIS_STATE_IDLE:
                time.sleep(0.2)
                if time.time() - start_time > 10.0:  # 10 second timeout
                    self.get_logger().error("Motor calibration timeout.")
                    return False, "Motor calibration timeout"
                    
            if self.drive.axis0.motor.is_calibrated:
                self.get_logger().info("Motor calibration successful.")
                return True, "Motor calibration successful"
            else:
                self.get_logger().error("Motor not calibrated after calibration sequence.")
                return False, "Motor not calibrated after calibration sequence"
                
        except Exception as e:
            self.get_logger().error(f"Motor calibration error: {str(e)}")
            return False, f"Motor calibration error: {str(e)}"

    def set_idle_mode(self):
        """아이들 모드 설정 - 토크 모드 해제"""
        self.get_logger().info("Setting idle mode...")
        try:
            self.drive.axis0.requested_state = AXIS_STATE_IDLE
            time.sleep(0.5)
            if self.drive.axis0.current_state == AXIS_STATE_IDLE:
                # 토크 모드 해제
                self.current_control_mode = None
                self.get_logger().info("Idle mode set and torque control disabled.")
                return True, "Idle mode set and torque control disabled"
            else:
                self.get_logger().error("Failed to set idle mode.")
                return False, "Failed to set idle mode"
        except Exception as e:
            self.get_logger().error(f"Error setting idle mode: {str(e)}")
            return False, f"Error setting idle mode: {str(e)}"

    def set_closed_loop_mode(self):
        """클로즈드 루프 모드 설정"""
        self.get_logger().info('Setting closed loop mode')
        try:
            self.drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
            self.get_logger().info('Closed loop mode set.')
            # time.sleep(0.5)
            # if self.drive.axis0.current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
            #     return True, "Closed loop mode set successfully"
            # else:
            #     return False, "Failed to set closed loop mode"
        except Exception as e:
            self.get_logger().error(f"Error setting closed loop mode: {str(e)}")
            return False, f"Error setting closed loop mode: {str(e)}"

    def torque_command_callback(self):
        """합산된 토크 명령을 모터에 전송"""
        # 드라이브가 없거나 토크 모드가 아니거나 Closed Loop가 아닌 경우 리턴
        if (self.drive is None or 
            self.current_control_mode != "torque" or 
            self.drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL):
            self.get_logger().debug("Torque command skipped: not in correct mode or drive not connected.")
            return
        
        if not self.start_controller:
            self.get_logger().debug("Torque command skipped: controller not started.")
            return
            
        try:
            # 토크 합산 및 명령 전송
            fcomp = self.fcomp_tau if self.fcomp_tau is not None else 0.0
            imp = self.imp_tau if self.imp_tau is not None else 0.0

            total_torque = fcomp + imp + self.hold_torque

            # Print total torque
            self.get_logger().info(f'Total torque: {total_torque} Nm')

            self.drive.axis0.controller.input_torque = total_torque
            self.get_logger().debug(f'Applied total torque: {total_torque} (fcomp: {self.fcomp_tau}, imp: {self.imp_tau})')
        except Exception as e:
            self.get_logger().error(f'Error applying torque command: {str(e)}')

    def set_torque_control(self):
        """토크 제어 모드 설정 - Closed Loop 상태에서만 가능"""
        self.get_logger().info("Setting torque control mode...")
        try:
            # Closed Loop 상태 확인
            if self.drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
                self.get_logger().error("Torque control can only be set in Closed Loop mode.")
                return False, "Torque control can only be set in Closed Loop mode"
                
            self.drive.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
            self.current_control_mode = "torque"
            self.get_logger().info("Successfully set torque control mode!")
            time.sleep(0.5)
            return True, "Torque control mode set successfully"
        except Exception as e:
            self.get_logger().error(f"Error setting torque control mode: {str(e)}")
            return False, f"Error setting torque control mode: {str(e)}"

    def initialize_sequence(self):
        """전체 초기화 시퀀스"""
        self.get_logger().info("Starting initialization sequence...")
        try:
            # 1. Connect
            if not self.connect_drive():
                self.get_logger().error("Failed to connect to ODrive.")
                return False, "Failed to connect to ODrive"
                
            # 2. Clear errors
            success, message = self.clear_errors()
            if not success:
                self.get_logger().error(f"Clear errors failed: {message}")
                return False, message
                
            # 3. Calibrate encoder
            success, message = self.calibrate_encoder()
            if not success:
                self.get_logger().error(f"Encoder calibration failed: {message}")
                return False, message
            
            # 4. Set closed loop mode
            self.get_logger().info("Setting closed loop mode after calibration...")
            try:
                self.drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                time.sleep(0.5)
                
                if self.drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
                    self.get_logger().error("Failed to set closed loop mode after calibration.")
                    return False, "Failed to set closed loop mode after calibration"
                
                # 5. Set torque control mode
                self.get_logger().info("Setting torque control mode after closed loop...")
                success, message = self.set_torque_control()
                if not success:
                    self.get_logger().error(f"Failed to set torque control mode: {message}")
                    return False, message
                
            except Exception as e:
                self.get_logger().error(f"Error setting modes after calibration: {str(e)}")
                return False, f"Error setting modes after calibration: {str(e)}"
                
            self.get_logger().info("Initialization sequence completed successfully with torque control enabled.")
            return True, "Initialization sequence completed successfully with torque control enabled"
            
        except Exception as e:
            self.get_logger().error(f"Initialization error: {str(e)}")
            return False, f"Initialization error: {str(e)}"

    def start_recording(self):
        """Start data recording by publishing to the recording_flag topic"""
        self.get_logger().info("Starting data recording...")
        try:
            msg = Bool()
            msg.data = True  # Signal to start recording
            self.recording_publisher_.publish(msg)
            self.get_logger().info("Started data recording")
            return True, "Data recording started"
        except Exception as e:
            self.get_logger().error(f"Error starting data recording: {str(e)}")
            return False, f"Error starting data recording: {str(e)}"

    def start_recording_with_subject(self, subject_name):
        """Start data recording with a specific subject name"""
        self.get_logger().info(f"Starting data recording for subject {subject_name}...")
        try:
            # Create a message to start recording
            msg = Bool()
            msg.data = True  # Signal to start recording
            
            # Publish the message to trigger recording
            self.recording_publisher_.publish(msg)
            
            # Log the action
            self.get_logger().info(f"Started data recording for subject {subject_name}")
            
            # In a production system, you would also set the subject name parameter
            # via ROS parameter service, but for simplicity we're just publishing the flag
            
            return True, f"Data recording started for subject {subject_name}"
        except Exception as e:
            self.get_logger().error(f"Error starting data recording: {str(e)}")
            return False, f"Error starting data recording: {str(e)}"

    def stop_recording(self):
        """Stop data recording by publishing to the recording_flag topic"""
        self.get_logger().info("Stopping data recording...")
        try:
            msg = Bool()
            msg.data = False  # Signal to stop recording
            self.recording_publisher_.publish(msg)
            self.get_logger().info("Stopped data recording")
            return True, "Data recording stopped"
        except Exception as e:
            self.get_logger().error(f"Error stopping data recording: {str(e)}")
            return False, f"Error stopping data recording: {str(e)}"

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
                message = data.decode('utf-8').strip()
                self.get_logger().info(f'Received message: {message}')
                
                # Handle recording commands with subject name
                if message.startswith("start_recording"):
                    # Parse subject name if included
                    parts = message.split(',')
                    if len(parts) > 1 and parts[1].strip():
                        subject_name = parts[1].strip()
                        self.get_logger().info(f"Starting recording for subject {subject_name}")
                        # Set parameter for data_recording node with subject name
                        success, response = self.start_recording_with_subject(subject_name)
                    else:
                        success, response = self.start_recording()
                elif message.startswith("stop_recording"):
                    # Parse subject name if included
                    parts = message.split(',')
                    if len(parts) > 1 and parts[1].strip():
                        subject_name = parts[1].strip()
                        self.get_logger().info(f"Stopping recording for subject {subject_name}")
                    success, response = self.stop_recording()
                elif message == "initialize":
                    self.get_logger().info("Received initialize command from client.")
                    success, response = self.initialize_sequence()
                elif message == "encoder_offset_calibration":
                    self.get_logger().info("Received encoder_offset_calibration command from client.")
                    success, response = self.calibrate_encoder()
                elif message == "motor_calibration":
                    self.get_logger().info("Received motor_calibration command from client.")
                    success, response = self.calibrate_motor()
                elif message == "clear_error":
                    self.get_logger().info("Received clear_error command from client.")
                    success, response = self.clear_errors()
                elif message == "set_idle":
                    self.get_logger().info("Received idle command from client.")
                    success, response = self.set_idle_mode()
                elif message == "set_closed_loop":
                    self.get_logger().info("Received closed_loop command from client.")
                    success, response = self.set_closed_loop_mode()
                elif message == "set_torque_mode":
                    self.get_logger().info("Received set_torque_mode command from client.")
                    success, response = self.set_torque_control()
                elif message == "start_controller":
                    self.get_logger().info("Received start_controller command from client.")
                    self.start_controller = True
                    
                    # Check if we're in the right state for controller to work
                    if self.drive is None:
                        success, response = False, "ODrive not connected"
                    elif self.drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
                        # Try to set closed loop mode automatically
                        self.get_logger().info("Controller start requested but not in CLOSED_LOOP mode. Setting now...")
                        try:
                            self.drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                            time.sleep(0.5)
                            
                            if self.drive.axis0.current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
                                # Now set torque control mode
                                self.drive.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
                                self.current_control_mode = "torque"
                                success, response = True, "Controller started and set to torque control mode"
                            else:
                                success, response = False, "Failed to set closed loop mode for controller"
                        except Exception as e:
                            success, response = False, f"Error setting control mode: {str(e)}"
                    elif self.current_control_mode != "torque":
                        # Set torque control mode
                        try:
                            self.drive.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
                            self.current_control_mode = "torque"
                            success, response = True, "Controller started and set to torque control mode"
                        except Exception as e:
                            success, response = False, f"Error setting torque control mode: {str(e)}"
                    else:
                        # Already in correct mode
                        success, response = True, "Controller started"
                    
                    # Log details about the motor state
                    try:
                        if self.drive:
                            state = self.drive.axis0.current_state
                            mode = self.drive.axis0.controller.config.control_mode
                            self.get_logger().info(f"Motor state: {state}, Control mode: {mode}, start_controller: {self.start_controller}")
                    except Exception as e:
                        self.get_logger().error(f"Error checking motor state: {str(e)}")
                elif message == "encoder_offset":
                    self.get_logger().info("Received encoder_offset command from client.")
                    success, response = self.encoder_offset_zero_callback()
                else:
                    self.get_logger().warning(f"Unknown command received: {message}")
                    success = False
                    response = f"Unknown command: {message}"
                
                # Send response back to client
                if self.client_socket:
                    self.client_socket.send(f'{success}: {response}\n'.encode('utf-8'))
            else:
                # Client disconnected
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

    def command_callback(self, request, response):
        """서비스 콜백 함수"""
        self.get_logger().info(f"Received service command: {request.command}")
        if self.drive is None and request.command != "initialize":
            response.success = False
            response.message = "ODrive not connected. Please initialize first."
            self.get_logger().error(response.message)
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
        elif request.command == "set_torque_mode":
            response.success, response.message = self.set_torque_control()
        else:
            response.success = False
            response.message = f"Unknown command: {request.command}"
            self.get_logger().warning(response.message)

        self.get_logger().info(f"Service response: {response.success}, {response.message}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ODriveController()
    
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            node.check_socket()
    except KeyboardInterrupt:
        node.get_logger().info("Shutdown requested by user.")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()