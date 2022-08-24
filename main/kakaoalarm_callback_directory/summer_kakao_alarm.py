import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse

import random
from time import time
from datetime import datetime
from collections import defaultdict

from account.models import *
from main.models import *
from dnd_7th_4_backend.settings.base import env


# 날씨 상태에 따른 템플릿 정보
TRUE_PRECIPITATION_TEMPLEATE_INFO = {
    '맑음': ['sunny_1', 'sunny_2', 'sunny_3'],
    '구름많음' : ['mostly_cloudy_1', 'mostly_cloudy_2', 'mostly_cloudy_3'],
    '흐림' : ['cloudy_1', 'cloudy_2', 'cloudy_3']
}

FALSE_PRECIPITATION_TEMPLEATE_INFO = {
    '맑음': ['sunny_1', 'sunny_2', 'sunny_3'],
    '구름많음' : ['mostly_cloudy_1', 'mostly_cloudy_2', 'mostly_cloudy_3'],
    '흐림' : ['cloudy_1', 'cloudy_2', 'cloudy_3']
}

CURRENT = datetime.now()

# 카카오톡 알림을 보내는 
def send_kakao_alarm(requests):
    people = Profile.objects.filter(kakao_alarm = True)
    
    # 날씨 기준으로 사용자 나누기
    user_data = defaultdict(list) # {(하늘상태, 강수유무): [profile 객체, 오전강수확률, 오후강수확률, 최고기온, 최저기온], }
    for p in people:
        # 알림을 받을 지역이나 핸드폰 번호가 저장되어 있지 않는 경우
        if not p.kakao_region or not p.phone_number: 
           continue 

        region = p.kakao_region
        morinig_precpitation, afternoon_precpitation, max_tem, min_tem, sky_status, is_precpitation = get_alarm_info(region)
        user_data[(sky_status, is_precpitation)].append((p, morinig_precpitation, afternoon_precpitation, max_tem, min_tem))
        
    """
    # 알림톡 내용 구성하기
    url = "https://sens.apigw.ntruss.com/alimtalk/v2/services/"+env('KAKAO_serviceId')+"/messages"
    for weather, user_info in user_data.items():
        ## 요청 데이터 생성하기
        ### 헤더 생성하기
        header = {}
        header['Content-Type'] = 'application/json; charset=utf-8'
        header['x-ncp-apigw-timestamp'] = time()
        header['x-ncp-iam-access-key'] = env('KAKAO_Sub_Account_Access_Key')
        header['x-ncp-apigw-signature-v2'] = env('KAKAO_API_Gateway_Signature')

        ### 바디 생성하기
        body = {}
        body['plusFriendId'] = env('KAKAO_plusFriendId')
        body['templateCode'] = random.sample(TEMPLEATE_INFO[weather], 1)
        body['reserveTime'] = datetime.today().strftime("%Y-%m-%d 08:00") # 지금은 현재로!!
        body['reserveTimeZone'] = 'Asia/Seoul'
        body['messages'] = []
        cnt = 1
        while user_info:
            user = user_info.pop()
            region = user[0].kakao_alarm_region
            body_messages_data = {}
            body_messages_data['countryCode'] = '82'
            body_messages_data['to'] = user[0].phone_number
            body_messages_data['content'] = f'최고기온, 최저기온 {user[1]}/{user[2]}'
            
            
            #### 링크
            body_buttons = {}
            body_buttons['type'] = 'WL'
            body_buttons['name'] = '자세한 내용을 확인하러 가기'
            body_buttons['linkMobile'] = f'http://localhost:8000/main?city={region.city}&district={region.distinct}'
            body_buttons['linkPc'] = f'http://localhost:8000/main?city={region.city}&district={region.distinct}'
            body_messages_data['buttons'] = body_buttons

            body['messages'].append(body_messages_data)
        try:
            cnt += 1
            # 100명이 되었을 경우
            if cnt >= 100 or not user_info:
                cnt = 1
                response = requests.post(url = url, headers = header, data = body)
                pring(f'resopnse kakao alalrm {response.text} ----------------------')

        except requests.Timeout:
            print(f'resopnse kakao alalrm: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'resopnse kakao alalrm: ConnectionError: {local}-----------------------------')
    """
    return HttpResponse("kakao alarm test  -----------------------------")

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

    return int(POP0_am), int(POP0_pm)  # 오전, 오후 강수 확률 반환