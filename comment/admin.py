from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Today)
class TodayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Today._meta.get_fields()]


@admin.register(Precipitation)
class PrecipitationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Precipitation._meta.get_fields()]


@admin.register(Humidity)
class HumidityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Humidity._meta.get_fields()]


@admin.register(Wind)
class WindAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wind._meta.get_fields()]