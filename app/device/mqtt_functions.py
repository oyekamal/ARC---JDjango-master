import sys

import paho.mqtt.client as mqtt
from django.conf import settings

# from device.models import Device, Relay


def update_create_device(payload):
    from device.models import Device, Relay

    if "device_name" in payload and "ip" in payload:
        device_name = payload.get("device_name")
        device_type = payload.get("device_type")
        device_ip = payload["ip"]

        # Check if the device already exists in the database
        existing_device = Device.objects.filter(
            device_name=device_name, device_ip=device_ip, device_type=device_type
        ).first()

        if existing_device:
            # Update the existing device's information
            existing_device.is_on = True  # Update as needed
            existing_device.extra = payload.get(
                "extra_info"
            )  # Update extra info as needed
            existing_device.save()

            # Update or create relays
            if "RELAY_PINS" in payload:
                for relay_number, relay_pin in payload["RELAY_PINS"].items():
                    relay, created = Relay.objects.get_or_create(
                        device=existing_device, relay_pin=relay_pin
                    )
                    relay.is_on = True  # Update as needed
                    # relay.relay_name = f"Relay {relay_number}"  # Update as needed
                    relay.save()

        else:
            # Create a new device entry
            new_device = Device(
                device_name=device_name,
                device_ip=device_ip,
                device_type=device_type,
                is_on=True,  # Update as needed
                extra=payload.get("extra_info"),  # Update extra info as needed
            )
            new_device.save()

            # Create relays for the new device
            if "RELAY_PINS" in payload:
                for relay_number, relay_pin in payload["RELAY_PINS"].items():
                    new_relay = Relay(
                        relay_pin=relay_pin,
                        is_on=True,  # Update as needed
                        relay_name=f"Relay {relay_number}",  # Update as needed
                        device=new_device,
                    )
                    new_relay.save()


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        #    mqtt_client.subscribe('django/mqtt')
        # Only the designated master client will subscribe to the topic
        # if userdata['is_master']:
        mqtt_client.subscribe("master/slaves", qos=2)

    else:
        print("Bad connection. Code:", rc)


def off_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Bad connection. Code:", rc)


def on_message(mqtt_client, userdata, msg):
    import ast

    from device.models import Device, Relay

    print(f"Received message on topic: {msg.topic} with payload: {msg.payload}")
    string = msg.payload.decode("utf-8")
    print("--------------data------------------")
    print(string)
    print("---------------enddata-----------------")
    payload = ast.literal_eval(string)
    update_create_device(payload)
    payload["message"] = f"hello  {payload.get('device_name')} im Master."
    device = payload.get("device_name") + ":" + payload.get("ip")

    result = mqtt_client.publish(device, str(payload))


# Assuming you have a way to determine whether the current client is the master
# Replace with actual logic to identify master
master_client_info = {"is_master": True}

# client = mqtt.Client(userdata=master_client_info)
client = mqtt.Client()


print(" sys.argv :", sys.argv)

if "runserver" in sys.argv:

    client.on_connect = on_connect
else:
    client.on_connect = off_connect


client.on_connect = on_connect
client.on_message = on_message
# client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE,
)
