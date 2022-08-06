from celery import shared_task, Celery

celery = Celery(__name__)
celery.config_from_object(__name__)

@celery.task
def say_hello():
    print("hello, world")
    return 'say_hello'