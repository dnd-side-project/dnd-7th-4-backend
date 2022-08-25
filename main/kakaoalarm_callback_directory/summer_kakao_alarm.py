import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from django.shortcuts import render, get_list_or_404

from django.http import HttpResponse

import json
import hmac
import base64
import random
import hashlib
import requests
from time import time
from datetime import datetime
from collections import defaultdict

from account.models import *
from main.models import *
from dnd_7th_4_backend.settings.base import env


# 날씨 상태에 따른 템플릿 정보
TRUE_PRECIPITATION_TEMPLATE_INFO = {
    '맑음': ['SUOSunny1', 'SUOSunny2'],
    '구름많음' : ['SUOMostly1', 'SUOMostly2'], # CHECK
    '흐림' : ['cloudyT1'] # TODO
}

FALSE_PRECIPITATION_TEMPLATE_INFO = {
    '맑음': ['sunnyTest1'],
    '구름많음' : ['MCloudyT1'],
    '흐림' : ['XcloudyT1']
}

CURRENT = datetime.now()


# 카카오톡 알림을 보내는 
def send_kakao_alarm(request):
    reset_variable()
    people = Profile.objects.filter(kakao_alarm = True)
    data = {}
    
    # 날씨 기준으로 사용자 나누기
    user_data = defaultdict(list) # {(하늘상태, 강수유무): [profile 객체, 오전강수확률, 오후강수확률, 최고기온, 최저기온], }
    for p in people:
        # 알림을 받을 지역이나 핸드폰 번호가 저장되어 있지 않는 경우
        if not p.kakao_region or not p.phone_number or p.phone_number[:3] != "+82" and p.kakao_id == 2400917243: 
           continue 

        region = p.kakao_region
        morinig_precpitation, afternoon_precpitation, max_tem, min_tem, sky_status, is_precpitation = get_alarm_info(region)
        user_data[(sky_status, is_precpitation)].append((p, str(morinig_precpitation), str(afternoon_precpitation), str(max_tem), str(min_tem)))

    # 알림톡 내용 구성하기 
    ## 헤더 생성하기
    timestamp = str(int(time() * 1000))
    header = {}
    header['Content-Type'] = 'application/json; charset=utf-8'
    header['x-ncp-apigw-timestamp'] = timestamp
    header['x-ncp-iam-access-key'] = env('KAKAO_Sub_Account_Access_Key')
    header['x-ncp-apigw-signature-v2'] = make_signature(timestamp)

    url = "https://sens.apigw.ntruss.com/alimtalk/v2/services/"+env('KAKAO_serviceId')+"/messages"
    for key_data, user_info in user_data.items():
        print(user_info)

        ## 템플릿 설정하기
        template = FALSE_PRECIPITATION_TEMPLATE_INFO[key_data[0]]
        if key_data[1]:
            template = TRUE_PRECIPITATION_TEMPLATE_INFO[key_data[0]]

        ## 바디 생성하기
        data = {}
        data['plusFriendId'] = "@한줄날씨"
        data['templateCode'] = random.sample(template, 1)[0]
        data['reserveTime'] = datetime.today().strftime("%Y-%m-%d 16:17")
        data['reserveTimeZone'] = "Asia/Seoul"
        data['messages'] = []
        cnt = 1
   
        while user_info:
            ### 데이터 가져오기
            user, morinig_precpitation, afternoon_precpitation, max_tem, min_tem = user_info.pop()
            region = user.kakao_region

            ### 알림톡 내용 넣기 
            body_messages_data = {}
            body_messages_data['countryCode'] = "82"
            body_messages_data['to'] = '0'+user.phone_number[4:].replace('-', '')
            body_messages_data['content'] = "오전 최대 강수 확률이 #{" + morinig_precpitation + "}% 이고, 오후 최대 강수 확률이 #{" + afternoon_precpitation + "}%/n최고 기온 #{" + max_tem + "}도, 최저 기온 {#{" + min_tem+ "}도"

            #### 링크
            body_buttons = {}
            body_buttons['type'] = "WL"
            body_buttons['name'] = "자세히"
            body_buttons['linkMobile'] = "https://www.weathercomment.com/"
            body_buttons['linkPc'] = "https://www.weathercomment.com/"
            body_messages_data['buttons'] = [body_buttons]

            data['messages'].append(body_messages_data)

        try:
            cnt += 1
            # 100명이 되었을 경우
            if cnt >= 100 or not user_info:
                cnt = 1
                response = requests.post(url = url, headers = header, data = json.dumps(data))
                print(f'resopnse kakao alalrm {response.text} ----------------------')

        except requests.Timeout:
            print(f'resopnse kakao alalrm: Timeout: {user} alarm -----------------------------')
        except requests.ConnectionError:
            print(f'resopnse kakao alalrm: ConnectionError: {user} alarm -----------------------------')

    return HttpResponse(data)

# x-ncp-apigw-signature-v2 헤더의 값을 생성하는 함수
def	make_signature(timestamp):
    access_key = env('KAKAO_Sub_Account_Access_Key')
    secret_key = env('KAKAO_API_Gateway_Signature')
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    uri = "/alimtalk/v2/services/"+env('KAKAO_serviceId')+"/messages"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

# 변수들 현재 시간 기준으로 리 세팅하는 함수
def reset_variable():
    global CURRENT
    CURRENT = datetime.now()

# 알람에 필요한 정보를 가져오는 함수
def get_alarm_info(region):
    h = int(CURRENT.strftime("%H"))

    # 데이터 불러오기
    api2 = Api2.objects.get(region=region)
    api3 = Api3.objects.get(region=region)

    # 하단 코멘트 데이터
    ## 강수 예보 확률
    morning_precpitation, afternoon_precpitation = precipitation_probability(api3)

    ## 최고/최저 기온
    max_tem = api3.info_day0_MAX  # 오늘 최고기온
    min_tem = api3.info_day0_MIN  # 오늘 최저기온

    # 썸네일 데이터 REVIEW
    ## 하늘상태
    field = f'info_{h}'
    str = (api2.serializable_value(field)).replace(" ", "")  # 나중엔 없앨 공백 제거 코드
    f_list = str.split('/')
    sky_status = f_list[1]  # 현재 하늘 상태

    ## 강수
    is_precpitation = False
    if morning_precpitation > 40 or afternoon_precpitation > 40:
        is_precpitation = True
    return morning_precpitation, afternoon_precpitation, max_tem, min_tem, sky_status, is_precpitation


# Region 객체 전달 시, 해당 지역의 당일 (오전 강수확률), (오후 강수확률) 반환하는 함수
def precipitation_probability(api3):
    # region = Region.objects.get(id=2)  ## 임의 테스트코드

    # 오전/오후별 : 강수확률
    pop0 = []

    for i in range(6, 12):  # 오전
        li = ((api3.serializable_value(f'info_{i}')).replace(" ", "")).split('/')
        pop0.append(li[4])

    POP0_am = max(pop0)  # 오전 강수확률
    pop0.clear()

    for i in range(12, 22):  # 오후
        li = ((api3.serializable_value(f'info_{i}')).replace(" ", "")).split('/')
        pop0.append(li[4])

    POP0_pm = max(pop0)  # 오후 강수확률

    return float(POP0_am), float(POP0_pm)  # 오전, 오후 강수 확률 반환