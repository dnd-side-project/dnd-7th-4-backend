from django.http import HttpResponse

import requests
from datetime import datetime

from dnd_7th_4_backend.settings.base import env
from main.models import Api6, Region


def api_6(request):
    if not len(Api6.objects.all()): # Api_6 가 비어있는 경우
        print('api_6: save -----------------------------')
        call_api_6()

    else:
        print('api_6: update -----------------------------')
        update_api_6()
        
    return HttpResponse("api_6: Success  -----------------------------")

# api_6 데이터 저장을 위한 데이터 요청
def call_api_6():
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    search_date = datetime.today().strftime("YYYY-mm-dd")
    local_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
    pm_data = {} # {(sideName, stationName): (pm10Grade1h, pm25Grade1h)}
    for local in local_list:
        params = {
            "serviceKey": env('DECODING_KEY2'),
            "returnType": "json",
            "sidoName": local,
            "numOfRows": 300,
            "ver": "1.3",
        }
        # api 요청
        try:
            response = requests.get(url, params=params)
            print(f'api_6: get request: {local}-----------------------------')

            # 데이터 받기가 성공일 경우
            if response.status_code == 200:
                for item in response.json()['response']['body']['items']:
                    sido_name = item['sidoName']
                    station_name = item['stationName']
                    pm_data = [item['pm10Grade1h'], item['pm25Grade1h'], item['pm10Grade'], item['pm25Grade']]

                    # 측정 불가 데이터 처리
                    for i in range(4):
                        if pm_data[i] == 1:
                            pm_data[i] = '좋음'
                        elif pm_data[i] == 2:
                            pm_data[i] = '보통'
                        elif pm_data[i] == 3:
                            pm_data[i] = '나쁨'
                        else:
                            pm_data[i] = '매우나쁨'

                    # 관련 지역에 대해서 Region 데이터가 존재하는지 확인
                    region_data = Region.objects.filter(api6_station = station_name)
                    if len(region_data) > 0:

                        print(f'api_6: {sido_name} {station_name} -----------------------------')
                        api6 = Api6(sidoName = sido_name, stationName = station_name, pm10Grade1h = pm_data[0], pm25Grade1h = pm_data[1],
                                    pm10Value24 = pm_data[2], pm25Value24 = pm_data[3])
                        api6.save()
                        
                        # Region에 FK 연결
                        for region in region_data:
                            print(f'api_6: connect fk {region} {api6.id} -----------------------------')
                            region.api6_id = api6
                            region.save()
            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_6: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_6: ConnectionError: {local}-----------------------------')

# 1시간 주기로 api_6 데이터 업데이트
def update_api_6():
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    search_date = datetime.today().strftime("YYYY-mm-dd")
    local_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
    pm_data = {} # {(sideName, stationName): (pm10Grade1h, pm25Grade1h)}
    for local in local_list:
        params = {
            "serviceKey": env('DECODING_KEY2'),
            "returnType": "json",
            "sidoName": local,
            "numOfRows": 300,
            "ver": "1.3",
        }
        try:
            # api 요청
            response = requests.get(url, params=params)
            print(f'api_6: get request: {local}-----------------------------')

            # 데이터 받기가 성공일 경우
            print(response.text)
            if response.status_code == 200:
                for item in response.json()['response']['body']['items']:
                    sido_name = item['sidoName']
                    station_name = item['stationName']
                    pm_data = [item['pm10Grade1h'], item['pm25Grade1h'], item['pm10Grade'], item['pm25Grade']]
                    
                    # 측정 불가 데이터 처리
                    for i in range(4):
                        if pm_data[i] == 1:
                            pm_data[i] = '좋음'
                        elif pm_data[i] == 2:
                            pm_data[i] = '보통'
                        elif pm_data[i] == 3:
                            pm_data[i] = '나쁨'
                        else:
                            pm_data[i] = '매우나쁨'

                    # api 데이터 찾아서 업데이트
                    api6_data = Api6.objects.filter(stationName = station_name)
                    for api6 in api6_data:
                        print(f'api_6: {sido_name} {station_name} -----------------------------')
                        api6.pm10Grade1h = pm_data[0]
                        api6.pm25Grade1h = pm_data[1]
                        api6.pm10Value24 = pm_data[2]
                        api6.pm25Value24 = pm_data[3]
                        api6.save()
            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_6: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_6: ConnectionError: {local}-----------------------------')

# OpenAPI 에러 처리
def get_api_error(code, text):
    if code == '01':
        print('api_6: Application Error: Application 서비스 제공 상태 원활하지 않음-----------------------------')
    elif code == '02':
        print('api_6: DB Error: DB 서비스 제공 상태 원활하지 않음-----------------------------')
    else:
        print(text)
    