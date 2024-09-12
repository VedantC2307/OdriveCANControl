import dearpygui.dearpygui as dpg
import subprocess

dpg.create_context()

def toggle_idle_closed_loop(sender):
    current_text = dpg.get_item_label(sender)
    if current_text == "IDLE | CLOSED LOOP":
        new_text = "CLOSED LOOP"
        message = "Switched to CLOSED LOOP"
        subprocess.run(['ros2', 'topic', 'pub', '/command_topic', 'std_msgs/String', '"CLOSED LOOP"'])
    else:
        new_text = "IDLE | CLOSED LOOP"
        message = "Switched to IDLE"
        subprocess.run(['ros2', 'topic', 'pub', '/command_topic', 'std_msgs/String', '"IDLE"'])
    
    dpg.set_item_label(sender, new_text)
    dpg.set_value("control_state_log", message)

def set_torque_mode(sender):
    result = subprocess.run(['ros2', 'topic', 'echo', '/odrive_axis0/controller_status'], capture_output=True, text=True)
    dpg.set_value("torque_mode_log", result.stdout if result.returncode == 0 else result.stderr)

def start_plotjuggler(sender):
    result = subprocess.run(['plotjuggler'], capture_output=True, text=True)
    dpg.set_value("plotjuggler_log", result.stdout if result.returncode == 0 else result.stderr)

def start_control_node(sender):
    result = subprocess.run(['ros2', 'run', 'your_package', 'your_control_node'], capture_output=True, text=True)
    dpg.set_value("control_node_log", result.stdout if result.returncode == 0 else result.stderr)

def start_ros2_bags(sender):
    result = subprocess.run(['ros2', 'bag', 'record', '-a'], capture_output=True, text=True)
    dpg.set_value("ros2_bags_log", result.stdout if result.returncode == 0 else result.stderr)

def stop_ros2_bags(sender):
    result = subprocess.run(['ros2', 'bag', 'stop'], capture_output=True, text=True)
    dpg.set_value("ros2_bags_log", result.stdout if result.returncode == 0 else result.stderr)

with dpg.theme() as theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 150))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 70, 170))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 90, 190))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

with dpg.window(label="ROS2 Control Panel", width=800, height=600):
    dpg.add_text("Control mode")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Set Torque mode", callback=set_torque_mode)
        dpg.add_input_text(multiline=True, width=300, height=50, readonly=True, tag="torque_mode_log")

    dpg.add_text("Control State")
    with dpg.group(horizontal=True):
        dpg.add_button(label="IDLE | CLOSED LOOP", callback=toggle_idle_closed_loop)
        dpg.add_input_text(multiline=True, width=300, height=50, readonly=True, tag="control_state_log")

    dpg.add_text("PlotJuggler")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Start Graph", callback=start_plotjuggler)
        dpg.add_input_text(multiline=True, width=300, height=50, readonly=True, tag="plotjuggler_log")

    dpg.add_text("Control node")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Start controller", callback=start_control_node)
        dpg.add_input_text(multiline=True, width=300, height=50, readonly=True, tag="control_node_log")

    dpg.add_text("Datalogging")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Start", callback=start_ros2_bags)
        dpg.add_button(label="Stop", callback=stop_ros2_bags)
        dpg.add_input_text(multiline=True, width=300, height=50, readonly=True, tag="ros2_bags_log")

dpg.bind_theme(theme)

dpg.create_viewport(title='ROS2 Control Panel', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
