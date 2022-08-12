from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'country', 'div_code', 'city', 'district']
    ordering = ('id',)


@admin.register(Api1)
class Api1Admin(admin.ModelAdmin):
    list_display = [field.name for field in Api1._meta.get_fields()]

@admin.register(Api_6)
class Api6Admin(admin.ModelAdmin):
    #list_display = [field.name for field in Api_6._meta.get_fields()]
    list_display = ('id', 'created_at', 'updated_at', 'sidoName', 'stationName', 'pm10Grade1h', 'pm25Grade1h', 'pm10Value24', 'pm25Value24')

@admin.register(Api_7)
class RegionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Api_7._meta.get_fields()]


@admin.register(Api2)
class Api2Admin(admin.ModelAdmin):
    list_display = [field.name for field in Api2._meta.get_fields()]