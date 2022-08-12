from rest_framework import serializers

from .models import *

# API6 오늘 데이터
class MainApi6TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Api6
        fields = ['pm10Grade1h', 'pm25Grade1h']

# API6 오늘 데이터
class MainApi6TomorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api6
        fields = ['pm10Value24', 'pm25Value24']
