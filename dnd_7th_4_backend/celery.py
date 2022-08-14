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

    # 'api1' : {  # 스케쥴링 이름
    #     'task' : 'main.tasks.api1_update',  # 수행할 task 설정
    #     'schedule': crontab(minute=53, hour=19),  # 수행할 시간 설정
    # },
    #  'printTime': {
    #      'task' : 'main.tasks.printName', # 테스트용
    #      'schedule': crontab(minute=5, hour='*'), # 매 시간 5분마다 실행 0005, 0105, 0205, ...
    #  }

    'api1': {  # 스케쥴링 이름
        'task': 'main.tasks.api1_update',  # 수행할 task 설정
        'schedule': crontab(minute=41, hour='*'),  # 매 시각 41분마다 호출
    },
    'api2': {  # 스케쥴링 이름
        'task': 'main.tasks.api2',  # 수행할 task 설정
        'schedule': crontab(minute=50, hour='*'),  # 매 시각 50분마다 호출
    },
    'api3': {  # 스케쥴링 이름
        'task': 'main.tasks.api3',  # 수행할 task 설정
        'schedule': crontab(minute=15, hour='2,5,8,11,14,17,20,23'),  # 3시간 주기로 해당 시간 15분에 호출
    },
    'api4': {  # 스케쥴링 이름
        'task': 'main.tasks.api4',  # 수행할 task 설정
        'schedule': crontab(minute=1, hour='6,18'),  # 6시, 18시에 호출
    },
    'api5': {  # 스케쥴링 이름
        'task': 'main.tasks.api5',  # 수행할 task 설정
        'schedule': crontab(minute=4, hour='6,18'),  # 6시, 18시에 호출
    },

    'add-every-60-minutes-api6': {
        'task': 'main.tasks.api_6',
        'schedule': crontab(minute=0, hour='*'),

    },
    'add-every-24-hour-api7': {
        'task': 'main.tasks.api_7',
        'schedule': crontab(minute=0, hour=0), # 자정마다 호출

    },
    'add-every-at-06-api8': {
        'task': 'main.tasks.api_8',
        'schedule': crontab(minute=0, hour=6), # 6시 마다 호출
    },

    'add-every-at-06-18-api9': {
        'task': 'main.tasks.api_9',
        'schedule': crontab(minute=0, hour='6, 18'), # 6시, 18시에 호출
    },

} 