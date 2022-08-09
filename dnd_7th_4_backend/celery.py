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

# task 함수 주기 설정
app.conf.beat_schedule = {
          	'add-every-60-minutes-api6': {
          		'task': 'main.tasks.api_6',
          		'schedule': crontab(minute='*/60'),

          	},

          }