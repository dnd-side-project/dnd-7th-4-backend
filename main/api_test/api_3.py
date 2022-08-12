import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
import django
django.setup()

from main.models import Api3, Region
import requests, datetime
from dnd_7th_4_backend.settings.base import env


# 단기예보조회
## 1일 8회 조회 가능 (2, 5, 8, 11, 14, 17, 20, 23) + 매 시각 10분 이후부터 API 제공
## API 호출 시간: ( 0215, 0515, ... 2315 )

def func3():
    sky = {'1': '맑음', '3': '구름많음', '4': '흐림'}
    pty = {'0': '없음', '1': '비', '2': '비/눈',
           '3': '눈', '4': '소나기'}
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)
    current = datetime.datetime.now()
    base_date = current.strftime("%Y%m%d")
    # base_time = current.strftime("%H%M") ## 배포용
    base_time = "2015"  # 테스트용

    for i in range(1, 3):  # region id: 1 ~ 250 까지 정보 업데이트
        region = Region.objects.get(id=i)
        nx = region.cor_x
        ny = region.cor_y

        # request url 정의
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

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

                print(f'id: {i}, fcstTime: {fcstTime}')

                TMP = []  # 1시간 기온
                SKY = []  # 하늘 상태

                REH = []  # 습도

                PTY = []  # 강수 형태
                POP = []  # 강수 확률
                PCP = []  # 1시간 강수량

                WSD = []  # 풍속
                VEC = []  # 풍향

                TMN = []  # 일 최저기온
                TMX = []  # 일 최고기온

                for item in items:
                    # print(item)
                    if item['category'] == 'TMP':  # 기온
                        TMP.append(item['fcstValue'])
                    if item['category'] == 'SKY':  # 하늘 상태
                        SKY.append(item['fcstValue'])
                    if item['category'] == 'REH':  # 습도
                        REH.append(item['fcstValue'])
                    if item['category'] == 'PTY':  # 강수 형태
                        PTY.append(item['fcstValue'])
                    if item['category'] == 'POP':  # 강수 확률
                        POP.append(item['fcstValue'])
                    if item['category'] == 'PCP':  # 1시간 강수량
                        PCP.append(item['fcstValue'])
                    if item['category'] == 'WSD':  # 풍속
                        WSD.append(item['fcstValue'])
                    if item['category'] == 'VEC':  # 풍향
                        VEC.append(item['fcstValue'])
                    if item['category'] == 'TMN':  # 일 최저기온
                        TMN.append(item['fcstValue'])
                    if item['category'] == 'TMX':  # 일 최고기온
                        TMX.append(item['fcstValue'])

                obj = Api3.objects.filter(region=region)

                if obj.exists():
                    # 있음 -> 가져오기
                    obj = Api3.objects.get(region=region)
                else:
                    # 없음 -> 새로 생성
                    obj = Api3.objects.create(region=region)

                print(TMP)
                print(REH)

                for i in range(fcstTime, 48):
                    field = "info_" + str(i)
                    idx = i - fcstTime
                    value = str(TMP[idx]) + '/ ' + sky[SKY[idx]] + '/ ' + str(REH[idx]) + '/ ' +\
                            pty[PTY[idx]] + '/ ' + str(POP[idx]) + '/ ' + str(PCP[idx]) + '/ ' +\
                            str(WSD[idx]) + '/ ' + str(VEC[idx])

                    print(f'time: {i}, idx: {idx}, value: {value}')

                    if field == 'info_0':
                        obj.info_0 = value
                    elif field == 'info_1':
                        obj.info_1 = value
                    elif field == 'info_2':
                        obj.info_2 = value
                    elif field == 'info_3':
                        obj.info_3 = value
                    elif field == 'info_4':
                        obj.info_4 = value
                    elif field == 'info_5':
                        obj.info_5 = value
                    elif field == 'info_6':
                        obj.info_6 = value
                    elif field == 'info_7':
                        obj.info_7 = value
                    elif field == 'info_8':
                        obj.info_8 = value
                    elif field == 'info_9':
                        obj.info_9 = value
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
                    elif field == 'info_24':
                        obj.info_24 = value
                    elif field == 'info_25':
                        obj.info_25 = value
                    elif field == 'info_26':
                        obj.info_26 = value
                    elif field == 'info_27':
                        obj.info_27 = value
                    elif field == 'info_28':
                        obj.info_28 = value
                    elif field == 'info_29':
                        obj.info_29 = value
                    elif field == 'info_30':
                        obj.info_30 = value

                    elif field == 'info_31':
                        obj.info_31 = value
                    elif field == 'info_32':
                        obj.info_32 = value
                    elif field == 'info_33':
                        obj.info_33 = value
                    elif field == 'info_34':
                        obj.info_34 = value
                    elif field == 'info_35':
                        obj.info_35 = value
                    elif field == 'info_36':
                        obj.info_36 = value
                    elif field == 'info_37':
                        obj.info_37 = value
                    elif field == 'info_38':
                        obj.info_38 = value
                    elif field == 'info_39':
                        obj.info_39 = value
                    elif field == 'info_40':
                        obj.info_40 = value

                    elif field == 'info_41':
                        obj.info_41 = value
                    elif field == 'info_42':
                        obj.info_42 = value
                    elif field == 'info_43':
                        obj.info_43 = value
                    elif field == 'info_44':
                        obj.info_44 = value
                    elif field == 'info_45':
                        obj.info_45 = value
                    elif field == 'info_46':
                        obj.info_46 = value
                    elif field == 'info_47':
                        obj.info_47 = value

                # 일 최저기온 / 최고기온 기록 갱신시키기
                ## 각 시간별 예외처리 필요
                # 일 최고기온 / 최저기온 기록 방법에 대해서
                if fcstTime == 3:
                    obj.info_day0_MIN, obj.info_day1_MIN, obj.info_day2_MIN = TMN[0], TMN[1], TMN[2]
                    obj.info_day0_MAX, obj.info_day1_MAX, obj.info_day2_MAX = TMX[0], TMX[1], TMX[2]
                elif fcstTime in [6, 9, 12]:
                    obj.info_day1_MIN, obj.info_day2_MIN = TMN[0], TMN[1]  # 내일, 모레
                    obj.info_day0_MAX, obj.info_day1_MAX, obj.info_day2_MAX = TMX[0], TMX[1], TMX[2]
                elif fcstTime == 15:
                    obj.info_day1_MIN, obj.info_day2_MIN = TMN[0], TMN[1]  # 내일, 모레
                    obj.info_day1_MAX, obj.info_day2_MAX = TMX[0], TMX[1]  # 내일, 모레
                elif fcstTime in [18, 21, 0]:
                    obj.info_day1_MIN, obj.info_day2_MIN, obj.info_day3_MIN = TMN[0], TMN[1], TMN[2]  # 내일, 모레, 글피
                    obj.info_day1_MAX, obj.info_day2_MAX, obj.info_day3_MAX = TMX[0], TMX[1], TMX[2]  # 내일, 모레, 글피

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


