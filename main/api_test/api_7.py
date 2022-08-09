import requests
from datetime import datetime
import xmltodict
import json

from main.models import Api_7, Region

def api_7(request):
    
    print('in')
    if not len(api_7.objects.all()): # api_7 가 비어있는 경우
        print('api_7: save -----------------------------')
        call_api_7()

    else:
        print('api_7: update -----------------------------')
        update_api_7()

# api_7 데이터 저장을 위한 데이터 요청
def call_api_7():
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo"
    search_date = datetime.today().strftime("%Y%m%d")
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='

    params = {
        "serviceKey": setting.api_key_decode,
        "locdate": search_date,
        "longitude": 128.20000,
        "latitude": 37.1500,
        "dnYn": "y",
    }

    print(f'api_7: get request: {local}-----------------------------')
    response_xml = requests.get(url, params=params)

    # 데이터 받기가 성공일 경우
    if response_xml.status_code == 200:
        xml_dict = xmltodict.parse(response_xml.text)
        response_str = json.dumps(xml_dict)
        response_json = json.loads(response_str)

        sunrise = response_json['response']['body']['items']['item']['sunrise']
        sunset = response_json['response']['body']['items']['item']['sunset']

# 1시간 주기로 api_7 데이터 업데이트
def update_api_7():

    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    search_date = datetime.today().strftime("YYYY-mm-dd")
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    local_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
    pm_data = {} # {(sideName, stationName): (pm10Grade1h, pm25Grade1h)}
    for local in local_list:
        params = {
            "serviceKey": serviceKey,
            "returnType": "json",
            "sidoName": local,
            "numOfRows": 300,
            "ver": "1.3",
        }
        # api 요청
        response = requests.get(url, params=params)
        print(f'api_7: get request: {local}-----------------------------')

        # 데이터 받기가 성공일 경우
        if response.status_code == 200:
            for item in response.json()['response']['body']['items']:
                # API6 model에 저장
                sido_name = item['sidoName']
                station_name = item['stationName']
                pm_data = [item['pm10Grade1h'], item['pm25Grade1h'], item['pm10Value24'], item['pm25Value24']]

                # 측정 불가 데이터 처리
                for i in range(4):
                    if pm_data[i] == '-':
                        pm_data[i] = 0

                print(f'api_7: {sido_name} {station_name} -----------------------------')

                # api 데이터 찾아서 업데이트
                api6_data = api_7.objects.filter(stationName = station_name)
                for api6 in api6_data:
                    api6.pm10Grade1h = pm_data[0]
                    api6.pm25Grade1h = pm_data[1]
                    api6.pm10Value24 = pm_data[2]
                    api6.pm25Value24 = pm_data[3]
                    api6.save()