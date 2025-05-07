import odrive
from odrive.enums import *
import time

# Find the ODrive connected via USB
print("Finding an ODrive...")
odrv0 = odrive.find_any()

print(odrv0)
time.sleep(1)
# Clear any existing errors
odrv0.clear_errors()
time.sleep(1)
# Ensure the motor is calibrated and ready
if odrv0.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
    print("Motor is not in closed loop control. Calibrating...")
    time.sleep(1)
    odrv0.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
    while odrv0.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(1)
    print("Calibration complete. Entering closed loop control.")
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

time.sleep(1)
# Set the control mode to velocity control
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

# Set the desired velocity (in turns per second)
target_velocity = 0.2
odrv0.axis0.controller.input_vel = target_velocity

print(f"Motor velocity set to {target_velocity} turns per second.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nCtrl+C detected! Stopping the motor...")
    odrv0.axis0.controller.input_vel = 0.0  # Set velocity to 0
    print("Motor velocity set to 0. Exiting...")