# 단기예보조회
def test():
    sky = {'1': '맑음', '3': '구름많음', '4': '흐림'}
    pty = {'0': '없음', '1': '비', '2': '비/눈',
           '3': '눈', '4': '소나기'}
    # current = datetime.datetime.now() + datetime.timedelta(hours=9)
    current = datetime.datetime.now() - datetime.timedelta(hours=1)
    base_date = current.strftime("%Y%m%d")
    base_time = current.strftime("%H%M")
    base_time = "2300"

    for i in range(7, 9):  # region id: 1 ~ 250 까지 정보 업데이트
        print(i, base_time)
        region = Region.objects.get(id=i)
        api2 = Api3.objects.get(region=region)
        nx = region.cor_x
        ny = region.cor_y

        # request url 정의
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

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
                print(fcstTime)

                TMX = []  # 일 최고기온
                TMN = []  # 일 최저기온


                for item in items:
                    if item['category'] == 'TMX':  # 일 최고기온
                        TMX.append(item['fcstValue'])
                    if item['category'] == 'TMN':  # 일 최저기온
                        TMN.append(item['fcstValue'])


                print("TMX size: ", len(TMX))
                print(TMX)
                print("TMN size: ", len(TMN))
                print(TMN)

                # 일 최고기온 / 최저기온 기록 방법에 대해서
                if base_time == "0200":
                    api2.info_day0_MIN, api2.info_day1_MIN, api2.info_day2_MIN = TMN[0], TMN[1], TMN[2]
                    api2.info_day0_MAX, api2.info_day1_MAX, api2.info_day2_MAX = TMX[0], TMX[1], TMX[2]
                elif base_time in ["0500", "0800", "1100"]:
                    api2.info_day1_MIN, api2.info_day2_MIN = TMN[0], TMN[1]  # 내일, 모레
                    api2.info_day0_MAX, api2.info_day1_MAX, api2.info_day2_MAX = TMX[0], TMX[1], TMX[2]
                elif base_time == "1400":
                    api2.info_day1_MIN, api2.info_day2_MIN = TMN[0], TMN[1]  # 내일, 모레
                    api2.info_day1_MAX, api2.info_day2_MAX = TMX[0], TMX[1]  # 내일, 모레
                elif base_time in ["1700", "2000", "2300"]:
                    api2.info_day1_MIN, api2.info_day2_MIN, api2.info_day3_MIN = TMN[0], TMN[1], TMN[2]  # 내일, 모레, 글피
                    api2.info_day1_MAX, api2.info_day2_MAX, api2.info_day3_MAX = TMX[0], TMX[1], TMX[2]  # 내일, 모레, 글피

                api2.save()
        except:
            print("error")
            pass



func3()