import ast
import platform
import time
import socket
import fcntl
import struct
import RPi.GPIO as GPIO
from flask import Flask
from flask_mqtt import Mqtt

# Function to get the IP address of a network interface


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])

# Function to get the MAC address of a network interface


def get_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(
        '256s', bytes(ifname[:15], 'utf-8')))
    return ''.join('%02x' % b for b in info[18:24])


# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

app = Flask(__name__)
app.config["SECRET"] = "my secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = "broker.hivemq.com"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
mqtt = Mqtt(app)

# Assuming eth0 is the interface you're interested in. Change to wlan0 if using WiFi.
interface_name = 'wlan0'
ip_address = get_ip_address(interface_name)
mac_address = get_mac_address(interface_name)
last_4_mac = mac_address.replace(":", "")[-4:]

# Update device information with dynamic IP and MAC address details
device_info = {
    "device_type": "slave",
    "device_name": f"URC4-{last_4_mac}",  # Updated with last 4 digits of MAC
    "extra_info": "Some extra info",
    "ip": ip_address,  # Dynamic IP address
    "port": 8081,
    "RELAY_PINS": {
        1: 3,
        2: 4,
        3: 6,
        4: 7,
    },
    "relay_on_off": [],
    "message": "hello Master",
    "device_update": False,
}


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    for relay_num, pin in device_info["RELAY_PINS"].items():
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Slave connected to MQTT broker")
    mqtt.subscribe(device_info["device_name"])
    result = mqtt.publish("master/slaves", str(device_info))
    if result:
        print("Message published successfully")
    else:
        print("Failed to publish message")


@mqtt.on_message()
def handle_message(client, userdata, message):
    string = message.payload.decode("utf-8")
    payload = ast.literal_eval(string)

    print(payload)
    if payload["device_update"] and payload["relay_on_off"]:
        print(payload["relay_on_off"])
        for each_relay in payload["relay_on_off"]:
            for key, value in each_relay.items():
                print("sending request to pin", key)
                GPIO.setup(key, GPIO.OUT)
                GPIO.output(key, GPIO.HIGH)
                time.sleep(0.8)
                GPIO.output(key, GPIO.LOW)

    print(f"Received message from {message.topic}: {payload['message']}")


@app.route("/")
def index():
    return "Slave Flask Application"


if __name__ == "__main__":
    initialize_gpio()
    app.run(host=ip_address, port=device_info["port"], debug=True)
