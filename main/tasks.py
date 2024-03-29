from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from .models import *
from dnd_7th_4_backend.settings.base import env
from datetime import date, datetime
from dnd_7th_4_backend.celery import app
from main.api_callback_directory.api_1 import func1, func1_update
from main.api_callback_directory.api_2 import func2
from main.api_callback_directory.api_3 import func3
from main.api_callback_directory.api_4 import func4
from main.api_callback_directory.api_5 import func5

from main.api_callback_directory.api_6 import call_api_6, update_api_6
from main.api_callback_directory.api_7 import call_api_7, update_api_7
from main.api_callback_directory.api_8 import call_api_8, update_api_8
from main.api_callback_directory.api_9 import call_api_9, update_api_9
from main.kakaoalarm_callback_directory.summer_kakao_alarm import send_kakao_alarm
from main.models import Region, Api6, Api7, Api8, Api9


# test 용 함수
@shared_task
def printName():
    print("Testtime: ", datetime.now())


# api1 처음 호출 시 필요한 함수 -> create
@shared_task
def api1_create():
    func1()

# api1 재호출 시 필요한 함수 -> update
@shared_task
def api1_update():
    func1_update()


# api2
@shared_task
def api2():
    func2()


# api3
@shared_task
def api3():
    func3()


# api4
@shared_task
def api4():
    func4()


# api5
@shared_task
def api5():
    func5()


@shared_task
def api_6():
    if not len(Api6.objects.all()): # Api_6 가 비어있는 경우
        print('api_6: save -----------------------------')
        call_api_6()
    else:
        print('api_6: update -----------------------------')
        update_api_6()

@shared_task
def api_7():
    if not len(Api7.objects.all()): # api_7 가 비어있는 경우
        print('api_7: save -----------------------------')
        call_api_7()

    else:
        print('api_7: update -----------------------------')
        update_api_7()

@shared_task
def api_8():
    if not len(Api8.objects.all()): # api_8 가 비어있는 경우
        print('api_8: save -----------------------------')
        call_api_8()

    else:
        print('api_8: update -----------------------------')
        update_api_8()

@shared_task
def api_9():
    if not len(Api9.objects.all()): # api_9 가 비어있는 경우
        print('api_9: save -----------------------------')
        call_api_9()

    else:
        print('api_9: update -----------------------------')
        update_api_9()

@shared_task
def kakao_alarm():
    send_kakao_alarm()