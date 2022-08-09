from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from main.models import *
from dnd_7th_4_backend.settings.base import env
from datetime import date, datetime
from dnd_7th_4_backend.celery import app


# api1 처음 호출 시 필요한 함수 -> create
def func1():
    d = str(date.today())
    now = datetime.now()
    base_date = d.replace("-", "")
    base_date = "20220810"

    h = now.strftime("%H")
    m = now.strftime("%M")
    # base_time = str(h) + str(m)
    base_time = "0300"

    print(base_date, base_time)
    for i in range(1, 251):  # region id: 1 ~ 250 까지 정보 업데이트
        region = Region.objects.get(id=i)
        nx = region.cor_x
        ny = region.cor_y

        print(region.id, nx, ny)

        # request url 정의
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

        # request parameter 정의
        params = {
            "ServiceKey": env('DECODING_KEY1'),
            "pageNo": 1,
            "numOfRows": 1000,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": region.cor_x,
            "ny": region.cor_y
        }

        try:
            # request 요청
            response = requests.get(url, params=params)
            print(response)
            # 결과 상태코드 정의
            rescode = response.status_code

            if (rescode == 200):
                print("rescode")
                print(rescode)
                response = response.json()
                print("response", response)
                items = response['response']['body']['items']['item']
                print("items", items)

                print("pass")

                for item in items:
                    if item['category'] == 'PTY':
                        PTY = item['obsrValue']
                    if item['category'] == 'REH':
                        REH = item['obsrValue']
                    if item['category'] == 'RN1':
                        RN1 = item['obsrValue']
                    if item['category'] == 'T1H':
                        T1H = item['obsrValue']
                    if item['category'] == 'UUU':
                        UUU = item['obsrValue']
                    if item['category'] == 'VEC':
                        VEC = item['obsrValue']
                    if item['category'] == 'VVV':
                        VVV = item['obsrValue']
                    if item['category'] == 'WSD':
                        WSD = item['obsrValue']

                Api1.objects.create(region=region, base_date=base_date, base_time=base_time, PTY=PTY, REH=REH,
                                    RN1=RN1, T1H=T1H, UUU=UUU, VEC=VEC, VVV=VVV, WSD=WSD)

            else:
                print("Error Code: " + str(rescode))

        except requests.Timeout:
            print("Timeout Error")
            pass
        except requests.ConnectionError:
            print("Connection Error")
            pass
        except:
            pass


# api1 재호출 시 필요한 함수 -> update
def func2():
    d = str(date.today())
    now = datetime.now()
    base_date = d.replace("-", "")

    h = now.strftime("%H")
    m = now.strftime("%M")
    base_time = str(h) + str(m)


    for i in range(1, 251):  # region id: 1 ~ 250 까지 정보 업데이트
        region = Region.objects.get(id=i)
        nx = region.cor_x
        ny = region.cor_y

        print(region.id, nx, ny)

        # request url 정의
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

        # request parameter 정의
        params = {
            "ServiceKey": env('DECODING_KEY1'),
            "pageNo": 1,
            "numOfRows": 1000,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": region.cor_x,
            "ny": region.cor_y
        }

        try:
            # request 요청
            response = requests.get(url, params=params)
            # 결과 상태코드 정의
            rescode = response.status_code

            obj = Api1.objects.get(region=region)
            print(rescode, obj)
            if (rescode == 200 and obj is not None):
                response = response.json()
                items = response['response']['body']['items']['item']

                for item in items:

                    if item['category'] == 'PTY':
                        obj.PTY = item['obsrValue']
                    if item['category'] == 'REH':
                        obj.REH = item['obsrValue']
                    if item['category'] == 'RN1':
                        obj.RN1 = item['obsrValue']
                    if item['category'] == 'T1H':
                        obj.T1H = item['obsrValue']
                    if item['category'] == 'UUU':
                        obj.UUU = item['obsrValue']
                    if item['category'] == 'VEC':
                        obj.VEC = item['obsrValue']
                    if item['category'] == 'VVV':
                        obj.VVV = item['obsrValue']
                    if item['category'] == 'WSD':
                        obj.WSD = item['obsrValue']

                obj.base_date = base_date
                obj.base_time = base_time
                obj.save()

            else:
                print("Error Code: " + str(rescode))

        except requests.Timeout:
            print("Timeout Error")
            pass
        except requests.ConnectionError:
            print("Connection Error")
            pass
        except:
            print("Extra Error")
            pass