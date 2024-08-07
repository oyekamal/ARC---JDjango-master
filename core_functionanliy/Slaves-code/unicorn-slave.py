import ast
import platform
import time
import socket
import fcntl
import struct
from flask import Flask
from flask_mqtt import Mqtt

import RPi.GPIO as GPIO  # sudo pip install --upgrade RPi.GPIO


# # Check if the script is running on a Raspberry Pi
# # ON_RASPBERRY_PI = 'arm' in platform.machine()


# # if ON_RASPBERRY_PI:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack("256s", ifname[:15].encode("utf-8")),
        )[20:24]
    )


def get_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(
        s.fileno(), 0x8927, struct.pack("256s", bytes(ifname[:15], "utf-8"))
    )
    return "".join("%02x" % b for b in info[18:24])


app = Flask(__name__)
app.config["SECRET"] = "my secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config["MQTT_BROKER_URL"] = "broker.hivemq.com"
app.config["MQTT_BROKER_URL"] = "mqtt.eclipseprojects.io"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
mqtt = Mqtt(app)
relay_pins = {
    1: {True: 21, False: 20, "color": "red"},  # Relay 1
    2: {True: 16, False: 12, "color": "blue"},  # Relay 2
    3: {True: 7, False: 15, "color": "green"},  # Relay 3
    4: {True: 25, False: 24, "color": "purple"},  # Relay 4
}
# Define the IP and port you want the app to run on

# Assuming eth0 is the interface you're interested in. Change to wlan0 if using WiFi.
interface_name = "wlan0"
ip_address = get_ip_address(interface_name)
mac_address = get_mac_address(interface_name)
last_4_mac = mac_address.replace(":", "")[-4:]

custom_ip = ip_address
custom_port = 8080

device_info = {
    "device_type": "slave",
    "device_name": f"URC-firmware-{last_4_mac}",
    "extra_info": str(relay_pins),
    "ip": custom_ip,
    "port": custom_port,
    "RELAY_PINS": {
        1: 1,  # {"on": 21, "off": 20, "color": "red"},    # Relay 1
        2: 2,  # {"on": 16, "off": 12, "color": "blue"},   # Relay 2
        3: 3,  # {"on": 7, "off": 8, "color": "green"},    # Relay 3
        4: 4,  # {"on": 25, "off": 24, "color": "purple"}  # Relay 4
    },
    "relay_on_off": [],
    "message": "hello Master",
    "device_update": False,
}


def update_relay_json(relays):
    relay_on_off_list = []
    for each_relay in relays:
        relay_on_off_list.append({each_relay.relay_pin: each_relay.is_on})
    return relay_on_off_list


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    for relay_num, pin in device_info["RELAY_PINS"].items():
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)


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
            # print("sending request to pin", key)
            # print("with value : ", value)
            pin = relay_pins[key][value]

            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            print("...............high.................")
            time.sleep(0.8)
            print("--------------break after 0.8s------------------")
            GPIO.output(pin, GPIO.LOW)
            print("...............low.................")

            print("...............toogle end.................")

        # logic for toggling device
    print(f"Received message from {message.topic}: {payload['message']}")


@app.route("/")
def index():
    return "Slave Flask Application"


if __name__ == "__main__":
    # initialize_gpio()
    app.run(host=custom_ip, port=custom_port, debug=True)
