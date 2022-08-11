from celery import shared_task

import requests
from datetime import datetime
import xmltodict
import json

from main.models import Api7, Region

# api_7 데이터 저장을 위한 데이터 요청
def call_api_7():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo"
    search_date = datetime.today().strftime("%Y%m%d")
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    print(f'api_7: get request: -----------------------------')

    region_data = Region.objects.all()
    for region in region_data:
        params = {
            "serviceKey": serviceKey,
            "locdate": search_date,
            "longitude": region.longitude,
            "latitude": region.latitude,
            "dnYn": "y",
        }
        try:
            # api 요청
            response_xml = requests.get(url, params=params)

            # 데이터 받기가 성공일 경우
            if response_xml.status_code == 200:
                # xml 을 json으로 변환
                xml_dict = xmltodict.parse(response_xml.text)
                response_str = json.dumps(xml_dict)
                response_json = json.loads(response_str)

                # API 7 데이터 저장
                sunrise = response_json['response']['body']['items']['item']['sunrise']
                sunset = response_json['response']['body']['items']['item']['sunset']
                api_7 = Api7(sunrise = sunrise, sunset = sunset, region_id = region)
                api_7.save()
                print(f'api_7: {region} {sunrise} {sunset} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_7: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_7: ConnectionError: {local}-----------------------------')

# 1시간 주기로 api_7 데이터 업데이트
def update_api_7():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo"
    search_date = datetime.today().strftime("%Y%m%d")
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    print(f'api_7: get request: -----------------------------')

    api7_data = Api7.objects.all()
    for api7 in api7_data:
        region = api7.region_id
        params = {
            "serviceKey": serviceKey,
            "locdate": search_date,
            "longitude": region.longitude,
            "latitude": region.latitude,
            "dnYn": "y",
        }
        try:
            # api 요청
            response_xml = requests.get(url, params=params)
        
            # 데이터 받기가 성공일 경우
            if response_xml.status_code == 200:
                # xml 을 json으로 변환
                xml_dict = xmltodict.parse(response_xml.text)
                response_str = json.dumps(xml_dict)
                response_json = json.loads(response_str)

                # Api7 데이터 업데이트
                sunrise = response_json['response']['body']['items']['item']['sunrise']
                sunset = response_json['response']['body']['items']['item']['sunset']
                api7.sunrise = sunrise
                api7.sunset = sunset
                api7.save()
                print(f'api_7: {region} {sunrise} {sunset} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_7: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_7: ConnectionError: {local}-----------------------------')