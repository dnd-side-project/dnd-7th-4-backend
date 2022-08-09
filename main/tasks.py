from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from .models import *
from dnd_7th_4_backend.settings.base import env
from datetime import date, datetime
from dnd_7th_4_backend.celery import app
from api_callback_directory.api_1 import func1, func2


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