from django.db import models
from django.contrib.auth.models import User


# 유저 모델
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kakao_id = models.CharField(max_length=50)  # 카카오 id
    nickname = models.CharField(max_length=50)  # 카카오 닉네임
    profile_image = models.TextField(null=True, default='')  # 카카오 프로필 이미지
    kakao_alarm = models.BooleanField(default=0)  # 카카오 알람

    def __str__(self):
        return self.nickname  # 닉네임 값을 대표값으로 설정

