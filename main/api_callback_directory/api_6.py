import requests
from datetime import datetime
from celery import shared_task

from main.models import Api_6, Region

@shared_task
def api_6(request):
    if not len(Api_6.objects.all()): # Api_6 가 비어있는 경우
        print('api_6: save -----------------------------')
        call_api_6()
    else:
        print('api_6: update -----------------------------')
        update_api_6()

# api_6 데이터 저장을 위한 데이터 요청
def call_api_6():
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
        
        try:
            # api 요청
            response = requests.get(url, params=params)
            print(f'api_6: get request: {local}-----------------------------')

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

                    print(f'api_6: {sido_name} {station_name} -----------------------------')
                    api6 = Api_6(sidoName = sido_name, stationName = station_name, pm10Grade1h = pm_data[0], pm25Grade1h = pm_data[1],
                                pm10Value24 = pm_data[2], pm25Value24 = pm_data[3])
                    api6.save()
                    
                    # Region에 FK 연결
                    region_data = Region.objects.filter(api6_station = station_name)
                    for region in region_data:
                        print(f'api_6: connect fk {region} {api6.id} -----------------------------')
                        region.api6_id = api6
                        region.save()
        except requests.Timeout:
            print(f'api_6: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_6: ConnectionError: {local}-----------------------------')

# 1시간 주기로 api_6 데이터 업데이트
def update_api_6():
    import requests
    from datetime import datetime
    from .models import Api_6

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
        
        try:
            # api 요청
            response = requests.get(url, params=params)
            print(f'api_6: get request: {local}-----------------------------')

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

                    print(f'api_6: {sido_name} {station_name} -----------------------------')

                    # api 데이터 찾아서 업데이트
                    api6_data = Api_6.objects.filter(stationName = station_name)
                    for api6 in api6_data:
                        api6.pm10Grade1h = pm_data[0]
                        api6.pm25Grade1h = pm_data[1]
                        api6.pm10Value24 = pm_data[2]
                        api6.pm25Value24 = pm_data[3]
                        api6.save()
        except requests.Timeout:
            print(f'api_6: Timeout: {local}-----------------------------')
        except requests.ConnectionError:
            print(f'api_6: ConnectionError: {local}-----------------------------')