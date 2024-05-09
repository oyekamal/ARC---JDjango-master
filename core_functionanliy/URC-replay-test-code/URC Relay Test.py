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
    {"on": 21, "off": 20, "color": "red"},  # Relay 1
    {"on": 16, "off": 12, "color": "blue"},  # Relay 2
    {"on": 7, "off": 8, "color": "green"},  # Relay 3
    {"on": 25, "off": 24, "color": "purple"},  # Relay 4
]
led_pins = {
    "red": 26,
    "green": 19,
    "blue": 13,
}  # Add white LED pin for flashing

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
# Function to set LED color for common cathode RGB LED
def set_led_color(color):
    if color == "red":
        led_pins["red"].ChangeDutyCycle(0)  # Red on
        led_pins["green"].ChangeDutyCycle(100)  # Green off
        led_pins["blue"].ChangeDutyCycle(100)  # Blue off
    elif color == "blue":
        led_pins["red"].ChangeDutyCycle(100)  # Red off
        led_pins["green"].ChangeDutyCycle(100)  # Green off
        led_pins["blue"].ChangeDutyCycle(0)  # Blue on
    elif color == "green":
        led_pins["red"].ChangeDutyCycle(100)  # Red off
        led_pins["green"].ChangeDutyCycle(0)  # Green on
        led_pins["blue"].ChangeDutyCycle(100)  # Blue off
    elif color == "purple":
        led_pins["red"].ChangeDutyCycle(0)  # Red on
        led_pins["green"].ChangeDutyCycle(100)  # Green off
        led_pins["blue"].ChangeDutyCycle(0)  # Blue on
    elif color == "white":
        led_pins["red"].ChangeDutyCycle(100)  # Red on
        led_pins["green"].ChangeDutyCycle(100)  # Green off
        led_pins["blue"].ChangeDutyCycle(100)  # Blue on


# Setup relay pins as outputs
for relay in relay_pins:
    GPIO.setup(relay["on"], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(relay["off"], GPIO.OUT, initial=GPIO.LOW)

# Function to toggle a relay
def toggle_relay(relay):
    on_pin = relay["on"]
    off_pin = relay["off"]
    set_led_color(relay["color"])

    print(f"Turning ON Relay: {on_pin}")
    GPIO.output(on_pin, GPIO.HIGH)
    time.sleep(1)  # Wait for 1 second
    GPIO.output(on_pin, GPIO.LOW)

    print(f"Turning OFF Relay: {off_pin}")
    GPIO.output(off_pin, GPIO.HIGH)
    time.sleep(1)  # Wait for 1 second
    GPIO.output(off_pin, GPIO.LOW)


# Docker Compose project directory
docker_compose_dir = "/home/arc/Documents/ARC---JDjango-master"

# Function to toggle Docker container state
def toggle_docker_state():
    os.chdir(
        docker_compose_dir
    )  # Change working directory to where docker-compose.yml is located
    if os.path.exists(docker_state_file):
        os.remove(docker_state_file)
        subprocess.call(["docker-compose", "down"])  # Stop Docker Compose project
        print("Docker Compose project down.")
    else:
        with open(docker_state_file, "w") as file:
            file.write("enabled")
        subprocess.call(
            ["docker-compose", "up", "--build", "-d"]
        )  # Start Docker Compose project
        print("Docker Compose project up.")


# Path to a flag file to persist the Docker container state across reboots
docker_state_file = "/tmp/docker_state"

# Main loop with button press detection for relay toggle and Docker control
current_relay_index = 0
try:
    while True:
        button_press_start_time = None
        while GPIO.input(button_pin) == GPIO.LOW:  # Button pressed
            if button_press_start_time is None:
                button_press_start_time = time.time()
            time.sleep(0.1)

        if button_press_start_time:
            button_press_duration = time.time() - button_press_start_time
            if button_press_duration >= 30:
                # Button held for 30 seconds, toggle Docker state
                set_led_color("white")
                toggle_docker_state()
                leds_off()  # Turn off LEDs after toggling Docker state
            else:
                # Short press, toggle relay
                toggle_relay(relay_pins[current_relay_index])
                current_relay_index = (current_relay_index + 1) % len(relay_pins)
except KeyboardInterrupt:
    # Cleanup GPIO on Ctrl+C
    GPIO.cleanup()
    print("GPIO cleanup completed. Program terminated.")
