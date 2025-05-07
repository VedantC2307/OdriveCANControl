import customtkinter as ctk
import socket
import signal 
import sys
import threading
import time
import struct

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Control App")
        self.geometry("850x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # UDP setup for recording triggers
        self.udp_socket = None
        self.udp_thread = None
        self.udp_running = False

        # Adding a subtle gradient to the main window (using a frame overlay)
        self.gradient_frame = ctk.CTkFrame(self, fg_color=("gray15", "gray25"))
        self.gradient_frame.pack(fill="both", expand=True)

        # TCP Connect Frame
        tcp_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        tcp_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.ip_label = ctk.CTkLabel(tcp_frame, text="IP Address:")
        self.ip_label.grid(row=0, column=0, padx=10, pady=5)
        self.ip_entry = ctk.CTkEntry(tcp_frame, corner_radius=10)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)
        self.ip_entry.insert(0, "192.168.0.64")

        self.port_label = ctk.CTkLabel(tcp_frame, text="Port:")
        self.port_label.grid(row=0, column=2, padx=10, pady=5)
        self.port_entry = ctk.CTkEntry(tcp_frame, corner_radius=10)
        self.port_entry.grid(row=0, column=3, padx=10, pady=5)
        self.port_entry.insert(0, "1234")

        self.connect_btn = ctk.CTkButton(tcp_frame, text="Connect", corner_radius=10, hover_color="#357ABD", command=self.connect)
        self.connect_btn.grid(row=0, column=4, padx=10, pady=5)
        self.disconnect_btn = ctk.CTkButton(tcp_frame, text="Disconnect", corner_radius=10, hover_color="#D9534F", command=self.disconnect)
        self.disconnect_btn.grid(row=0, column=5, padx=10, pady=5)

        # Control Mode Frame
        control_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        control_label = ctk.CTkLabel(control_frame, text="Control Mode", font=("Arial", 14, "bold"))
        control_label.grid(row=0, column=0, padx=10, pady=5)

        self.control_mode = ctk.StringVar(value="Position")
        self.position_radio = ctk.CTkRadioButton(control_frame, text="Position", variable=self.control_mode, value="Position", hover_color="#5DADE2")
        self.position_radio.grid(row=1, column=0, padx=10, pady=5)
        self.velocity_radio = ctk.CTkRadioButton(control_frame, text="Velocity", variable=self.control_mode, value="Velocity", hover_color="#5DADE2")
        self.velocity_radio.grid(row=1, column=1, padx=10, pady=5)
        self.torque_radio = ctk.CTkRadioButton(control_frame, text="Torque", variable=self.control_mode, value="Torque", hover_color="#5DADE2")
        self.torque_radio.grid(row=1, column=2, padx=10, pady=5)

        self.value_entry = ctk.CTkEntry(control_frame, placeholder_text="Value", corner_radius=10)
        self.value_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.send_btn = ctk.CTkButton(control_frame, text="Send", corner_radius=10, hover_color="#357ABD", command=self.send_command)
        self.send_btn.grid(row=2, column=2, padx=10, pady=5)

        # Data Recording Frame
        data_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        data_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Add title to the Data Recording Frame
        recording_label = ctk.CTkLabel(data_frame, text="Data Recording", font=("Arial", 14, "bold"))
        recording_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Changed from "Subject Number" to "Subject Name"
        self.file_label = ctk.CTkLabel(data_frame, text="Subject Name:")
        self.file_label.grid(row=1, column=0, padx=10, pady=5)
        self.file_entry = ctk.CTkEntry(data_frame, corner_radius=10)
        self.file_entry.grid(row=1, column=1, padx=10, pady=5)
        self.file_entry.insert(0, "subject1")  # Default subject name

        # Toggle button for start/stop recording
        self.is_recording = False
        self.start_recording_btn = ctk.CTkButton(data_frame, text="Start Recording", corner_radius=10, hover_color="#357ABD", command=self.toggle_recording)
        self.start_recording_btn.grid(row=1, column=2, padx=10, pady=5)

        # Main container frame for Motor State and Buttons
        main_container_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        main_container_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        main_container_frame.grid_columnconfigure(0, weight=1)
        main_container_frame.grid_columnconfigure(1, weight=1)
        
        # Motor Toggle Frame (Left Side)
        motor_frame = ctk.CTkFrame(main_container_frame, corner_radius=15)
        motor_frame.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")

        motor_label = ctk.CTkLabel(motor_frame, text="Motor State", font=("Arial", 14, "bold"))
        motor_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.motor_state_switch = ctk.CTkSwitch(motor_frame, text=" ", onvalue="set_closed_loop", offvalue="set_idle", command=self.toggle_motor_state)
        self.motor_state_switch.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.motor_state_switch.deselect()  # Set default state to "IDLE"

        # Display current state label next to the switch
        self.current_state_label = ctk.CTkLabel(motor_frame, text="IDLE", font=("Arial", 14))
        self.current_state_label.grid(row=1, column=1, padx=(0,100), pady=5, sticky="w")

        # Controller & Odrive Node Start Button Frame (Right Side)
        motor_frame1 = ctk.CTkFrame(main_container_frame, corner_radius=15)
        motor_frame1.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="e")

        self.odrive_node_active = False
        self.controller_active = False
        self.odrive_node_btn = ctk.CTkButton(motor_frame1, text="Initialize Odrive Setup", corner_radius=10, command=self.toggle_odrive_setup)
        self.odrive_node_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.controller_btn = ctk.CTkButton(motor_frame1, text="Clear errors", corner_radius=10, command=self.toggle_clear_errors)
        self.controller_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.odrive_node_btn = ctk.CTkButton(motor_frame1, text="Motor Calibration", corner_radius=10, command=self.toggle_motor_calibration)
        self.odrive_node_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.controller_btn = ctk.CTkButton(motor_frame1, text="Encoder Offset Calibration", corner_radius=10, command=self.toggle_encoder_offset_calibration)
        self.controller_btn.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.odrive_node_btn = ctk.CTkButton(motor_frame1, text="Encoder Offset", corner_radius=10, command=self.encoder_offset_zero)
        self.odrive_node_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        self.controller_btn = ctk.CTkButton(motor_frame1, text="Start Controller", corner_radius=10, command=self.start_controller)
        self.controller_btn.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # Start UDP listener
        self.start_udp_listener()

    def toggle_odrive_setup(self):
        """Toggle ODrive setup and send 'initialize' command."""
        """Send the 'initialize' command without changing the button text."""
        command = "initialize"
        self.send_tcp_message(command)

    def start_controller(self):
        """Start Odrive Controller"""
        command = "start_controller"
        print(f"Sending start controller command: {command}")
        self.send_tcp_message(command)

    def encoder_offset_zero(self):
        """Encoder offset to zero"""
        command = "encoder_offset"
        self.send_tcp_message(command)

    def toggle_clear_errors(self):
        """Send the 'initialize' command without changing the button text."""
        command = "clear_error"
        self.send_tcp_message(command)

    def toggle_motor_calibration(self):
        """Toggle ODrive setup and send 'initialize' command."""
        """Send the 'initialize' command without changing the button text."""
        command = "motor_calibration"
        self.send_tcp_message(command)

    def toggle_encoder_offset_calibration(self):
        """Send the 'initialize' command without changing the button text."""
        command = "encoder_offset_calibration"
        self.send_tcp_message(command)

    def send_tcp_message(self, message):
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                print(f"DEBUG: About to send message: '{message}'")
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Sent command: {message}")
                
                # Add a small delay to ensure command processing
                time.sleep(0.1)
                
                # Optionally try to get a response to confirm command receipt
                try:
                    self.client_socket.settimeout(0.5)  # Short timeout for response
                    response = self.client_socket.recv(1024)
                    print(f"Response from server: {response.decode('utf-8')}")
                except socket.timeout:
                    print("No response from server (timeout)")
                except Exception as e:
                    print(f"Error receiving response: {e}")
                finally:
                    self.client_socket.settimeout(None)  # Reset timeout
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def toggle_motor_state(self):
        # Update the state label based on the toggle switch state
        current_state = self.motor_state_switch.get()
        self.current_state_label.configure(text=current_state.upper())
        
        # Make sure we send the exact command in the correct format
        if current_state == "idle":
            command = "set_idle"
        else:
            command = "set_closed_loop"
            
        print(f"Sending motor state command: {command}")
        self.send_tcp_message(command)

    def connect(self):
        ip_address = self.ip_entry.get()
        port = int(self.port_entry.get())

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {ip_address} on port {port}...")
        try:
            self.client_socket.connect((ip_address, port))
            print(f"Successfully connected to {ip_address} on port {port}")
        except Exception as e:
            print(f"Failed to connect to {ip_address} on port {port}: {e}")

    def disconnect(self):
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.close()
                print("Disconnected from the server.")
            else:
                print("No active connection to disconnect.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

    def send_command(self):
        mode = self.control_mode.get()
        value = self.value_entry.get()

        message = f"{mode}:{value}"
        
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Sent command: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def toggle_recording(self, external_trigger=None):
        """
        Toggle recording state, can be triggered by UI button or external UDP message
        external_trigger: If provided, uses this value (1.0 = start, 0.0 = stop)
        """
        # If triggered externally, set recording state based on the trigger value
        if external_trigger is not None:
            should_record = (external_trigger == 1.0)
            
            # Only take action if the state would change
            if should_record != self.is_recording:
                self.is_recording = should_record
                if self.is_recording:
                    print("External trigger received to start recording")
                    self.start_recording()
                    self.start_recording_btn.configure(text="Stop Recording")
                    print("Recording started by external trigger")
                else:
                    self.stop_recording()
                    self.start_recording_btn.configure(text="Start Recording")
                    print("Recording stopped by external trigger")
        else:
            # Original UI button logic
            if not self.is_recording:
                self.is_recording = True
                self.start_recording()
                self.start_recording_btn.configure(text="Stop Recording")
            else:
                self.is_recording = False
                self.stop_recording()
                self.start_recording_btn.configure(text="Start Recording")

    def start_recording(self):
        file_name = self.file_entry.get()
        message = f"start_recording,{file_name}"

        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Recording started for Subject: {file_name}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def stop_recording(self):
        file_name = self.file_entry.get()
        message = f"stop_recording,{file_name}"
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print("Recording stopped.")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def start_udp_listener(self):
        """Initialize and start UDP listener thread"""
        try:
            # Create UDP socket
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(('0.0.0.0', 9000))  # Listen on all interfaces, port 5678
            self.udp_socket.settimeout(1.0)  # 1 second timeout for clean shutdown
            
            # Start UDP listener thread
            self.udp_running = True
            self.udp_thread = threading.Thread(target=self.udp_listener)
            self.udp_thread.daemon = True  # Thread will close when main program exits
            self.udp_thread.start()
            print("UDP listener started on port 5678")
        except Exception as e:
            print(f"Failed to start UDP listener: {e}")

    def udp_listener(self):
        """Thread function to listen for UDP messages"""
        while self.udp_running:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                print(f"Received data from {addr}: {data}")
                
                try:
                    # Unpack both position and boolean values from the received data
                    # Assuming format is: double (position) followed by double (boolean as 0.0 or 1.0)
                    trigger_value = struct.unpack('d', data)
                    print(f"trigger value: {trigger_value}")
                    
                    # Handle the trigger value for recording (existing functionality)
                    self.after(0, lambda: self.toggle_recording(external_trigger=trigger_value))
                    
                    
                except struct.error as e:
                    print(f"Error unpacking data: {e}. Expected format: 'dd' (two double values)")
                except ValueError:
                    print(f"Received invalid values: {data}")
            except socket.timeout:
                # This is expected due to the socket timeout
                pass
            except Exception as e:
                print(f"Error in UDP listener: {e}")
                time.sleep(1)  # Prevent tight loop in case of persistent errors

    def handle_position_update(self, position):
        """Process the position value received via UDP"""
        print(f"Processing position update: {position}")
        # You can add code to handle the position value here
        # For example, update a display, send to the motor controller, etc.
        
        # Optional: Automatically update position control value if in position mode
        if self.control_mode.get() == "Position":
            self.value_entry.delete(0, 'end')
            self.value_entry.insert(0, str(position))
            # Uncomment the next line if you want to automatically send the command
            # self.send_command()

    def on_closing(self):
        """Clean up resources before closing"""
        # Stop UDP thread
        if hasattr(self, 'udp_running'):
            self.udp_running = False
        
        # Close UDP socket if it exists
        if hasattr(self, 'udp_socket') and self.udp_socket:
            self.udp_socket.close()
            
        # Close TCP connection if it exists
        if hasattr(self, 'client_socket') and self.client_socket:
            self.client_socket.close()
            
        # Destroy the window
        self.destroy()

def signal_handler(sig, frame):
    print("\nGracefully exiting...")
    app.on_closing()  # Use our clean shutdown method
    sys.exit(0)

if __name__ == '__main__':
    app = ModernApp()
    signal.signal(signal.SIGINT, signal_handler)  # Bind the signal handler
    
    # Override the window close button to use our clean shutdown
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    app.mainloop()
