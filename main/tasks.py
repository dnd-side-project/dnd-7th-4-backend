from __future__ import absolute_import, unicode_literals
from celery import shared_task

from dnd_7th_4_backend.celery import app

from main.api_callback_directory.api_6 import call_api_6, update_api_6
from main.api_callback_directory.api_7 import call_api_7, update_api_7
from main.models import Api_6, Api_7, Region

@shared_task
def printName():
    print('my name is ')

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