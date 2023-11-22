from celery import shared_task
# celery -A core  beat -l info
# celery -A core.celery worker -l info

from datetime import datetime, time
from .models import RelaySchedule


@shared_task
def task_name():
    # Your task logic goes here
    relay_schedules = RelaySchedule.objects.all()
    for each_schedule in relay_schedules:
        current_time = datetime.now().time()

        if each_schedule.start_time <= current_time <= each_schedule.end_time:
            print("Relay on")
            # relay.is_on = True
        else:
            print("Relay off")
            # relay.is_on = False

        # relay.save()
    print("----------------------------------------------------------------")
