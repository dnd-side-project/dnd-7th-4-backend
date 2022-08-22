from django.shortcuts import render, get_list_or_404

import random
from time import time
from datetime import datetime

from account.models import *
from main.models import Region
from dnd_7th_4_backend.settings.base import env


# 날씨 상태에 따른 템플릿 정보
TEMPLEATE_INFO = {
    '맑음': ['sunny_1', 'sunny_2', 'sunny_3'],
    '구름많음' : ['mostly_cloudy_1', 'mostly_cloudy_2', 'mostly_cloudy_3'],
    '흐림' : ['cloudy_1', 'cloudy_2', 'cloudy_3']
}

current = datetime.now()

# 카카오톡 알림을 보내는 
def send_kakao_alarm():
    people = get_list_or_404(Profile, kakao_alarm =True)
    url = "https://sens.apigw.ntruss.com/alimtalk/v2/services/"+env('KAKAO_serviceId')+"/messages"

    # 날씨 기준으로 사용자 나누기
    user_data = {'맑음' : [], '구름많음': [], '흐림': []}
    for p in people:
        region = p.kakao_region
        weather, max_tem, min_tem = get_alarm_info(region)
        user_data[weather].append((p, max_tem, min_tem))
    
    for weather, user_info in user_data.items():

        # 요청 데이터 생성하기
        ## 헤더 생성하기
        header = {}
        header['Content-Type'] = 'application/json; charset=utf-8'
        header['x-ncp-apigw-timestamp'] = time()
        header['x-ncp-iam-access-key'] = env('KAKAO_Sub_Account_Access_Key')
        header['x-ncp-apigw-signature-v2'] = env('KAKAO_API_Gateway_Signature')

        ## 바디 생성하기
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
            
            
            ### 링크
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
    


# 알람에 필요한 정보를 가져오는 함수
def get_alarm_info(region):
    hour = int(current.strftime("%H"))

    # API 객체 가져오기
    api3 = Api3.objects.get(region=region)
    
    # 하단 코멘트 데이터
    ## 강수 예보 확률
    ### 오전
    morning = 0
    for i in range(h, h+6):
        field = f'info_{i}'
        data = (api3.serializable_value(field)).replace(" ", "").split('/')[4]
        morning = max(data, morning)
    
    ### 오후
    afternoon
    for i in range(h+6, h+18):
        field = f'info_{i}'
        data = (api3.serializable_value(field)).replace(" ", "").split('/')[4]
        afternoon = max(data, afternoon)
