import sys

if 'runserver' in sys.argv:
    from . import mqtt_functions
    mqtt_functions.client.loop_start()

# from . import mqtt_functions

# mqtt_functions.client.loop_start()
