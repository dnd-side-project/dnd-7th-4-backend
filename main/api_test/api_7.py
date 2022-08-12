from django.http import HttpResponse

import requests
from datetime import datetime, timedelta
import xmltodict
import json

from main.models import Api7, Region

def api_7(request):
    print('in')
    if not len(Api7.objects.all()): # api_7 가 비어있는 경우
        print('api_7: save -----------------------------')
        call_api_7()

    else:
        print('api_7: update -----------------------------')
        update_api_7()
    return HttpResponse("api_7: Success  -----------------------------")

# api_7 데이터 저장을 위한 데이터 요청
def call_api_7():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo"
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    now = datetime.today()
    tomorrow = (datetime.today() + timedelta(days=1))
    print(f'api_7: get request: -----------------------------')

    region_data = Region.objects.all()
    for region in region_data:
        try:
            # 오늘에 대한 데이터 보내기
            today_params = {
                "serviceKey": serviceKey,
                "locdate": now.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_today = requests.get(url, params=today_params)

            # 내일에 대한 데이터 보내기
            tomorrow_params = {
                "serviceKey": serviceKey,
                "locdate": tomorrow.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_tomorrow = requests.get(url, params=tomorrow_params)
            

            # 데이터 받기가 성공일 경우
            if response_xml_today.status_code == 200 and response_xml_tomorrow.status_code == 200:
                # xml 을 json으로 변환
                ## 오늘
                xml_dict_today = xmltodict.parse(response_xml_today.text)
                response_str_today = json.dumps(xml_dict_today)
                response_json_today = json.loads(response_str_today)
                ##내일
                xml_dict_tomorrow = xmltodict.parse(response_xml_tomorrow.text)
                response_str_tomorrow = json.dumps(xml_dict_tomorrow)
                response_json_tomorrow = json.loads(response_str_tomorrow)

                # API 7 데이터 저장
                today_sunrise = response_json_today['response']['body']['items']['item']['sunrise']
                today_sunset = response_json_today['response']['body']['items']['item']['sunset']
                tomorrow_sunrise = response_json_tomorrow['response']['body']['items']['item']['sunrise']
                tomorrow_sunset = response_json_tomorrow['response']['body']['items']['item']['sunset']
                api_7 = Api7(today_sunrise = today_sunrise, today_sunset = today_sunset, tomorrow_sunrise = tomorrow_sunrise, tomorrow_sunset = tomorrow_sunset,region_id = region)
                api_7.save()
                print(f'api_7: {region} {today_sunrise} {tomorrow_sunrise} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_7: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_7: ConnectionError: {local}-----------------------------')

# 1시간 주기로 api_7 데이터 업데이트
def update_api_7():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo"
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    print(f'api_7: get request: -----------------------------')
    now = datetime.today()
    tomorrow = (datetime.today() + timedelta(days=1))

    api7_data = Api7.objects.all()
    for api7 in api7_data:
        try:
            region = api7.region_id
            # 오늘에 대한 데이터 보내기
            today_params = {
                "serviceKey": serviceKey,
                "locdate": now.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_today = requests.get(url, params=today_params)

            # 내일에 대한 데이터 보내기
            tomorrow_params = {
                "serviceKey": serviceKey,
                "locdate": tomorrow.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_tomorrow = requests.get(url, params=tomorrow_params)
        
            # 데이터 받기가 성공일 경우
            if response_xml_today.status_code == 200 and response_xml_tomorrow.status_code == 200:
                # xml 을 json으로 변환
                ## 오늘
                xml_dict_today = xmltodict.parse(response_xml_today.text)
                response_str_today = json.dumps(xml_dict_today)
                response_json_today = json.loads(response_str_today)
                ##내일
                xml_dict_tomorrow = xmltodict.parse(response_xml_tomorrow.text)
                response_str_tomorrow = json.dumps(xml_dict_tomorrow)
                response_json_tomorrow = json.loads(response_str_tomorrow)

                # Api7 데이터 업데이트
                today_sunrise = response_json_today['response']['body']['items']['item']['sunrise']
                tomorrow_sunrise = response_json_tomorrow['response']['body']['items']['item']['sunrise']
                api7.today_sunrise = today_sunrise
                api7.today_sunset = response_json_today['response']['body']['items']['item']['sunset']
                api7.tomorrow_sunrise = tomorrow_sunrise
                api7.tomorrow_sunset = response_json_tomorrow['response']['body']['items']['item']['sunset']
                api7.save()
                print(f'api_7: {region} {today_sunrise} {tomorrow_sunrise} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_7: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_7: ConnectionError: {local}-----------------------------')