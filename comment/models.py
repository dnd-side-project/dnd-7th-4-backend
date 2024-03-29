from django.db import models

# Create your models here.


PRECIPITATION_CHOICES = [
    ('1', '강수없음'),
    ('2', '약한 비'),
    ('3', '보통 비'),
    ('4', '강한 비'),
    ('5', '매우 강한 비'),
]

HUMIDITY_CHOICES = [
    ('1', '습함'),
    ('2', '쾌적'),
    ('3', '건조'),
]

WIND_CHOICES = [
    ('1', '4미만'),
    ('2', '4이상 ~ 9미만'),
    ('3', '9이상 ~ 14미만'),
    ('4', '14이상'),
]

SEASON_CHOICES = [
    ('1', '봄'),
    ('2', '여름'),
    ('3', '가을'),
    ('4', '겨울'),
]

FINEDUST_CHOICES = [
    ('1', '좋음'),
    ('2', '보통'),
    ('3', '나쁨'),
    ('4', '매우 나쁨')
]

WINDCHILL_CHOICES = [
    ('0', '이상 없음'),
    ('1', '여름철 관심'),
    ('2', '여름철 주의'),
    ('3', '여름철 경고'),
    ('4', '여름철 위험'),
    ('5', '겨울철 낮음'),
    ('6', '겨울철 보통'),
    ('7', '겨울철 추움'),
    ('8', '겨울철 주의'),
    ('9', '겨울철 위험')
]

# 강수 코멘트
class Precipitation(models.Model):
    comment = models.TextField()
    imageUrl = models.TextField()
    standard = models.CharField(max_length=50, choices=PRECIPITATION_CHOICES)

    def __str__(self):
        return self.comment  # comment 값을 대표값으로


# 습도 코멘트
class Humidity(models.Model):
    comment = models.TextField()
    imageUrl = models.TextField()
    standard = models.CharField(max_length=50, choices=HUMIDITY_CHOICES)

    def __str__(self):
        return self.comment  # comment 값을 대표값으로


# 바람 코멘트
class Wind(models.Model):
    comment = models.TextField()
    imageUrl = models.TextField()
    standard = models.CharField(max_length=50, choices=WIND_CHOICES)

    def __str__(self):
        return self.comment  # comment 값을 대표값으로

# 미세먼지 코멘트
class Finedust(models.Model):
    comment = models.TextField()
    imageUrl = models.TextField()
    standard = models.CharField(max_length=50, choices=FINEDUST_CHOICES)

    def __str__(self):
        return self.comment  # comment 값을 대표값으로

# 체감온도 코멘트
class Windchill(models.Model):
    comment = models.TextField()
    imageUrl = models.TextField()
    standard = models.CharField(max_length=50, choices=WINDCHILL_CHOICES)

    def __str__(self):
        return self.comment  # comment 값을 대표값으로

# 오늘 코멘트
class Today(models.Model):
    comment = models.TextField()
    first_standard = models.IntegerField()  # 1차기준 ~ n차 기준
    second_standard = models.CharField(max_length=50, null=True, default='')  # 해당 기준에서 세부 기준
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)

    def __str__(self):
        return self.comment  # comment 값을 대표값으로