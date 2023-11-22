from celery import shared_task
# celery -A core  beat -l info
# celery -A core.celery worker -l info
@shared_task
def task_name():
    # Your task logic goes here
    print("Task name")
    print("----------------------------------------------------------------")
