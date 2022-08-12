import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from main.models import Api2, Region
import requests, datetime
from dnd_7th_4_backend.settings.base import env


# API2 - 초단기 예보 조회
def func2():
    sky = {'1': '맑음', '3': '구름많음', '4': '흐림'}  # 하늘상태코드
    pty = {'0': '없음', '1': '비', '2': '비/눈', '5': '빗방울',  # 강수형태코드
           '6': '빗방울눈날림', '7': '눈날림'}
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)  # 최종 배포용
    current = datetime.datetime.now()  # 매 시각 45분 이후부터 호출 가능 --> task에는 45분으로 등록
    base_date = current.strftime("%Y%m%d")
    base_time = current.strftime("%H%M")

    for i in range(1, 251):  # region id: 1 ~ 250 까지 정보 업데이트
        region = Region.objects.get(id=i)
        nx = region.cor_x
        ny = region.cor_y

        # request url 정의
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

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

            if (rescode == 200):
                response = response.json()
                items = response['response']['body']['items']['item']
                fcstTime = int((items[0]['fcstTime'])[0:2])  # 관측 첫 시작 시간

                # print(items)
                print(f'item: {i} | fcstTime: {fcstTime}')

                T1H = []  # 기온
                SKY = []  # 하늘 상태
                PTY = []  # 강수 형태
                RN1 = []  # 1시간 강수량

                for item in items:
                    if item['category'] == 'T1H':
                        T1H.append(item['fcstValue'])
                    if item['category'] == 'SKY':
                        SKY.append(item['fcstValue'])
                    if item['category'] == 'PTY':
                        PTY.append(item['fcstValue'])
                    if item['category'] == 'RN1':
                        RN1.append(item['fcstValue'])

                obj = Api2.objects.filter(region=region)

                if obj.exists():
                    # 있음 -> 객체 가져오기
                    obj = Api2.objects.get(region=region)
                else:
                    # 없음 -> 객체 새로 생성
                    obj = Api2.objects.create(region=region)

                for i in range(6):  # 총 6시간에 대한 기록 정보
                    field = "info_" + str((fcstTime + i) % 24)
                    value = str(T1H[i]) + '/ ' + sky[SKY[i]] + '/ ' + pty[PTY[i]] + '/ ' + str(RN1[i])  # 저장할 값들 문자열로 만들기
                    print(f'{field} || {value}')

                    if field == 'info_0':
                        obj.info_00 = value
                    elif field == 'info_1':
                        obj.info_01 = value
                    elif field == 'info_2':
                        obj.info_02 = value
                    elif field == 'info_3':
                        obj.info_03 = value
                    elif field == 'info_4':
                        obj.info_04 = value
                    elif field == 'info_5':
                        obj.info_05 = value
                    elif field == 'info_6':
                        obj.info_06 = value
                    elif field == 'info_7':
                        obj.info_07 = value
                    elif field == 'info_8':
                        obj.info_08 = value
                    elif field == 'info_9':
                        obj.info_09 = value
                    elif field == 'info_10':
                        obj.info_10 = value

                    elif field == 'info_11':
                        obj.info_11 = value
                    elif field == 'info_12':
                        obj.info_12 = value
                    elif field == 'info_13':
                        obj.info_13 = value
                    elif field == 'info_14':
                        obj.info_14 = value
                    elif field == 'info_15':
                        obj.info_15 = value
                    elif field == 'info_16':
                        obj.info_16 = value
                    elif field == 'info_17':
                        obj.info_17 = value
                    elif field == 'info_18':
                        obj.info_18 = value
                    elif field == 'info_19':
                        obj.info_19 = value
                    elif field == 'info_20':
                        obj.info_20 = value

                    elif field == 'info_21':
                        obj.info_21 = value
                    elif field == 'info_22':
                        obj.info_22 = value
                    elif field == 'info_23':
                        obj.info_23 = value

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


func2()