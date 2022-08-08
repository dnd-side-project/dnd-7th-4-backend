from django.db import models

# Create your models here.


#  행정구역
class Region(models.Model):
    country = models.CharField(max_length=10)  # 나라
    div_code = models.CharField(max_length=10)  # 행정구역 코드
    city = models.CharField(max_length=20)  # 시, 도 (1단계)
    district = models.CharField(max_length=20)  # 군, 구  (2단계)

    cor_x = models.IntegerField()  # x좌표
    cor_y = models.IntegerField()  # y좌표

    lon_h = models.IntegerField()  # 경도(시)
    lon_m = models.IntegerField()  # 경도(분)
    lon_s = models.FloatField()  # 경도(초)

    lat_h = models.IntegerField()  # 위도(시)
    lat_m = models.IntegerField()  # 위도(분)
    lat_s = models.FloatField()  # 위도(초)

    longitude = models.FloatField()  # 경도(초/100)
    latitude = models.FloatField()  # 위도(초/100)

    api4_code = models.CharField(max_length=20)  # 중기육상예보 api code
    api5_code = models.CharField(max_length=20)  # 중기기온예보 api code
    api6_code = models.CharField(max_length=20)  # 대기오염정보 api code
    api10_code = models.IntegerField()  # 종관관측예보 api code

    def __str__(self):
        return self.div_code  # 행정 구역 코드값을 대표값으로