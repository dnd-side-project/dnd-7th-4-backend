from django.http import HttpResponse

import requests
from datetime import datetime, timedelta
import json

from dnd_7th_4_backend.settings.base import env
from main.models import Api9, Region

def api_10():
    url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
    search_date = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")
    hour = datetime.today().strftime("%H")
    print(f'api_10: get request: -----------------------------')
    print(search_date, hour)
    params = {
        "serviceKey": `lBsQJ7AKQ12dYsYOFKnToj90mX5JOb7s5a5gPvjf0ZiEpZIda9Umu3+VVW7YgKNCT1F4ByCX/r3MGSH/4VJQBg==`,
        "numOfRows" : "1",
        "dataType": "JSON",
        "dataCd": "ASOS",
        "dateCd": "HR",
        "startDt": search_date,
        "startHh" : hour,
        "endDt" : search_date,
        "endHh" : hour,
        "stnIds": "108" # 나중에 해당 지역 코드로
    }
    try:
        # api 요청
        response = requests.get(url, params=params)
        code = response.json()['response']['header']['resultCode']
        # 데이터 받기가 성공일 경우
        if code == '00':
            tem = response.json()['response']['body']['items']['item'][0]['ta']
            print(f'api_10 result : -- {tem} ---------------------------')
            return tem
        else:
            get_api_error(str(response.status_code), response.text)

    except requests.Timeout:
        print(f'api_10: Timeout: -----------------------------')
    except requests.ConnectionError:
        print(f'api_10: ConnectionError: -----------------------------')

# OpenAPI 에러 처리
def get_api_error(code, text):
    if code == '01':
        print('api_6: Application Error: Application 서비스 제공 상태 원활하지 않음-----------------------------')
    elif code == '02':
        print('api_6: DB Error: DB 서비스 제공 상태 원활하지 않음-----------------------------')
    else:
        print(text)
