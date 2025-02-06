import customtkinter as ctk
import socket
import signal 
import sys

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Motor Control App")
        self.geometry("900x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main container with gradient background
        self.main_frame = ctk.CTkFrame(self, fg_color=("gray10", "gray20"))
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Connection Section
        connection_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        connection_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        
        # IP/Port Inputs
        ctk.CTkLabel(connection_frame, text="IP Address:", font=("Arial", 12)).grid(row=0, column=0, padx=(10, 2))
        self.ip_entry = ctk.CTkEntry(connection_frame, width=120, corner_radius=10)
        self.ip_entry.grid(row=0, column=1, padx=5)
        self.ip_entry.insert(0, "172.26.33.8")

        ctk.CTkLabel(connection_frame, text="Port:", font=("Arial", 12)).grid(row=0, column=2, padx=(10, 2))
        self.port_entry = ctk.CTkEntry(connection_frame, width=80, corner_radius=10)
        self.port_entry.grid(row=0, column=3, padx=5)
        self.port_entry.insert(0, "1234")

        # Connection Buttons
        self.connect_btn = ctk.CTkButton(
            connection_frame, 
            text="Connect", 
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            corner_radius=10,
            command=self.connect
        )
        self.connect_btn.grid(row=0, column=4, padx=(20, 5))

        self.disconnect_btn = ctk.CTkButton(
            connection_frame, 
            text="Disconnect",
            fg_color="#C62828",
            hover_color="#B71C1C",
            corner_radius=10,
            command=self.disconnect
        )
        self.disconnect_btn.grid(row=0, column=5, padx=5)

        # Control Section
        control_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        control_frame.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        
        # Control Mode
        ctk.CTkLabel(control_frame, text="Control Mode:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.control_mode = ctk.StringVar(value="Position")
        modes = [("Position", "#388E3C"), ("Velocity", "#1976D2"), ("Torque", "#D32F2F")]
        for col, (text, color) in enumerate(modes):
            btn = ctk.CTkRadioButton(
                control_frame,
                text=text,
                variable=self.control_mode,
                value=text,
                border_color=color,
                hover_color=color,
                fg_color=color
            )
            btn.grid(row=1, column=col, padx=10, pady=5)

        # Value Input
        self.value_entry = ctk.CTkEntry(
            control_frame,
            placeholder_text="Enter value...",
            width=200,
            corner_radius=10
        )
        self.value_entry.grid(row=1, column=3, padx=10, pady=5)

        self.send_btn = ctk.CTkButton(
            control_frame,
            text="Send Command",
            fg_color="#1565C0",
            hover_color="#0D47A1",
            corner_radius=10,
            command=self.send_command
        )
        self.send_btn.grid(row=1, column=4, padx=10, pady=5)

        # Status and Actions Section
        status_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        status_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        status_frame.grid_columnconfigure((0, 1), weight=1)

        # Motor Status
        motor_status_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        motor_status_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(motor_status_frame, text="Motor State:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5)
        self.state_label = ctk.CTkLabel(motor_status_frame, text="IDLE", font=("Arial", 14, "bold"), text_color="#42A5F5")
        self.state_label.grid(row=0, column=1, padx=5)
        
        self.state_switch = ctk.CTkSwitch(
            motor_status_frame,
            text="Toggle State",
            progress_color="#42A5F5",
            command=self.toggle_motor_state
        )
        self.state_switch.grid(row=0, column=2, padx=10)

        # Control Buttons
        button_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        buttons = [
            ("Initialize Odrive", "#00796B", self.toggle_odrive_setup),
            ("Clear Errors", "#D84315", self.toggle_clear_errors),
            ("Motor Calibration", "#0288D1", self.toggle_motor_calibration),
            ("Encoder Calibration", "#7B1FA2", self.toggle_encoder_offset_calibration)
        ]

        for row, (text, color, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                fg_color=color,
                hover_color=self.darken_color(color),
                corner_radius=10,
                command=command
            )
            btn.grid(row=row//2, column=row%2, padx=5, pady=5, sticky="ew")

    def darken_color(self, color, factor=0.8):
        """Utility function to darken a hex color"""
        rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(component * factor)) for component in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'


    def toggle_odrive_setup(self):
        """Toggle ODrive setup and send 'initialize' command."""
        """Send the 'initialize' command without changing the button text."""
        command = "initialize"
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
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Sent command: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def toggle_motor_state(self):
        # Update the state label based on the toggle switch state
        current_state = self.motor_state_switch.get()
        self.current_state_label.configure(text=current_state)
        print(current_state)
        self.send_tcp_message(current_state)

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

    def toggle_recording(self):
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.start_recording()
            self.start_recording_btn.configure(text="Stop")
        else:
            # Stop recording
            self.is_recording = False
            self.stop_recording()
            self.start_recording_btn.configure(text="Start")

    def start_recording(self):
        topic_name = self.topic_entry.get()
        topic_name_1 = self.topic_entry1.get()
        file_name = self.file_entry.get()

        # Create the message based on the available topic names
        message = f"{self.is_recording},{topic_name}"
        if topic_name_1:
            message += f",{topic_name_1}"
        message += f",{file_name}"

        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Recording started for Topic: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def stop_recording(self):
        file_name = self.file_entry.get()
        message = f"{self.is_recording},{file_name}"
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print("Recording stopped.")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")
    
def signal_handler(sig, frame):
    print("\nExiting application...")
    app.destroy()
    sys.exit(0)

if __name__ == '__main__':
    app = ModernApp()
    signal.signal(signal.SIGINT, signal_handler)
    app.mainloop()