import RPi.GPIO as GPIO 
import time 
    
# Set up GPIO pins 
ENCODER_A = 21  # GPIO pin for A 
ENCODER_B = 20  # GPIO pin for B 
    
GPIO.setmode(GPIO.BCM)  # Use BCM numbering 
GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(ENCODER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    
position = 0 
last_A = GPIO.input(ENCODER_A) 
    
def update_position(channel): 
    global position 
    global last_A 
    current_A = GPIO.input(ENCODER_A) 
    current_B = GPIO.input(ENCODER_B) 
    
    if last_A == 0 and current_A == 1:  # Rising edge detected 
        if current_B == 0:  # A leads B: clockwise 
            position += 1 
        else:  # B leads A: counterclockwise 
            position -= 1 
    
    last_A = current_A 
    
# Set up event detection 
GPIO.add_event_detect(ENCODER_A, GPIO.BOTH, callback=update_position) 
GPIO.add_event_detect(ENCODER_B, GPIO.BOTH) 
    
try: 
    while True: 
        print("Position:", position) 
        time.sleep(0.1)  # Adjust the sleep time as needed 
    
except KeyboardInterrupt: 
    GPIO.cleanup()  # Clean up on exit 