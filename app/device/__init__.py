import sys


if 'runserver' in sys.argv and 'manage.py' in sys.argv:
    print("Starting.. MQtt server")
    from . import mqtt_functions
    mqtt_functions.client.loop_start()


# __init__.py
# import sys
# from .mqtt_singleton import MqttSingleton

# if 'runserver' in sys.argv and 'manage.py' in sys.argv:
#     print("Starting MQTT server")
#     mqtt_instance = MqttSingleton.getInstance()


# from . import mqtt_functions

# mqtt_functions.client.loop_start()
