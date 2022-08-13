import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from main.models import Api4
import requests, datetime
from dnd_7th_4_backend.settings.base import env


# 중기육상예보 API

def func4():
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)  # 배포용
    current = datetime.datetime.now()  # 테스트용
    base_date = current.strftime("%Y%m%d")
    base_time = current.strftime("%H")
    # tmFc = str(base_date) + str(base_time) + "00"  # 배포용
    tmFc = "202208131800"  # 테스트용

    districtCode = ["11B00000", "11D10000", "11D20000", "11C20000", "11C10000",
                    "11F20000", "11F10000", "11H10000", "11H20000", "11G00000"]

    for regId in districtCode:  # region id: 중기육상예보 지역코드 (총 10개)

        # request url 정의
        url = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"

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

                obj = Api4.objects.filter(regId=regId)

                if obj.exists():
                    # 있음 -> 가져오기
                    obj = Api4.objects.get(regId=regId)
                else:
                    # 없음 -> 새로 생성
                    obj = Api4.objects.create(regId=regId)

                # 해당 필드에 데이터 넣기 or 갱신
                obj.tmFc = tmFc
                obj.rnSt3Am = item['rnSt3Am']
                obj.rnSt3Pm = item['rnSt3Pm']
                obj.rnSt4Am = item['rnSt4Am']
                obj.rnSt4Pm = item['rnSt4Pm']
                obj.rnSt5Am = item['rnSt5Am']
                obj.rnSt5Pm = item['rnSt5Pm']
                obj.rnSt6Am = item['rnSt6Am']
                obj.rnSt6Pm = item['rnSt6Pm']
                obj.rnSt7Am = item['rnSt7Am']
                obj.rnSt7Pm = item['rnSt7Pm']
                obj.rnSt8 = item['rnSt8']
                obj.rnSt9 = item['rnSt9']
                obj.rnSt10 = item['rnSt10']
                obj.wf3Am = item['wf3Am']
                obj.wf3Pm = item['wf3Pm']
                obj.wf4Am = item['wf4Am']
                obj.wf4Pm = item['wf4Pm']
                obj.wf5Am = item['wf5Am']
                obj.wf5Pm = item['wf5Pm']
                obj.wf6Am = item['wf6Am']
                obj.wf6Pm = item['wf6Pm']
                obj.wf7Am = item['wf7Am']
                obj.wf7Pm = item['wf7Pm']
                obj.wf8 = item['wf8']
                obj.wf9 = item['wf9']
                obj.wf10 = item['wf10']

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


def test():
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)  # 배포용
    current = datetime.datetime.now()  # 테스트용
    base_date = current.strftime("%Y%m%d")
    base_time = current.strftime("%H%M")
    # tmFc = str(base_date) + str(base_time)
    tmFc = "202208101800"  # 테스트용

    districtCode = ["11B00000", "11D10000", "11D20000", "11C20000", "11C10000",
                    "11F20000", "11F10000", "11H10000", "11H20000", "11G00000"]

    for regId in districtCode:  # region id: 1 ~ 250 까지 정보 업데이트

        # request url 정의
        url = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"

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
            # 해당 api4 obj 찾기
            obj = Api4.objects.get(regId=regId)
            # request 요청
            response = requests.get(url, params=params)
            # 결과 상태코드 정의
            rescode = response.status_code

            if (rescode == 200):
                response = response.json()
                item = response['response']['body']['items']['item'][0]

                obj.tmFc = tmFc
                obj.rnSt3Am = item['rnSt3Am']
                obj.rnSt3Pm = item['rnSt3Pm']
                obj.rnSt4Am = item['rnSt4Am']
                obj.rnSt4Pm = item['rnSt4Pm']
                obj.rnSt5Am = item['rnSt5Am']
                obj.rnSt5Pm = item['rnSt5Pm']
                obj.rnSt6Am = item['rnSt6Am']
                obj.rnSt6Pm = item['rnSt6Pm']
                obj.rnSt7Am = item['rnSt7Am']
                obj.rnSt7Pm = item['rnSt7Pm']
                obj.rnSt8 = item['rnSt8']
                obj.rnSt9 = item['rnSt9']
                obj.rnSt10 = item['rnSt10']
                obj.wf3Am = item['wf3Am']
                obj.wf3Pm = item['wf3Pm']
                obj.wf4Am = item['wf4Am']
                obj.wf4Pm = item['wf4Pm']
                obj.wf5Am = item['wf5Am']
                obj.wf5Pm = item['wf5Pm']
                obj.wf6Am = item['wf6Am']
                obj.wf6Pm = item['wf6Pm']
                obj.wf7Am = item['wf7Am']
                obj.wf7Pm = item['wf7Pm']
                obj.wf8 = item['wf8']
                obj.wf9 = item['wf9']
                obj.wf10 = item['wf10']

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