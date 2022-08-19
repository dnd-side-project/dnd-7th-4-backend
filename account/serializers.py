from rest_framework import serializers

from .models import *

class ProfileKakaoAlarmSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'kakao_alarm']