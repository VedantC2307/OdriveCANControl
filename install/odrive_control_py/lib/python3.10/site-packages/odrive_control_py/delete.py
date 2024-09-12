import subprocess
import dearpygui.dearpygui as dpg
import os
import signal

# Global variables to store the subprocesses
process1 = None
process2 = None

def execute_command1(sender, app_data, user_data):
    global process1
    command = "ros2 topic echo /odrive_axis0/controller_status"
    process1 = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command], preexec_fn=os.setsid)

def stop_command1(sender, app_data, user_data):
    global process1
    if process1 is not None:
        os.killpg(os.getpgid(process1.pid), signal.SIGINT)
        process1 = None

def execute_command2(sender, app_data, user_data):
    global process2
    command = "ros2 topic echo /odrive_axis1/controller_status"
    process2 = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command], preexec_fn=os.setsid)

def stop_command2(sender, app_data, user_data):
    global process2
    if process2 is not None:
        os.killpg(os.getpgid(process2.pid), signal.SIGINT)
        process2 = None

dpg.create_context()

with dpg.window(label="ROS Command GUI"):
    dpg.add_button(label="Execute ROS Command 1", callback=execute_command1)
    dpg.add_button(label="Stop ROS Command 1", callback=stop_command1)
    dpg.add_button(label="Execute ROS Command 2", callback=execute_command2)
    dpg.add_button(label="Stop ROS Command 2", callback=stop_command2)

dpg.create_viewport(title='ROS Command GUI', width=300, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
