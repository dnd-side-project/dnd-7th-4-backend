from rest_framework import serializers

from .models import *

# API6 오늘 데이터
class MainApi6TodaySerializer(serializers.ModelSerializer):
    미세먼지 = serializers.IntegerField(source="pm10Grade1h")
    초미세먼지 = serializers.IntegerField(source="pm25Grade1h")

    class Meta:
        model = Api6
        fields = ['미세먼지', '초미세먼지']

# API6 내일 데이터
class MainApi6TomorrowSerializer(serializers.ModelSerializer):
    미세먼지 = serializers.IntegerField(source="pm10Value24")
    초미세먼지 = serializers.IntegerField(source="pm10Value24")

    class Meta:
        model = Api6
        fields = ['미세먼지', '초미세먼지']

# API7 오늘 데이터
class MainApi7TodaySerializer(serializers.ModelSerializer):
    일출 = serializers.IntegerField(source="today_sunrise")
    일몰 = serializers.IntegerField(source="today_sunset")

    class Meta:
        model = Api7
        fields = ['일출', '일몰']

# API7 내일 데이터
class MainApi7TomorrowSerializer(serializers.ModelSerializer):
    일출 = serializers.IntegerField(source="tomorrow_sunrise")
    일몰 = serializers.IntegerField(source="tomorrow_sunset")

    class Meta:
        model = Api7
        fields = ['일출', '일몰']

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

# API9 오늘 데이터
class MainApi9TodaySerializer(serializers.ModelSerializer):
    apparent_tem = serializers.IntegerField(source="today")

    class Meta:
        model = Api8
        fields = ['apparent_tem']

# API9 내일 데이터
class MainApi9TomorrowSerializer(serializers.ModelSerializer):
    apparent_tem = serializers.IntegerField(source="tomorrow")

    class Meta:
        model = Api8
        fields = ['apparent_tem']

# API3
class Api3Serializer(serializers.ModelSerializer):

    class Meta:
        model = Api3
        fields = [field.name for field in Api3._meta.get_fields()]

# Region 데이터
class RegionSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'city', 'district']