import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from comment.models import *
from main.models import *
import random
from datetime import datetime


## 오늘 코멘트 부분
# 1차 기준: 1시간 이내 확률 40% 이상의 강수예보시
# 2차 기준: 1시간 이내 확률 0 초과 40% 미만의 강수예보 시
# 3차 기준: 체감온도가 현재기온보다 높을 때
# 4차 기준: 자외선지수가 6이상 일 시
# 5차 기준(그 외): 하늘상태 기준 - 맑음 / 구름많음 / 흐림

# 아직 이 함수는 배포에는 적용하지 않겠습니다! 채영님까지 완성 후  + db 더미데이터 후에 적용하겠습니다
def today(region):
    current = datetime.now()
    h = int(current.strftime("%H"))
    api3 = Api3.objects.get(region=region)
    api2 = Api2.objects.get(region=region)

    # 2시간 내 강수 확률 확인
    p1 = int(((api3.serializable_value(f'info_{h}')).replace(" ", "")).split('/')[4])  # 현재 시 강수 확률
    p2 = int(((api3.serializable_value(f'info_{h+1}')).replace(" ", "")).split('/')[4])  # 현재 시 + 1 강수 확률

    if p1 >= 40 or p2 >= 40:  # 1차 기준
        queryset = list(Today.objects.filter(first_standard=1))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].commet

    elif 0 < p1 < 40 or 0 < p2 < 40:  # 2차 기준
        queryset = list(Today.objects.filter(first_standard=2))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].commet

    # elif (3차 기준):
    # elif (4차 기준):

    else:  # 5차 기준 (그 외) -> 현재 하늘상태로 판별
        sky = (((api2.serializable_value(f'info_{h}')).replace(" ", "")).split('/'))[1]  # 현재 하늘상태
        queryset = list(Today.objects.filter(first_standard=5).filter(second_standard=sky))
        comm = random.sample(queryset, 1)
        today_comment = comm[0].comment

    return today_comment



##
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
