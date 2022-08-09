from __future__ import absolute_import, unicode_literals
from celery import shared_task

from dnd_7th_4_backend.celery import app

from api_callback_directory.api_6 import api_6

@shared_task
def printName(name):
    print(f'my name is {name}')
