from celery import shared_task

# celery -A core  beat -l info
# celery -A core.celery worker -l info

from datetime import datetime, time
from .models import RelaySchedule

import requests
import json


def mqtt_request(device_info):
    url = "http://localhost:8000/publish/"

    payload = json.dumps(device_info)
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


@shared_task
def task_name():
    # Your task logic goes here
    relay_schedules = RelaySchedule.objects.all()
    for each_schedule in relay_schedules:
        current_time = datetime.now().time()

        if each_schedule.start_time <= current_time <= each_schedule.end_time:
            print("Relay on")
            relay = each_schedule.relay
            print(relay.is_on)
            # if not relay.is_on:
            relay.is_on = True
            relay.save()
            print("updated  relay to on ")
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
            device_info["device_name"] = relay.device.device_name
            device_info["device_update"] = True
            device_info["relay_on_off"][relay.relay_pin] = True
            mqtt_request(device_info)
        else:
            print("Relay off")
            # relay.is_on = False

        relay.save()
    print("----------------------------------------------------------------")
