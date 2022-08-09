from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# 기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnd_7th_4_backend.settings')
app = Celery('dnd_7th_4_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

#등록된 장고 앱 설정에서 task 불러오기
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # 'api1' : {  # 스케쥴링 이름
    #     'task' : 'main.tasks.api1_update',  # 수행할 task 설정
    #     'schedule': crontab(minute=22, hour=1),  # 수행할 시간 설정
    # },
    # 'printTime': {
    #     'task' : 'main.tasks.printName',
    #     'schedule': crontab(),
    # }
}