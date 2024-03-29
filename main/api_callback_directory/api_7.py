from django.http import HttpResponse

import requests
from datetime import datetime, timedelta
import xmltodict
import json

from dnd_7th_4_backend.settings.base import env
from main.models import Api7, Region


# api_7 데이터 저장을 위한 데이터 요청
def call_api_7():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo"
    now = datetime.today()
    tomorrow = (datetime.today() + timedelta(days=1))
    print(f'api_7: get request: -----------------------------')

    region_data = Region.objects.all()
    for region in region_data:
        try:
            # 오늘에 대한 데이터 보내기
            today_params = {
                "serviceKey": env('DECODING_KEY2'),
                "locdate": now.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_today = requests.get(url, params=today_params)

            # 내일에 대한 데이터 보내기
            tomorrow_params = {
                "serviceKey": env('DECODING_KEY2'),
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
    print(f'api_7: get request: -----------------------------')
    now = datetime.today()
    tomorrow = (datetime.today() + timedelta(days=1))
    
    data = []
    region_data = Region.objects.all()
    for region in region_data:
        try:
            # 오늘에 대한 데이터 보내기
            today_params = {
                "serviceKey": env('DECODING_KEY2'),
                "locdate": now.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_today = requests.get(url, params=today_params)

            # 내일에 대한 데이터 보내기
            tomorrow_params = {
                "serviceKey": env('DECODING_KEY2'),
                "locdate": tomorrow.strftime("%Y%m%d"),
                "longitude": region.longitude,
                "latitude": region.latitude,
                "dnYn": "y",
            }
            response_xml_tomorrow = requests.get(url, params=tomorrow_params)

            # xml 을 json으로 변환
            ## 오늘
            xml_dict_today = xmltodict.parse(response_xml_today.text)
            response_str_today = json.dumps(xml_dict_today)
            response_json_today = json.loads(response_str_today)
            ##내일
            xml_dict_tomorrow = xmltodict.parse(response_xml_tomorrow.text)
            response_str_tomorrow = json.dumps(xml_dict_tomorrow)
            response_json_tomorrow = json.loads(response_str_tomorrow)
            data = [response_json_today, response_json_tomorrow]
            # 데이터 받기가 성공일 경우
            if response_json_today['response']['header']['resultCode'] == '00' and response_json_tomorrow['response']['header']['resultCode'] == '00':
                api7 = 0
                print(response_json_tomorrow['response']['body']['items']['item'])
                print(response_json_today['response']['body']['items']['item'])
                today_sunrise = response_json_today['response']['body']['items']['item']['sunrise']
                today_sunset = response_json_today['response']['body']['items']['item']['sunset']
                tomorrow_sunrise = response_json_tomorrow['response']['body']['items']['item']['sunrise']
                tomorrow_sunset = response_json_tomorrow['response']['body']['items']['item']['sunset']
                if hasattr(region, 'api7'):
                    # Api7 데이터 업데이트
                    api7 = region.api7
                    api7.today_sunrise = today_sunrise
                    api7.today_sunset = today_sunset
                    api7.tomorrow_sunrise = tomorrow_sunrise
                    api7.tomorrow_sunset = tomorrow_sunset
                else:
                    # API7 새로 생성하기
                    api7 = Api7(today_sunrise = today_sunrise, today_sunset = today_sunset, tomorrow_sunrise = tomorrow_sunrise, tomorrow_sunset = tomorrow_sunset,region_id = region)
                api7.save()
                print(f'api_7: {region} {today_sunrise} {tomorrow_sunrise} -----------------------------')

            else:
                get_api_error(str(response_json_today['response']['header']['resultCode']), response_json_today.text)
                get_api_error(str(response_json_tomorrow['response']['header']['resultCode']), response_json_tomorrow.text)

        except requests.Timeout:
            print(f'api_7: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_7: ConnectionError: {local}-----------------------------')
        except KeyError:
            print()

# OpenAPI 에러 처리
def get_api_error(code, text):
    if code == '01':
        print('api_6: Application Error: Application 서비스 제공 상태 원활하지 않음-----------------------------')
    elif code == '02':
        print('api_6: DB Error: DB 서비스 제공 상태 원활하지 않음-----------------------------')
    else:
        print(text)