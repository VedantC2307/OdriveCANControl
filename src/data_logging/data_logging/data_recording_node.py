#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from custom_msgs import MotionState, FrictionComp, ImpedanceTorque
from std_msgs.msg import Float32MultiArray, Bool
from std_srvs.srv import SetBool
import h5py
import numpy as np
import time
import os
from datetime import datetime

class DataCollectorNode(Node):
    def __init__(self):
        super().__init__('data_collector_node')
        
        # 파라미터 설정
        self.declare_parameter('save_dir', '/home/user/data')  # 기본값 설정
        self.save_dir = self.get_parameter('save_dir').value

        # 사용자로부터 subject number 입력 받기
        while True:
            try:
                subject_num = input("Enter subject number: ")
                subject_num = int(subject_num)
                if subject_num > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        self.subject_name = f'subject_{subject_num}'
        
        # trial 관련 변수
        self.current_trial = 1
        self.is_recording = False
        self.h5_file = None
        self.data_group = None
        self.start_time = None
        
        # subject 폴더 생성
        self.subject_dir = os.path.join(self.save_dir, self.subject_name)
        if not os.path.exists(self.subject_dir):
            os.makedirs(self.subject_dir)
        
        # logged_items 초기화
        self.logged_items = {
            'elapsed_time': None,
            'position': None,
            'velocity': None,
            'tau_fcomp': None,
            'tau_imp': None,
        }
        
        # 서비스 생성
        self.srv = self.create_service(SetBool, 'toggle_recording', self.toggle_recording_callback)
        
        # 구독자 생성
        self.subscription1 = self.create_subscription(
            MotionState,
            'motor_state',
            self.callback_motor_state,
            10)
            
        self.subscription2 = self.create_subscription(
            FrictionComp,
            'friction_comp_torque',
            self.callback_friction_torque,
            10)
            
        self.subscription3 = self.create_subscription(
            ImpedanceTorque,
            'impedance_torque',
            self.callback_imp_torque,
            10)
        
        # 타이머 설정 (100Hz)
        self.global_rate = 100
        self.timer = self.create_timer(1/self.global_rate, self.timer_callback)
        
        self.get_logger().info('Data collector node has been started')

    def create_new_file(self):
        """새로운 trial 파일 생성"""
        filename = os.path.join(self.subject_dir, f'trial_{self.current_trial}.h5')
        self.h5_file = h5py.File(filename, 'w')
        self.data_group = self.h5_file.create_group("TrialData")
        self.start_time = time.time()
        self.get_logger().info(f'Created new file: {filename}')

    def close_current_file(self):
        """현재 trial 파일 닫기"""
        if self.h5_file is not None:
            self.h5_file.close()
            self.h5_file = None
            self.data_group = None
            self.get_logger().info(f'Closed trial_{self.current_trial}.h5')
            self.current_trial += 1

    def toggle_recording_callback(self, request, response):
        """recording 토글 서비스 콜백"""
        if request.data:  # Start recording
            if not self.is_recording:
                self.create_new_file()
                self.is_recording = True
                response.message = f"Started recording trial_{self.current_trial}"
                response.success = True
            else:
                response.message = "Already recording"
                response.success = False
        else:  # Stop recording
            if self.is_recording:
                self.close_current_file()
                self.is_recording = False
                response.message = "Stopped recording"
                response.success = True
            else:
                response.message = "Not recording"
                response.success = False
        return response

    def callback_motor_state(self, msg):
        if not self.is_recording:
            return
        self.logged_items['position'] = msg.position
        self.logged_items['velocity'] = msg.velocity

    def callback_friction_torque(self, msg):
        if not self.is_recording:
            return
        self.logged_items['tau_fcomp'] = msg.tau_fcomp

    def callback_imp_torque(self, msg):
        if not self.is_recording:
            return
        self.logged_items['tau_imp'] = msg.tau_imp

    def timer_callback(self):
        if not self.is_recording:
            return
            
        # elapsed_time 업데이트
        current_time = time.time() - self.start_time
        self.logged_items['elapsed_time'] = np.array([current_time])
        
        # 데이터 저장
        self.sync_log()

    def sync_log(self):
        if not self.is_recording or self.data_group is None:
            return
            
        for dataset_name, data_to_append in self.logged_items.items():
            if data_to_append is None:
                continue
                
            try:
                if dataset_name in self.data_group:
                    dataset = self.data_group[dataset_name]
                    if isinstance(data_to_append, np.ndarray):
                        dataset.resize((dataset.shape[0] + 1,) + data_to_append.shape)
                        dataset[-1] = data_to_append
                else:
                    if isinstance(data_to_append, np.ndarray):
                        self.data_group.create_dataset(
                            dataset_name,
                            data=[data_to_append],
                            maxshape=((None,) + data_to_append.shape),
                            chunks=True
                        )
            except Exception as e:
                self.get_logger().error(f'Failed to save dataset {dataset_name}: {e}')

    def __del__(self):
        if self.h5_file is not None:
            self.h5_file.close()
            self.get_logger().info('H5 file has been closed')

def main(args=None):
    rclpy.init(args=args)
    data_collector = DataCollectorNode()
    
    try:
        rclpy.spin(data_collector)
    except KeyboardInterrupt:
        pass
    finally:
        if data_collector.h5_file is not None:
            data_collector.close_current_file()
        data_collector.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()