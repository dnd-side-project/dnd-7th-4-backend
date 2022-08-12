from rest_framework import serializers

from .models import *

# API6 오늘 데이터
class MainApi6TodaySerializer(serializers.ModelSerializer):
    pm10 = serializers.IntegerField(source="pm10Grade1h")
    pm25 = serializers.IntegerField(source="pm25Grade1h")

    class Meta:
        model = Api6
        fields = ['pm10', 'pm25']

# API6 내일 데이터
class MainApi6TomorrowSerializer(serializers.ModelSerializer):
    pm10 = serializers.IntegerField(source="pm10Value24")
    pm25 = serializers.IntegerField(source="pm10Value24")

    class Meta:
        model = Api6
        fields = ['pm10', 'pm25']

# API7 오늘 데이터
class MainApi7TodaySerializer(serializers.ModelSerializer):
    sunrise = serializers.IntegerField(source="today_sunrise")
    sunset = serializers.IntegerField(source="today_sunset")

    class Meta:
        model = Api7
        fields = ['sunrise', 'sunset']

# API7 내일 데이터
class MainApi7TomorrowSerializer(serializers.ModelSerializer):
    sunrise = serializers.IntegerField(source="tomorrow_sunrise")
    sunset = serializers.IntegerField(source="tomorrow_sunset")

    class Meta:
        model = Api7
        fields = ['sunrise', 'sunset']

# API8 오늘 데이터
class MainApi8TodaySerializer(serializers.ModelSerializer):
    ultraviolet = serializers.IntegerField(source="today")

    class Meta:
        model = Api8
        fields = ['ultraviolet']

# API8 내일 데이터
class MainApi8TomorrowSerializer(serializers.ModelSerializer):
    ultraviolet = serializers.IntegerField(source="tomorrow")

    class Meta:
        model = Api8
        fields = ['ultraviolet']