from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'kakao_alarm', 'kakao_region']


@admin.register(User_Region)
class User_RegionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User_Region._meta.get_fields()]