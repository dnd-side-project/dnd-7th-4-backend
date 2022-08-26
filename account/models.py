from django.db import models
from django.contrib.auth.models import User
from main.models import Region, Base


# 유저 모델
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kakao_id = models.CharField(max_length=50)  # 카카오 id
    nickname = models.CharField(max_length=50)  # 카카오 닉네임
    profile_image = models.TextField(null=True, default='')  # 카카오 프로필 이미지
    kakao_alarm = models.BooleanField(default=0)  # 카카오 알람
    kakao_region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, default='') # 카카오 알림 지역
    phone_number = models.CharField(max_length=50, null=True)  # 카카오 핸드폰 번호

    def __str__(self):
        return self.nickname  # 닉네임 값을 대표값으로 설정


# 유저-행정구역 중개모델
class User_Region(Base):
    #FK
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, default='')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, default='')

    def __str__(self):
        return f'{self.user.nickname} - {self.region.city} {self.region.district}'