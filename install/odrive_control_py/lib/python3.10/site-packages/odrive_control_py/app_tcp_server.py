import socket
import threading
import os
import subprocess

# Define server address and port
SERVER_IP = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 1234

# Define functions for system-level commands
def start_recording(topic_name, file_name, topic_name_1=None):
    print(f"Starting recording for topic {topic_name}", end="")
    if topic_name_1:
        print(f" and topic {topic_name_1}", end="")
    print(f", saving to file {file_name}")
    # Implement actual recording logic here

    
    # Example (placeholder): Log topics to file
    with open(file_name, 'a') as f:
        f.write(f"Recording topics: {topic_name}")
        if topic_name_1:
            f.write(f", {topic_name_1}")


def stop_recording(file_name):
    print(f"Stopping recording, saving to file {file_name}")
    # Example system-level command to stop recording
    # Replace with actual stop recording command, e.g., stop a rosbag recording
    subprocess.run(["echo", "Recording stopped"], stdout=open(file_name, "a"))  # Simulate stop

def set_motor_state(state):
    print(f"Setting motor state to {state}")
    # Example system-level command based on motor state
    if state == "CLOSED LOOP":
        # Replace with actual command to enable motor control
        subprocess.run(["echo", "Motor in closed loop mode"])
    elif state == "IDLE":
        # Replace with actual command to disable motor control
        subprocess.run(["echo", "Motor set to idle"])

def set_control_mode(mode, value):
    print(f"Setting control mode to {mode} with value {value}")
    # Placeholder for control mode action, replace with actual system commands
    if mode == "Position":
        # Command to set position
        subprocess.run(["echo", f"Setting position to {value}"])
    elif mode == "Velocity":
        # Command to set velocity
        subprocess.run(["echo", f"Setting velocity to {value}"])
    elif mode == "Torque":
        # Command to set torque
        subprocess.run(["echo", f"Setting torque to {value}"])

# Function to handle each client connection
def handle_client(client_socket, client_address):
    print(f"Client connected from {client_address}")
    
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Client {client_address} disconnected.")
                break

            # Process received message
            if "Position" in data or "Velocity" in data or "Torque" in data:
                # Parse control mode and value
                mode, value = data.split(':')
                set_control_mode(mode, value)

            elif "True" in data or "False" in data:
                # Parse recording state, topics, and file name
                parts = data.split(',')
                recording_state = parts[0]
                topic_name = parts[1]
                file_name = parts[-1]  # The file name is always the last part of the message

                # Check if there is an additional topic_name_1
                if len(parts) == 4:
                    topic_name_1 = parts[2]
                    if recording_state == "True":
                        start_recording(topic_name, file_name, topic_name_1)  # Pass both topics to the start_recording function
                    else:
                        stop_recording(file_name)
                else:
                    # Only one topic
                    if recording_state == "True":
                        start_recording(topic_name, file_name)  # Only pass topic_name if there's no topic_name_1
                    else:
                        stop_recording(file_name)


            elif data == "CLOSED LOOP" or data == "IDLE":
                # Handle motor state commands
                set_motor_state(data)

            else:
                print(f"Unknown command received: {data}")

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed for client {client_address}")

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            # Accept a new client connection
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
