from django.http import HttpResponse

import requests
from datetime import datetime, timedelta
import json

from dnd_7th_4_backend.settings.base import env
from main.models import Api8, Region


# api_8 데이터 저장을 위한 데이터 요청
def call_api_8():
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV2/getUVIdxV2"
    search_date = datetime.today()

    # 오전 6시 이전인 경우
    now_hour = datetime.today().strftime("%H")
    if int(now_hour) <= 6:
        search_date = (datetime.today() - timedelta(days=1))
    print(f'api_8: get request: -----------------------------')

    region_data = Region.objects.all()
    for region in region_data:
        params = {
            "serviceKey": env('DECODING_KEY2'),
            "areaNo": region.div_code,
            "dataType": "JSON",
            "time": search_date.strftime("%Y%m%d")+"06"
        }
        try:
            # api 요청
            response = requests.get(url, params=params)

            # 데이터 받기가 성공일 경우
            code = response.json()['response']['header']['resultCode']
            if code == '00':
                # API 8 데이터 저장
                today = response.json()['response']['body']['items']['item'][0]['today']
                tomorrow = response.json()['response']['body']['items']['item'][0]['tomorrow']
                div_code = response.json()['response']['body']['items']['item'][0]['areaNo']
                api_8 = Api8(today = today, tomorrow = tomorrow, div_code = div_code)
                api_8.save()
                print(f'api_8: {div_code} {today} {tomorrow} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_8: Timeout: {region.div_code}-----------------------------')
        except requests.ConnectionError:
            print(f'api_8: ConnectionError: {region.div_code}-----------------------------')

# 오전 6시마다 api_8 데이터 업데이트
def update_api_8():
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV2/getUVIdxV2"
    search_date = datetime.today()

    # 오전 6시 이전인 경우
    now_hour = datetime.today().strftime("%H")
    if int(now_hour) <= 6:
        search_date = (datetime.today() - timedelta(days=1))
    print(f'api_8: get request: -----------------------------')

    region_data = Region.objects.all()
    for region in region_data:
        params = {
            "serviceKey": env('DECODING_KEY2'),
            "areaNo": region.div_code,
            "dataType": "JSON",
            "time": search_date.strftime("%Y%m%d")+"06"
        }
        try:
            # api 요청
            response = requests.get(url, params=params)

            # 데이터 받기가 성공일 경우
            code = response.json()['response']['header']['resultCode']

            if code == '00':
                # API 8 데이터 저장
                today = response.json()['response']['body']['items']['item'][0]['today']
                tomorrow = response.json()['response']['body']['items']['item'][0]['tomorrow']
                api8 = Api8.objects.filter(div_code = region.div_code)
                if len(api8) :
                    #API 8 업데이트
                    api8 = api8[0]
                    api8.today = today
                    api8.tomorrow = tomorrow
                else:
                    # Api 8 생성
                    api8 = Api8(today = today, tomorrow = tomorrow, div_code = region.div_code)
                api8.save()
                print(f'api_8: {region} {today} {tomorrow} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_8: Timeout: -----------------------------')
        except requests.ConnectionError:
            print(f'api_8: ConnectionError:-----------------------------')
        except request.JSONDecodeError:
            print(f'api_8: JSONDecodeError:-----------------------------')

# OpenAPI 에러 처리
def get_api_error(code, text):
    if code == '01':
        print('api_6: Application Error: Application 서비스 제공 상태 원활하지 않음-----------------------------')
    elif code == '02':
        print('api_6: DB Error: DB 서비스 제공 상태 원활하지 않음-----------------------------')
    else:
        print(text)