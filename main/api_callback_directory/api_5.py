import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from main.models import Api5, Region
import requests, datetime
from dnd_7th_4_backend.settings.base import env


# 중기기온예보 API
def func5():
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)  # 배포용
    current = datetime.datetime.now()  # 테스트용
    base_date = current.strftime("%Y%m%d")
    base_time = current.strftime("%H%M")
    # tmFc = str(base_date) + str(base_time) + "00"  # 배포용
    tmFc = "202208131800"  # 테스트용

    districtCode = ["11B10101", "11B20201", "11B20601", "11B20305", "11D10301", "11D10401",
                    "11D20501", "11C20401", "11C20101", "11C20404", "11C10301", "11G00201",
                    "11G00401", "11F20501", "21F20801", "11F20401", "11F10201", "21F10501",
                    "11H20201", "11H20101", "11H20301", "11H10701", "11H10501", "11H10201"]

    for i in range(1, 251):  # region id: 1 ~ 250 까지 정보 create
        region = Region.objects.get(id=i)
        regId = region.api6_code

        # request url 정의
        url = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"

        # request parameter 정의
        params = {
            "serviceKey": env('DECODING_KEY1'),
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
            "regId": regId,
            "tmFc": tmFc
        }

        try:
            # request 요청
            response = requests.get(url, params=params)
            # 결과 상태코드 정의
            rescode = response.status_code

            if (rescode == 200):
                response = response.json()
                item = response['response']['body']['items']['item'][0]
                print(item)

                obj = Api5.objects.filter(region=region)

                if obj.exists():
                    # 있음 -> 가져오기
                    obj = Api5.objects.get(region=region)
                else:
                    # 없음 -> 새로 생성
                    obj = Api5.objects.create(region=region)

                obj.regId = regId
                obj.tmFc = tmFc
                obj.taMin3 = item['taMin3']  # 3일 후 예상 최저 기온
                obj.taMax3 = item['taMax3']  # 3일 후 예상 최고 기온
                obj.taMin4 = item['taMin4']  # 4일 후 예상 최저 기온
                obj.taMax4 = item['taMax4']  # 4일 후 예상 최고 기온
                obj.taMin5 = item['taMin5']  # 5일 후 예상 최저 기온
                obj.taMax5 = item['taMax5']  # 5일 후 예상 최고 기온
                obj.taMin6 = item['taMin6']  # 6일 후 예상 최저 기온
                obj.taMax6 = item['taMax6']  # 6일 후 예상 최고 기온
                obj.taMin7 = item['taMin7']  # 7일 후 예상 최저 기온
                obj.taMax7 = item['taMax7']  # 7일 후 예상 최고 기온
                obj.taMin8 = item['taMin8']  # 8일 후 예상 최저 기온
                obj.taMax8 = item['taMax8']  # 8일 후 예상 최고 기온
                obj.taMin9 = item['taMin9']  # 9일 후 예상 최저 기온
                obj.taMax9 = item['taMax9']  # 9일 후 예상 최고 기온
                obj.taMin10 = item['taMin10']  # 10일 후 예상 최저 기온
                obj.taMax10 = item['taMax10']  # 10일 후 예상 최고 기온

                obj.save()

                print("success")

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



def test():
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)  # 배포용
    current = datetime.datetime.now()  # 테스트용
    base_date = current.strftime("%Y%m%d")
    base_time = current.strftime("%H%M")
    # tmFc = str(base_date) + str(base_time)
    tmFc = "202208101800"  # 테스트용

    objs = Api5.objects.all()

    for obj in objs:  # region id: 1 ~ 250 까지 정보 업데이트

        # request url 정의
        url = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"

        # request parameter 정의
        params = {
            "serviceKey": env('DECODING_KEY1'),
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
            "regId": obj.regId,
            "tmFc": tmFc
        }

        try:
            # request 요청
            response = requests.get(url, params=params)
            # 결과 상태코드 정의
            rescode = response.status_code

            if (rescode == 200):
                response = response.json()
                item = response['response']['body']['items']['item'][0]
                print(obj, item)

                obj.tmFc = tmFc
                obj.taMin3 = item['taMin3']
                obj.taMax3 = item['taMax3']
                obj.taMin4 = item['taMin4']
                obj.taMax4 = item['taMax4']
                obj.taMin5 = item['taMin5']
                obj.taMax5 = item['taMax5']
                obj.taMin6 = item['taMin6']
                obj.taMax6 = item['taMax6']
                obj.taMin7 = item['taMin7']
                obj.taMax7 = item['taMax7']
                obj.taMin8 = item['taMin8']
                obj.taMax8 = item['taMax8']
                obj.taMin9 = item['taMin9']
                obj.taMax9 = item['taMax9']
                obj.taMin10 = item['taMin10']
                obj.taMax10 = item['taMax10']

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


