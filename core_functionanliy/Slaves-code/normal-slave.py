import socket
import ast
import platform
import time

from flask import Flask
from flask_mqtt import Mqtt

# import RPi.GPIO as GPIO #sudo pip install --upgrade RPi.GPIO


# # # Check if the script is running on a Raspberry Pi
# # # ON_RASPBERRY_PI = 'arm' in platform.machine()

# # # if ON_RASPBERRY_PI:
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(True)

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

# Define the IP and port you want the app to run on

custom_ip = "127.0.0.12"
custom_port = 8080

device_info = {
    "device_type": "slave",
    "device_name": "TD-16R-2-open",
    "extra_info": "Some extra info",
    "ip": custom_ip,
    "port": custom_port,
    "RELAY_PINS": {
        1: 3,
        2: 4,
    },
    "relay_on_off": [],
    "message": "hello Master",
    "device_update": False,
}

# def update_relay_json(relays):
#     relay_on_off_list = []
#     for each_relay in relays:
#         relay_on_off_list.append({each_relay.relay_pin: each_relay.is_on})
#     return relay_on_off_list

# def initialize_gpio():
#     GPIO.setmode(GPIO.BCM)
#     for relay_num, pin in device_info["RELAY_PINS"].items():
#         GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)


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
    print("--------------------------------")
    print(payload)
    print("--------------------------------")
    if payload["device_update"] and payload["relay_on_off"]:
        print(payload["relay_on_off"])
        for key, value in payload["relay_on_off"].items():
            print("sending request to pin", key)
            # GPIO.setup(key, GPIO.OUT)
            # GPIO.output(key, GPIO.HIGH)
            print("...............high.................")
            # time.sleep(0.8)
            print("--------------break after 0.8s------------------")
            # GPIO.output(key, GPIO.LOW)
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
