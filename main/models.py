from django.db import models

# Create your models here.

# API6 -시도별 실시간 측정정보
class Api_6(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sidoName = models.CharField(max_length=2) # 시도명
    stationName = models.CharField(max_length=10) # 측정소명

    pm10Grade1h = models.IntegerField() # 미세먼지 등급
    pm25Grade1h = models.IntegerField() # 고농도 미세먼지 등급
    
    pm10Value24 = models.IntegerField() # 미세먼지 24시간 예측 등급
    pm25Value24 = models.IntegerField() # 고농도 24시간 예측 미세먼지 등급

    def __str__(self):
        return (self.sidoName, self.stationName)

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
    api6_code = models.CharField(max_length=20)  # 시도별 실시간 측정정보 api code
    api6_station = models.CharField(max_length=20, null=True, default='') # 측정소 데이터
    api10_code = models.IntegerField()  # 종관관측예보 api code

    # FK
    api6_id = models.ForeignKey(Api_6, on_delete=models.CASCADE,null=True, default='')

    def __str__(self):
        return self.div_code  # 행정 구역 코드값을 대표값으로