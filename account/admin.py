from django.contrib import admin
from .models import *

admin.site.register(Profile)


@admin.register(User_Region)
class Api1Admin(admin.ModelAdmin):
    list_display = [field.name for field in User_Region._meta.get_fields()]