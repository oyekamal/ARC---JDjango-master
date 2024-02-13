# your_app/signals.py
# import paho.mqtt.client as mqtt
from device.mqtt_functions import client
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Relay, RelayGroup, Device


@receiver(post_save, sender=RelayGroup)
def update_relays_on_relaygroup_change(sender, instance, **kwargs):
    if kwargs.get("created", False):
        # The RelayGroup instance is being created, no need to update relays.
        return

    print(f"Updating relays for RelayGroup: {instance}")

    # Get the related Relay instances
    for each_relay in instance.relays.all():
        each_relay.is_on = instance.is_on
        each_relay.save()


@receiver(post_save, sender=Device)
def update_relays(sender, instance, **kwargs):
    print("signals of device")
    if kwargs.get("created", False):
        # The RelayGroup instance is being created, no need to update relays.
        return

    # Get the related Relay instances
    for each_relay in Relay.objects.filter(device=instance):
        each_relay.is_on = instance.is_on
        each_relay.save()


@receiver(post_save, sender=Relay)
def update_relays(sender, instance, **kwargs):
    print("signals of relay")
    if kwargs.get("created", False):
        # The RelayGroup instance is being created, no need to update relays.
        return

    device_info = {
        "device_type": "slave",
        "device_name": "",
        "extra_info": "",
        "ip": "",
        "port": "",
        "RELAY_PINS": {},
        "relay_on_off": {},
        "message": "Update relay",
        "device_update": False,
    }
    device_info["device_name"] = instance.device.device_name
    device_info["ip"] = instance.device.device_ip
    device_info["device_update"] = True
    device_info["relay_on_off"][instance.relay_pin] = instance.is_on
    device = device_info["device_name"]+":" + device_info['ip']
    result = client.publish(device, str(device_info))
    print(f"Updating relays: {instance}")
