from rest_framework import serializers

from .models import *

class ProfileKakaoAlarmSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'kakao_alarm']



# 유저 - 지역 중개 모델
class UserRegionSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    def get_city(self, obj):
        return obj.region.city

    def get_district(self, obj):
        return obj.region.district

    class Meta:
        model = User_Region
        fields = ['region']