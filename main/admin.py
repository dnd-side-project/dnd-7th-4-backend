from django.contrib import admin
from .models import Region, Api_6

# Register your models here.


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Region._meta.get_fields()]

@admin.register(Api_6)
class Api6Admin(admin.ModelAdmin):
    #list_display = [field.name for field in Api_6._meta.get_fields()]
    list_display = ('id', 'created_at', 'updated_at', 'sidoName', 'stationName', 'pm10Grade1h', 'pm25Grade1h', 'pm10Value24', 'pm25Value24')