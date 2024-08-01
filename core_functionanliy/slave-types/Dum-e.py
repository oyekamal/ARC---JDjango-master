import ast
import platform
import time
import socket
import fcntl
import struct
import subprocess
import os
from flask import Flask
from flask_mqtt import Mqtt
import RPi.GPIO as GPIO
import threading

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

# Define pins
button_pin = 27  # Button pin
led_pins = {"red": 26, "green": 19, "blue": 13}  # LED pins

# Setup button and LED pins
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for color, pin in led_pins.items():
    GPIO.setup(pin, GPIO.OUT)
    led_pins[color] = GPIO.PWM(pin, 100)  # Set PWM at 100 Hz
    led_pins[color].start(0)

# Network functions
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(), 0x8915, struct.pack("256s", ifname[:15].encode("utf-8"))
        )[20:24]
    )


def get_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(
        s.fileno(), 0x8927, struct.pack("256s", bytes(ifname[:15], "utf-8"))
    )
    return "".join("%02x" % b for b in info[18:24])


def find_available_port(start=5000, end=5100):
    """
    Find an available port within the given range.

    :param start: Start of port range
    :param end: End of port range
    :return: Available port
    """
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # Attempt to bind to the port
                s.bind(("localhost", port))
                return port
            except OSError:
                pass  # Port is in use, continue to next port
    return None  # No available ports found


# Flask and MQTT setup
app = Flask(__name__)
app.config["SECRET"] = "my secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = "mqtt.eclipseprojects.io"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
mqtt = Mqtt(app)

# Relay configuration
# you can change the relays here
relay_pins = {
    1: {"on": 21, "off": 20, "color": "red"},  # Relay 1
    2: {"on": 16, "off": 12, "color": "blue"},  # Relay 2
    3: {"on": 7, "off": 15, "color": "green"},  # Relay 3
    4: {"on": 25, "off": 24, "color": "purple"},  # Relay 4
    5: {"on": 21, "off": 20, "color": "red"},  # Relay 5
    6: {"on": 16, "off": 12, "color": "blue"},  # Relay 6
    7: {"on": 7, "off": 15, "color": "green"},  # Relay 7
    8: {"on": 25, "off": 24, "color": "purple"},  # Relay 8
}

# Setup relay pins as outputs
for relay in relay_pins.values():
    GPIO.setup(relay["on"], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(relay["off"], GPIO.OUT, initial=GPIO.LOW)

# Network configuration
interface_name = "wlan0"
ip_address = get_ip_address(interface_name)
mac_address = get_mac_address(interface_name)
last_4_mac = mac_address.replace(":", "")[-4:]

custom_ip = ip_address
# custom_port = 8080
custom_port = find_available_port()

# Device information
device_info = {
    "device_type": "slave",
    "device_name": f"Dim-E-{last_4_mac}",
    "extra_info": str(relay_pins),
    "ip": custom_ip,
    "port": custom_port,
    "RELAY_PINS": {
        i: i for i in relay_pins
    },  # add pin automatically for master to send request back
    "relay_on_off": [],
    "message": "hello Master",
    "device_update": False,
}

# LED control functions
def leds_off():
    for color in led_pins:
        led_pins[color].ChangeDutyCycle(0)


def set_led_color(color):
    if color == "red":
        led_pins["red"].ChangeDutyCycle(100)
        led_pins["green"].ChangeDutyCycle(0)
        led_pins["blue"].ChangeDutyCycle(0)
    elif color == "blue":
        led_pins["red"].ChangeDutyCycle(0)
        led_pins["green"].ChangeDutyCycle(0)
        led_pins["blue"].ChangeDutyCycle(100)
    elif color == "green":
        led_pins["red"].ChangeDutyCycle(0)
        led_pins["green"].ChangeDutyCycle(100)
        led_pins["blue"].ChangeDutyCycle(0)
    elif color == "purple":
        led_pins["red"].ChangeDutyCycle(100)
        led_pins["green"].ChangeDutyCycle(0)
        led_pins["blue"].ChangeDutyCycle(100)
    elif color == "white":
        led_pins["red"].ChangeDutyCycle(100)
        led_pins["green"].ChangeDutyCycle(100)
        led_pins["blue"].ChangeDutyCycle(100)


# Relay control function
def toggle_relay(relay_num):
    relay = relay_pins[relay_num]
    on_pin = relay["on"]
    off_pin = relay["off"]
    set_led_color(relay["color"])

    print(f"Turning ON Relay: {on_pin}")
    GPIO.setup(on_pin, GPIO.OUT)
    GPIO.output(on_pin, GPIO.HIGH)
    time.sleep(0.8)
    GPIO.output(on_pin, GPIO.LOW)

    print(f"Turning OFF Relay: {off_pin}")
    GPIO.setup(off_pin, GPIO.OUT)
    GPIO.output(off_pin, GPIO.HIGH)
    time.sleep(0.8)
    GPIO.output(off_pin, GPIO.LOW)


# Docker control
docker_compose_dir = "/home/arc/Documents/ARC---JDjango-master"
docker_state_file = "/tmp/docker_state"


def toggle_docker_state():
    os.chdir(docker_compose_dir)
    if os.path.exists(docker_state_file):
        os.remove(docker_state_file)
        subprocess.call(["docker-compose", "down"])
        print("Docker Compose project down.")
    else:
        with open(docker_state_file, "w") as file:
            file.write("enabled")
        subprocess.call(["docker-compose", "up", "--build", "-d"])
        print("Docker Compose project up.")


# MQTT handlers
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Slave connected to MQTT broker")
    mqtt.subscribe(device_info["device_name"] + ":" + device_info["ip"])
    result = mqtt.publish("master/slaves", str(device_info))
    if result:
        print("Message published successfully")
    else:
        print("Failed to publish message")


@mqtt.on_message()
def handle_message(client, userdata, message):
    string = message.payload.decode("utf-8")
    payload = ast.literal_eval(string)
    print("--------------------------------")
    print(payload)
    print("--------------------------------")
    if payload["device_update"] and payload["relay_on_off"]:
        print(payload["relay_on_off"])
        for key, value in payload["relay_on_off"].items():
            relay = relay_pins[int(key)]
            pin = relay["on"] if value else relay["off"]
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            print("...............high.................")
            time.sleep(0.8)
            print("--------------break after 0.8s------------------")
            GPIO.output(pin, GPIO.LOW)
            print("...............low.................")
            print("...............toggle end.................")
    print(f"Received message from {message.topic}: {payload['message']}")


@app.route("/")
def index():
    return "URC Slave Flask Application"


def button_handler():
    current_relay_index = 0
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
                toggle_relay(current_relay_index + 1)
                current_relay_index = (current_relay_index + 1) % len(relay_pins)


if __name__ == "__main__":
    # Start button handler in a separate thread
    button_thread = threading.Thread(target=button_handler)
    button_thread.daemon = True
    button_thread.start()

    # Run Flask app
    app.run(host=custom_ip, port=custom_port, debug=True)
