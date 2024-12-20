```bash
git clone https://github.com/VedantC2307/OdriveCANControl.git
rm -rf build/ log/ install/
cd src/
rm -rf ros_odrive
git clone https://github.com/odriverobotics/ros_odrive.git
colcon build --packages-select odrive_can odrive_control_py
colcon build --packages-select odrive_can odrive_control_py
source ./install/setup.bash
```