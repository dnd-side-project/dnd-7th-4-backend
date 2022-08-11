from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from .models import *
from dnd_7th_4_backend.settings.base import env
from datetime import date, datetime
from dnd_7th_4_backend.celery import app
from main.api_callback_directory.api_1 import func1, func2

from main.api_callback_directory.api_6 import call_api_6, update_api_6
from main.api_callback_directory.api_7 import call_api_7, update_api_7
from main.api_callback_directory.api_8 import call_api_8, update_api_8
from main.api_callback_directory.api_9 import call_api_9, update_api_9
from main.models import Region, Api_6, Api_7, Api8, Api9


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
    func2()


@shared_task
def api_6():
    if not len(Api_6.objects.all()): # Api_6 가 비어있는 경우
        print('api_6: save -----------------------------')
        call_api_6()
    else:
        print('api_6: update -----------------------------')
        update_api_6()

@shared_task
def api_7():
    if not len(Api_7.objects.all()): # api_7 가 비어있는 경우
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