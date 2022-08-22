import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from comment.models import *
from main.models import *
import random
from datetime import datetime

current = datetime.now()

prec_dic = {
    "맑음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%EB%A7%91%EC%9D%8C.png",
    "구름많음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%EA%B5%AC%EB%A6%84%EB%A7%8E%EC%9D%8C.png",
    "흐림": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%ED%9D%90%EB%A6%BC.png",

    "약한비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%EC%95%BD%ED%95%9C%EB%B9%84.png",
    "보통비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%EB%B3%B4%ED%86%B5%EB%B9%84.png",
    "강한비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%EA%B0%95%ED%95%9C%EB%B9%84.png",
    "매우강한비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EA%B0%95%EC%88%98%EB%9F%89/%EB%A7%A4%EC%9A%B0%EA%B0%95%ED%95%9C%EB%B9%84.png"
}

# 시간대별 이미지
time_dic = {
    "맑음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8B%9C%EA%B0%84%EB%8C%80%EB%B3%84+%EB%82%A0%EC%94%A8/%EB%A7%91%EC%9D%8C.png",
    "구름많음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8B%9C%EA%B0%84%EB%8C%80%EB%B3%84+%EB%82%A0%EC%94%A8/%EA%B5%AC%EB%A6%84%EB%A7%8E%EC%9D%8C.png",
    "흐림": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8B%9C%EA%B0%84%EB%8C%80%EB%B3%84+%EB%82%A0%EC%94%A8/%ED%9D%90%EB%A6%BC.png",
    "비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8B%9C%EA%B0%84%EB%8C%80%EB%B3%84+%EB%82%A0%EC%94%A8/%EB%B9%84.png"
}

# 이번주날씨 이미지
weekend_dic = {
    "맑음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%A7%91%EC%9D%8C.png",
    "구름많음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EA%B5%AC%EB%A6%84%EB%A7%8E%EC%9D%8C.png",
    "구름많고 비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "구름많고 눈": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "구름많고 비/눈": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "구름많고 소나기": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "흐림": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%ED%9D%90%EB%A6%BC.png",
    "흐리고 비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "흐리고 눈": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "흐리고 비/눈": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "흐리고 소나기": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png",
    "소나기": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%9D%B4%EB%B2%88%EC%A3%BC+%EB%82%A0%EC%94%A8/%EB%B9%84.png"
}


# 습도 이미지 -> 습함, 쾌적, 건조
def humidity_img(self):
    humidity = float(self)  # 습도
    if humidity >= 70:  # 습함 (70 이상)
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8A%B5%EB%8F%84/%EC%8A%B5%ED%95%A8.png"
    elif 40 <= humidity < 70:  # 쾌적 (40이상 70미만)
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8A%B5%EB%8F%84/%EC%BE%8C%EC%A0%81.png"
    else:  # 건조 (40미만)
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EC%8A%B5%EB%8F%84/%EA%B1%B4%EC%A1%B0.png"

    return img_url


# 바람 이미지 -> 4단계
def wind_img(self):
    wind = float(self)  # 풍속
    if wind < 4:
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EB%B0%94%EB%9E%8C/4%EB%AF%B8%EB%A7%8C.png"
    elif 4 <= wind < 9:
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EB%B0%94%EB%9E%8C/4~9.png"
    elif 9 <= wind < 14:
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EB%B0%94%EB%9E%8C/9~14.png"
    else:  # 14이상
        img_url = "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%95%84%EC%9D%B4%EC%BD%98/%EB%B0%94%EB%9E%8C/14%EC%9D%B4%EC%83%81.png"

    return img_url


# 강수 이미지 -> 강수없음(맑음, 구름많음, 흐림) / 강수있음(약한비, 보통비, 강한비, 매우강한비)
def precipication_img(sky, pty, rn1):  # sky: 하늘상태, pty: 강수형태, rn1: 1시간강수량
    if pty == "없음":  # 강수없음인 경우 -> 맑음, 구름많음, 흐림
        img_url = prec_dic[sky]
    else:  # 강수있음인 경우 -> 약한비, 보통비, 강한비, 매우강한비
        rn1 = float(rn1)  # data-type 맞추기
        if rn1 >= 30:
            img_url = prec_dic["매우강한비"]
        elif rn1 >= 15:
            img_url = prec_dic["강한비"]
        elif 3 <= rn1 < 15:
            img_url = prec_dic["보통비"]
        else:
            img_url = prec_dic["약한비"]

    return img_url


# 시간대별 이미지
def time_img(pty, sky):  # pty: 강수형태, sky: 하늘상태
    if pty == "없음":  # 강수없음 -> 맑음, 구름많음, 흐림
        img_url = time_dic[sky]
    else:  # 강수있음 -> 비 (여름만 고려)
        img_url = time_dic["비"]

    return img_url


# 이번주 날씨 이미지
def weekend_img(sky):
    return weekend_dic[sky]
