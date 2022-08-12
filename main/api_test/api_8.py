from django.http import HttpResponse

import requests
from datetime import datetime, timedelta
import json

from dnd_7th_4_backend.settings.base import env
from main.models import Api8, Region

def api_8(request):
    if not len(Api8.objects.all()): # api_8 가 비어있는 경우
        print('api_8: save -----------------------------')
        call_api_8()

    else:
        print('api_8: update -----------------------------')
        update_api_8()
    return HttpResponse("api_8: Success  -----------------------------")

# api_8 데이터 저장을 위한 데이터 요청
def call_api_8():
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV2/getUVIdxV2"
    #serviceKey = env('API_SERVICEKEY1')
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    search_date = datetime.today()

    # 오전 6시 이전인 경우
    now_hour = datetime.today().strftime("%H")
    if int(now_hour) <= 6:
        search_date = (datetime.today() - timedelta(days=1))
    print(f'api_8: get request: -----------------------------')

    region_data = Region.objects.all()
    for region in region_data:
        params = {
            "serviceKey": serviceKey,
            "areaNo": region.div_code,
            "dataType": "JSON",
            "time": search_date.strftime("%Y%m%d")+"06"
        }
        try:
            # api 요청
            response = requests.get(url, params=params)
            print(response.text)

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

    #serviceKey = env('API_SERVICEKEY1')
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    search_date = datetime.today()

    # 오전 6시 이전인 경우
    now_hour = datetime.today().strftime("%H")
    if int(now_hour) <= 6:
        search_date = (datetime.today() - timedelta(days=1))
    print(f'api_8: get request: -----------------------------')

    api8_data = Api8.objects.all()
    for api8 in api8_data:
        region = api8.div_code
        params = {
            "serviceKey": serviceKey,
            "areaNo": region,
            "dataType": "JSON",
            "time": search_date.strftime("%Y%m%d")+"06"
        }
        try:
            # api 요청
            response = requests.get(url, params=params)
            print('a')
            # 데이터 받기가 성공일 경우
            code = response.json()['response']['header']['resultCode']
            print(response.text)
            if code == '00':
                # API 8 데이터 저장
                today = response.json()['response']['body']['items']['item'][0]['today']
                tomorrow = response.json()['response']['body']['items']['item'][0]['tomorrow']
                api8.today = today
                api8.tomorrow = tomorrow
                api8.save()
                print(f'api_8: {region} {today} {tomorrow} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_8: Timeout: -----------------------------')
        except requests.ConnectionError:
            print(f'api_8: ConnectionError:-----------------------------')