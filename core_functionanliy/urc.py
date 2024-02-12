import RPi.GPIO as GPIO
import time
import subprocess
import os

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pins
button_pin = 27  # Button pin
relay_pins = [
    {"on": 21, "off": 20, "color": "red"},    # Relay 1
    {"on": 16, "off": 12, "color": "blue"},   # Relay 2
    {"on": 7, "off": 8, "color": "green"},    # Relay 3
    {"on": 25, "off": 24, "color": "purple"}  # Relay 4
]
led_pins = {"red": 26, "green": 19, "blue": 13,
            "white": 22}  # Add white LED pin for flashing

# Setup button and LED pins
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for color, pin in led_pins.items():
    GPIO.setup(pin, GPIO.OUT)
    led_pins[color] = GPIO.PWM(pin, 100)  # Set PWM at 100 Hz
    led_pins[color].start(0)

# Function to turn off all LEDs


def leds_off():
    for color in led_pins:
        led_pins[color].ChangeDutyCycle(0)

# Function to set LED color, including white for flashing


def set_led_color(color, duty_cycle=100):
    leds_off()
    if color in led_pins:
        led_pins[color].ChangeDutyCycle(duty_cycle)


# Path to a flag file to persist the Docker container state across reboots
docker_state_file = "/tmp/docker_state"

# Function to toggle Docker container state


def toggle_docker_state():
    if os.path.exists(docker_state_file):
        os.remove(docker_state_file)
        # Stop Docker container
        subprocess.call(["docker", "stop", "your_container_name"])
        print("Docker instance disabled.")
    else:
        with open(docker_state_file, "w") as file:
            file.write("enabled")
        # Start Docker container
        subprocess.call(["docker", "start", "your_container_name"])
        print("Docker instance enabled.")

# Function to check button hold time and toggle Docker state if held for 30 seconds


def check_button_hold():
    button_pressed_time = None
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:  # Button pressed
            if button_pressed_time is None:
                button_pressed_time = time.time()
            else:
                if (time.time() - button_pressed_time) >= 30:  # Button held for 30 seconds
                    set_led_color("white", 50)  # Flash white LED
                    toggle_docker_state()
                    break
        else:
            button_pressed_time = None
        time.sleep(0.1)


# Check Docker state on startup and ensure the container is in the desired state
if os.path.exists(docker_state_file):
    # Ensure Docker container is started
    subprocess.call(["docker", "start", "your_container_name"])
else:
    # Ensure Docker container is stopped
    subprocess.call(["docker", "stop", "your_container_name"])

# Main loop
try:
    while True:
        check_button_hold()
except KeyboardInterrupt:
    # Cleanup GPIO on Ctrl+C
    GPIO.cleanup()
    print("GPIO cleanup completed. Program terminated.")
