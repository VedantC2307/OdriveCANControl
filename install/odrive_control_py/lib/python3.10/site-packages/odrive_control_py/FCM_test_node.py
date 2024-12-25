import numpy as np

def velocity_5_point_backward(position):
    """
    Calculate velocity using the 5-point backward difference method.
    Coefficients are based on the Simulink model.
    """
    # Coefficients from the Simulink model
    coefficients = np.array([-25, 48, -36, 16, -3]) / 12.0

    # Ensure position has enough points (padding if necessary)
    if len(position) < 5:
        raise ValueError("Position array must have at least 5 points for 5-point backward difference.")

    velocity = np.zeros_like(position)
    
    # Compute velocity for indices starting from 4
    for i in range(4, len(position)):
        velocity[i] = np.dot(coefficients, position[i-4:i+1])

    return velocity

def friction_compensation(velocity):
    """
    Compute friction compensation torque based on velocity.
    Implements the MATLAB function logic.
    """
    i_torque = np.zeros_like(velocity)

    for i, vel in enumerate(velocity):
        if abs(vel) > 0.2:
            i_torque[i] = 0.38 * np.sign(vel)
        else:
            i_torque[i] = 0

    return i_torque

def main():
    """Main simulation function."""
    # Simulated position data (example, replace with real data)
    time = np.linspace(0, 10, 1000)  # Time from 0 to 10 seconds
    position = np.sin(time)  # Example position (sinusoidal motion)

    # Step 1: Compute velocity
    velocity = velocity_5_point_backward(position)

    # Step 2: Friction compensation
    compensation_torque = friction_compensation(velocity)

    # Step 3: Input torque (example constant input torque)
    input_torque = 1.0  # Replace with real input torque values if available

    # Step 4: Combine input torque and compensation torque
    total_torque = input_torque + compensation_torque

    # Simulate CAN transmission (convert to bytes)
    can_data = (total_torque * 100).astype(np.uint8)  # Example scaling and packing

    # Output results
    print("Velocity:", velocity)
    print("Friction Compensation Torque:", compensation_torque)
    print("Total Torque:", total_torque)
    print("CAN Data:", can_data)

if __name__ == "__main__":
    main()
