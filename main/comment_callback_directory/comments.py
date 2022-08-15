import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from comment.models import *
from main.models import *
import random
from datetime import datetime

current = datetime.now()

## 오늘 코멘트 부분
# 1차 기준: 1시간 이내 확률 40% 이상의 강수예보시
# 2차 기준: 1시간 이내 확률 0 초과 40% 미만의 강수예보 시
# 3차 기준: 체감온도가 현재기온보다 높을 때
# 4차 기준: 자외선지수가 6이상 일 시
# 5차 기준(그 외): 하늘상태 기준 - 맑음 / 구름많음 / 흐림

# 아직 이 함수는 배포에는 적용하지 않겠습니다! 채영님까지 완성 후  + db 더미데이터 후에 적용하겠습니다
def today(region, windchill):
    h = int(current.strftime("%H"))
    api2 = Api2.objects.get(region=region)
    api3 = Api3.objects.get(region=region)
    api8 = Api8.objects.get(div_code = region.div_code)

    # 2시간 내 강수 확률 확인
    p1 = int(((api3.serializable_value(f'info_{h}')).replace(" ", "")).split('/')[4])  # 현재 시 강수 확률
    p2 = int(((api3.serializable_value(f'info_{h+1}')).replace(" ", "")).split('/')[4])  # 현재 시 + 1 강수 확률
    p3_1 = region.api1.T1H # 현재 기온
    p3_2 = windchill # 체감온도
    p4 = api8.today

    if p1 >= 40 or p2 >= 40:  # 1차 기준
        queryset = list(Today.objects.filter(first_standard=1))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].commet

    elif 0 < p1 < 40 or 0 < p2 < 40:  # 2차 기준
        queryset = list(Today.objects.filter(first_standard=2))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].commet
    
    elif p3_2 > p3_1: # 3차 기준
        queryset = list(Today.objects.filter(first_standard=3))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].commet
    
    elif p4 >= 6:
        queryset = list(Today.objects.filter(first_standard=4))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].commet

    else:  # 5차 기준 (그 외) -> 현재 하늘상태로 판별
        sky = (((api2.serializable_value(f'info_{h}')).replace(" ", "")).split('/'))[1]  # 현재 하늘상태
        queryset = list(Today.objects.filter(first_standard=5).filter(second_standard=sky))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].comment

    return today_comment


## 세부 코멘트 부분 -> 딕셔너리 형태로 반환
def humidity(self):  # 습도
    hud = float(self)
    if hud >= 70:
        stand = 1
    elif 40 <= hud < 70:
        stand = 2
    else:
        stand = 3

    queryset = list(Humidity.objects.filter(standard=stand))
    comm = random.sample(queryset, 1)
    d = {"코멘트": comm[0].comment, "이미지 url": comm[0].imageUrl}
    return d


def precipication(self):  # 강수
    prec = str(self)
    if prec == "강수없음":  # "강수없음" 문자열일때 예외처리
        stand = 1

    else:
        prec = int(prec.replace("mm", ""))  # 단위 없애기
        if prec < 3:
            stand = 2
        elif 3 <= prec < 15:
            stand = 3
        elif 15 <= prec < 30:
            stand = 4
        else:
            stand = 5

    queryset = list(Precipitation.objects.filter(standard=stand))
    comm = random.sample(queryset, 1)
    d = {"코멘트": comm[0].comment, "이미지 url": comm[0].imageUrl}
    return d


def wind(self):  # 바람
    wi = float(self)
    if wi < 4:
        stand = 1
    elif 4 <= wi < 9:
        stand = 2
    elif 9 <= wi < 14:
        stand = 3
    else:
        stand = 4

    queryset = list(Wind.objects.filter(standard=stand))
    comm = random.sample(queryset, 1)
    d = {"코멘트": comm[0].comment, "이미지 url": comm[0].imageUrl}
    return d


def finedust(fd): # 미세먼지
    standard = 0
    if fd == 29 or fd == 2:
        standard = 1
    elif fd == 2:
        standard = 2
    else:
        standard = 3
    queryset = list(Finedust.objects.filter(standard=standard))
    comm = random.sample(queryset, 1)
    data = {"코멘트": comm[0].comment, "이미지 url": comm[0].imageUrl}
    return data

def windchill(wd): # 체감온도
    wd = float(wd)
    standard = 0
    if 29 <= wd < 31:
        standard = 1
    elif 31 <= wd < 34:
        standard = 2
    elif 34 <= wd < 37:
        standard = 3
    elif wd > 37 :
        standard = 4
    elif -10 < wd <= 10:
        standard = 5
    elif -25 < wd <= -10:
        standard = 6
    elif -45 < wd <= -25:
        standard = 7
    elif -59 <= wd <= -45:
        standard = 8
    elif wd <= -60:
        standard = 9
    queryset = list(Windchill.objects.filter(standard=standard))
    comm = random.sample(queryset, 1)
    data = {"코멘트": comm[0].comment, "이미지 url": comm[0].imageUrl}
    return data

def sun(state, sunrise, sunset):
    sunrise = (str(sunrise)[0], str(sunrise)[1:])
    sunset = (str(sunset)[0], str(sunset)[1:])

    now_hour = int(current.strftime("%H"))
    now_minute = int(current.strftime("%M"))

    if int(sunset[0]) >= now_hour and int(sunset[1]) >= now_minute:
        hour, minute = cal_time(state, int(sunrise[0])-now_hour, int(sunrise[1])-now_minute)
        return {"코멘트": f'일출까지/{hour}시간 {minute}분', "이미지 url": "일몰 일출 이미지"}
    elif int(sunrise[0]) >= now_hour and int(sunrise[1]) >= now_minute:
        hour, minute = cal_time(int(state, sunset[0])-now_hour, int(sunset[1])-now_minute)
        return {"코멘트": f'일몰까지/{hour}시간 {minute}분', "이미지 url": "일몰 일출 이미지"}
    else:
        hour, minute = cal_time(int(state, sunrise[0])-now_hour, int(sunrise[1])-now_minute)
        return {"코멘트": f'일출까지/{hour}시간 {minute}분', "이미지 url": "일몰 일출 이미지"}

def cal_time(state, hour, minute):
    if minute < 0:
        hour -= 1
        minute += 60

    if hour < 0:
        hour += 12
    
    if state: # 내일에 대한 코멘트인 경우
        hour += 24
    return hour, minute

    
