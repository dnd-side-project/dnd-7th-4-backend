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