# ODrive CAN Control

A ROS 2 workspace for controlling ODrive motor controllers with impedance control and data logging via serial communication.

## Quick Start

1. **Launch the system**:
   ```bash
   source ./install/setup.bash
   ros2 launch robot_launch robot.launch.py
   ```

2. **Start the GUI**:
   ```bash
   python3 src/controller/src/controller/App.py
   ```

## System Components

### Main Nodes
- **ODrive Controller** (`odrive_controller`): Interfaces with ODrive hardware via serial communication
- **Impedance Control** (`Impedance_Control`): Implements compliant motion control with configurable stiffness (K), damping (B), and inertia (I) parameters
- **Friction Compensation** (`friction_compensation_node`): Uses velocity-based friction model for smoother motion
- **Data Logging** (`data_logging`): Records sensor data and controller signals to HDF5 files

## Using the GUI

1. **Connect to ODrive**:
   - Enter IP and Port (default: `172.26.33.8:1234`)
   - Click "Connect"

2. **Initialize the system**:
   - Click "Initialize ODrive Setup"
   - Click "Motor Calibration" (if needed)
   - Click "Encoder Offset Calibration" (if needed)
   - Set Motor State to "CLOSED LOOP"
   - Click "Start Controller"

3. **Record data**:
   - Enter Subject Name
   - Click "Start Recording" (click again to stop)

## Control Methods


## Data Recording

The system records data to HDF5 files with chunked storage for efficient I/O. Data is buffered and written in batches for optimal performance.

To start/stop recording:
- Use GUI's "Start Recording" button with a subject name
- Or publish to the recording_flag topic: `ros2 topic pub /recording_flag std_msgs/msg/Bool "data: true"`

## Troubleshooting

- **ODrive Connection Issues**: Click "Clear errors" and reinitialize
- **Calibration Problems**: Ensure motor can move freely during calibration
- **Data Recording Errors**: Check write permissions for data directory
- **Node Shutdown Issues**: Use Ctrl+C once and wait for clean shutdown