# mqtt_singleton.py
import threading
import paho.mqtt.client as mqtt
from django.conf import settings


class MqttSingleton:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def __init__(self):
        if not hasattr(self.__class__, '_instance'):
            self._client = mqtt.Client(userdata={'is_master': True})
            self._client.on_connect = self.on_connect
            self._client.on_message = self.on_message
            self._client.username_pw_set(
                settings.MQTT_USER, settings.MQTT_PASSWORD)
            self._client.connect(
                host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=settings.MQTT_KEEPALIVE)
            self._client.loop_start()
            print("Starting MQTT server...")

    @property
    def client(self):
        return self._client

    # Define your callback functions here
    def on_connect(self, mqtt_client, userdata, flags, rc):
        # ... your existing on_connect code ...
        if rc == 0:
            print("Connected successfully")
            #    mqtt_client.subscribe('django/mqtt')
            # Only the designated master client will subscribe to the topic
            if userdata['is_master']:
                mqtt_client.subscribe("master/slaves", qos=2)

        else:
            print("Bad connection. Code:", rc)

    def on_message(self, mqtt_client, userdata, msg):
        # ... your existing on_message code ...
        import ast

        from device.models import Device, Relay

        print(
            f"Received message on topic: {msg.topic} with payload: {msg.payload}")
        string = msg.payload.decode("utf-8")
        print("--------------data------------------")
        print(string)
        print("---------------enddata-----------------")
        payload = ast.literal_eval(string)
        update_create_device(payload)
        payload["message"] = f"hello  {payload.get('device_name')} im Master."
        device = payload.get("device_name")+":" + payload.get('ip')

        result = mqtt_client.publish(device, str(payload))

    # Move the update_create_device function into this class
    def update_create_device(self, payload):
        # ... your existing update_create_device code ...
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
                    # Update extra info as needed
                    extra=payload.get("extra_info"),
                )
                new_device.save()

                # Create relays for the new device
                if "RELAY_PINS" in payload:
                    for relay_number, relay_pin in payload["RELAY_PINS"].items():
                        new_relay = Relay(
                            relay_pin=relay_pin,
                            is_on=True,  # Update as needed
                            # Update as needed
                            relay_name=f"Relay {relay_number}",
                            device=new_device,
                        )
                        new_relay.save()
