from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from drf_yasg.utils import swagger_auto_schema

from datetime import datetime
import collections
import requests
import json

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from main.models import *
from account.models import *
from .serializers import *
from dnd_7th_4_backend.settings.base import env

from .kakaoalarm_callback_directory.summer_kakao_alarm import send_kakao_alarm

from .comment_callback_directory.comments import *
from .comment_callback_directory.comments_img import *

from .api_test.api_10 import api_10


pty = {'0': '없음', '1': '비', '2': '비/눈', '5': '빗방울',  # 강수형태코드
       '6': '빗방울눈날림', '7': '눈날림'}


# 메인 화면 - 오늘, 내일, 이번주
class MainView(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        self.today_finedust = 0
        self.today_windchill = 0
        self.today_sunset = 0
        self.today_sunrise = 0
        self.tomorrow_finedust = 0
        self.tomorrow_windchill = 0
        self.tomorrow_sunset = 0
        self.tomorrow_sunrise = 0

    def get(self, request):
        try:
            current = datetime.now()  # 매 시각 45분 이후부터 호출 가능 --> task에는 45분으로 등록
            base_date = current.strftime("%Y%m%d")
            base_time = current.strftime("%H%M")
            h = int(current.strftime("%H"))

            city = request.GET.get('city', '')  # 시
            district = request.GET.get('district', '')   # 군, 구
            region = Region.objects.filter(city=city, district=district)
            
            if len(region) == 0:
                return Response({'data': '', 'message': f'{city}, {district}에 대한 자원이 존재하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)
            region = region[0]

            # api1 ~ api5에 해당하는 객체들 가져오기
            api1 = Api1.objects.get(region=region)
            api2 = Api2.objects.get(region=region)
            api3 = Api3.objects.get(region=region)
            api4 = Api4.objects.get(regId=region.api5_code)
            api5 = Api5.objects.get(region=region)

            T1H = api1.T1H  # 기온
            REH = api1.REH  # 습도
            WSD = api1.WSD  # 풍속
            PTY = pty[api1.PTY]  # 강수형태
            RN1 = api1.RN1  # 1시간 강수량
            POP = ((api3.serializable_value(f'info_{h}')).replace(" ", "")).split('/')[4]  # (오늘) 강수 확률
            MAX = api3.info_day0_MAX  # 오늘 최고기온
            MIN = api3.info_day0_MIN  # 오늘 최저기온

            ## 1시간 강수량 데이터 단위 추가
            if RN1 != "0":
                RN1 += "mm"

            field = f'info_{h}'
            str = (api2.serializable_value(field)).replace(" ", "")  # 나중엔 없앨 공백 제거 코드
            f_list = str.split('/')
            SKY = f_list[1]  # 현재 하늘 상태

            d = {"기온": T1H, "하늘상태": SKY, "습도": REH, "풍속": WSD, "강수형태": PTY,
                "1시간강수량": RN1, "강수확률": POP, "최고기온": MAX, "최저기온": MIN}


            ## 메인 백그라운드 이미지 데이터 -> 맑음 / 구름많음 / 흐림 / ( 약한비 / 중간비 / 강한비 )
            today_weather_state = background_img(SKY, PTY, RN1)
            #######


            ## 코멘트 부분 추가 -> 이미지도 업로드 할 것!
            today_comments_detail = dict()
            today_comments_detail["메인"] = today_comment(region, self.today_windchill)
            today_comments_detail["습도"] = humidity(REH)  # 습도
            # today_comments_detail["습도"]["이미지url"] = humidity_img(REH)  # 습도 이미지
            today_comments_detail["강수"] = precipication(SKY, PTY, RN1)  # 강수
            today_comments_detail["강수"]["이미지url"] = precipication_img(SKY, PTY, RN1)  # 강수 이미지

            today_comments_detail["바람"] = wind(WSD)  # 바람
            # today_comments_detail["바람"]["이미지url"] = wind_img(WSD)  # 바람 이미지
            ## 이 부분 밑에 추가해주시면 될 것 같아요!!
            ########

            d1 = dict()
            for i in range(h, h + 6):  # 현재 시각 ~ 6 시간의 정보
                if i == 24:  # 00 ~ 23시까지의 정보만을 표현
                    break
                field = f'info_{i}'
                str = ((api2.serializable_value(field)).replace(" ", "")).split('/')  # 정보 4개 : 기온 / 하늘상태 / 강수형태 / 1시간강수량
                str.append(time_img(str[2], str[1]))
                d1[i] = str


            d2 = dict()
            if h + 6 < 24:  # 아직 오늘 날씨가 더 남아있으면 -> API3에서 가져오기 (기온, 하늘 상태, 강수 형태, 1시간 강수량 만 가져오기)
                for i in range(h + 6, 24):
                    field = f'info_{i}'
                    str = (api3.serializable_value(field)).replace(" ", "")
                    li = str.split('/')
                    new_li = []
                    new_li.append(li[0])  # 기온
                    new_li.append(li[1])  # 하늘 상태
                    new_li.append(li[3])  # 강수 형태
                    new_li.append(li[5])  # 1시간 강수량
                    new_li.append(time_img(li[3], li[1]))  # 이미지 추가
                    d2[i] = new_li

            ## 최소 12개 시간대 날씨 보여주기
            if len(d1)+len(d2) < 12:
                for i in range(24, 24+(12-len(d1)-len(d2))):
                    field = f'info_{i}'
                    str = (api3.serializable_value(field)).replace(" ", "")
                    li = str.split('/')
                    new_li = []
                    new_li.append(li[0])  # 기온
                    new_li.append(li[1])  # 하늘 상태
                    new_li.append(li[3])  # 강수 형태
                    new_li.append(li[5])  # 1시간 강수량
                    new_li.append(time_img(li[3], li[1]))  # 이미지 추가
                    d2[i] = new_li
            #########################

            # 딕셔너리 합치기 d1 = d1 + d2
            d1.update(d2)

            # 내일
            ## 내일 특정 h 시간에 대한 정보 제공
            tomm_li = ((api3.serializable_value(f'info_{h}')).replace(" ", "")).split('/')
            T1H = tomm_li[0]  # 기온 - 0
            REH = tomm_li[2]  # 습도 - 2
            WSD = tomm_li[6]  # 풍속 - 6
            PTY = tomm_li[3]  # 강수형태 - 3
            RN1 = tomm_li[5]  # 1시간 강수량- 5
            POP = tomm_li[4]  # (내일) 강수 확률 - 4

            MAX = api3.info_day1_MAX  # 내일 최고기온
            MIN = api3.info_day1_MIN  # 내일 최저기온

            d3 = {"기온": T1H, "하늘상태": SKY, "습도": REH, "풍속": WSD, "강수형태": PTY,
                "1시간강수량": RN1, "강수확률": POP, "최고기온": MAX, "최저기온": MIN}


            ## 메인 백그라운드 이미지 데이터 -> 맑음 / 구름많음 / 흐림 / ( 약한비 / 중간비 / 강한비 )
            tommorrow_weather_state = background_img(SKY, PTY, RN1)
            #######


            ## 코멘트 부분 추가
            tomorrow_comments_detail = dict()
            tomorrow_comments_detail["메인"] = tomorrow_comment(region, self.tomorrow_windchill)
            tomorrow_comments_detail["습도"] = humidity(REH)  # 습도
            # tomorrow_comments_detail["습도"]["이미지url"] = humidity_img(REH)  # 습도 이미지
            tomorrow_comments_detail["강수"] = precipication(SKY, PTY, RN1)  # 강수
            tomorrow_comments_detail["강수"]["이미지url"] = precipication_img(SKY, PTY, RN1)  # 강수 이미지

            tomorrow_comments_detail["바람"] = wind(WSD)  ## 바람
            # tomorrow_comments_detail["바람"]["이미지url"] = wind_img(WSD)  # 바람 이미지


            # 내일 00시 ~ 23시 정보
            d4 = dict()
            for i in range(24, 48):
                field = f'info_{i}'
                str = (api3.serializable_value(field)).replace(" ", "")
                li = str.split('/')
                new_li = []
                new_li.append(li[0])  # 기온
                new_li.append(li[1])  # 하늘 상태
                new_li.append(li[3])  # 강수 형태
                new_li.append(li[5])  # 1시간 강수량
                new_li.append(time_img(li[3], li[1]))  # 이미지 추가

                d4[i - 24] = new_li

            ##
            ## 이번주 ( day0 ~ day6 )
            ## day0 ~ day2 : api3 이용 - 오늘.내일.모래
            ## day3 ~ day6 : ap4, 5 이용

            # 필요한 정보:  (하늘상태), (강수확률), (최고/최저기온)
            # 오전/오후별 : 하늘상태, 강수확률
            # 하루별: 최고/최저기온

            sky0 = []
            pop0 = []
            sky1 = []
            pop1 = []
            sky2 = []
            pop2 = []
            for i in range(6, 12):  # 오전
                li = ((api3.serializable_value(f'info_{i}')).replace(" ", "")).split('/')
                sky0.append(li[1])
                pop0.append(li[4])

                li = ((api3.serializable_value(f'info_{i + 24}')).replace(" ", "")).split('/')
                sky1.append(li[1])
                pop1.append(li[4])

                li = ((api3.serializable_value(f'info_{i + 48}')).replace(" ", "")).split('/')
                sky2.append(li[1])
                pop2.append(li[4])

            SKY0_am = (collections.Counter(sky0)).most_common(1)[0][0]  # 하늘상태
            POP0_am = max(pop0)  # 강수확률
            SKY1_am = (collections.Counter(sky1)).most_common(1)[0][0]  # 하늘상태
            POP1_am = max(pop1)  # 강수확률
            SKY2_am = (collections.Counter(sky2)).most_common(1)[0][0]  # 하늘상태
            POP2_am = max(pop2)  # 강수확률

            sky0.clear()
            pop0.clear()
            sky1.clear()
            pop1.clear()
            sky2.clear()
            pop2.clear()

            for i in range(12, 22):  # 오후
                li = ((api3.serializable_value(f'info_{i}')).replace(" ", "")).split('/')
                sky0.append(li[1])
                pop0.append(li[4])

                li = ((api3.serializable_value(f'info_{i + 24}')).replace(" ", "")).split('/')
                sky1.append(li[1])
                pop1.append(li[4])

                li = ((api3.serializable_value(f'info_{i + 48}')).replace(" ", "")).split('/')
                sky2.append(li[1])
                pop2.append(li[4])

            SKY0_pm = (collections.Counter(sky0)).most_common(1)[0][0]  # 하늘상태
            POP0_pm = max(pop0)  # 강수확률
            SKY1_pm = (collections.Counter(sky1)).most_common(1)[0][0]  # 하늘상태
            POP1_pm = max(pop1)  # 강수확률
            SKY2_pm = (collections.Counter(sky2)).most_common(1)[0][0]  # 하늘상태
            POP2_pm = max(pop2)  # 강수확률

            d5 = {"0": {"오전하늘상태": SKY0_am, "오후하늘상태": SKY0_pm,
                        "오전하늘이미지": weekend_img(SKY0_am), "오후하늘이미지": weekend_img(SKY0_pm),
                        "오전강수확률": POP0_am, "오후강수확률": POP0_pm,
                        "최저기온": api3.info_day0_MIN, "최고기온": api3.info_day0_MAX},
                "1": {"오전하늘상태": SKY1_am, "오후하늘상태": SKY1_pm,
                        "오전하늘이미지": weekend_img(SKY1_am), "오후하늘이미지": weekend_img(SKY1_pm),
                        "오전강수확률": POP1_am, "오후강수확률": POP1_pm,
                        "최저기온": api3.info_day1_MIN, "최고기온": api3.info_day1_MAX},
                "2": {"오전하늘상태": SKY2_am, "오후하늘상태": SKY2_pm,
                        "오전하늘이미지": weekend_img(SKY2_am), "오후하늘이미지": weekend_img(SKY2_pm),
                        "오전강수확률": POP2_am, "오후강수확률": POP2_pm,
                        "최저기온": api3.info_day2_MIN, "최고기온": api3.info_day2_MAX},

                "3": {"오전하늘상태": api4.wf3Am, "오후하늘상태": api4.wf3Pm,
                        "오전하늘이미지": weekend_img(api4.wf3Am), "오후하늘이미지": weekend_img(api4.wf3Pm),
                        "오전강수확률": api4.rnSt3Am, "오후강수확률": api4.rnSt3Pm,
                        "최저기온": api5.taMin3, "최고기온": api5.taMax3},
                "4": {"오전하늘상태": api4.wf4Am, "오후하늘상태": api4.wf4Pm,
                        "오전하늘이미지": weekend_img(api4.wf4Am), "오후하늘이미지": weekend_img(api4.wf4Pm),
                        "오전강수확률": api4.rnSt4Am, "오후강수확률": api4.rnSt4Pm,
                        "최저기온": api5.taMin4, "최고기온": api5.taMax4},
                "5": {"오전하늘상태": api4.wf5Am, "오후하늘상태": api4.wf5Pm,
                        "오전하늘이미지": weekend_img(api4.wf5Am), "오후하늘이미지": weekend_img(api4.wf5Pm),
                        "오전강수확률": api4.rnSt5Am, "오후강수확률": api4.rnSt5Pm,
                        "최저기온": api5.taMin5, "최고기온": api5.taMax5},
                "6": {"오전하늘상태": api4.wf6Am, "오후하늘상태": api4.wf6Pm,
                        "오전하늘이미지": weekend_img(api4.wf6Am), "오후하늘이미지": weekend_img(api4.wf6Pm),
                        "오전강수확률": api4.rnSt6Am, "오후강수확률": api4.rnSt6Pm,
                        "최저기온": api5.taMin6, "최고기온": api5.taMax6}
                }

            # 데이터 넣기
            ## API1 - 5까지의 오늘 데이터 넣기
            response_today = {"배경이미지": today_weather_state.replace(' ', ''), "현재": d, "시간별정보": d1, "세부코멘트": today_comments_detail}
            ## API6 - 10까지의 오늘 데이터 넣기
            response_today.update(self.today(region).items())
            ### 코멘트 넣기
            response_today['세부코멘트'].update(self.today_comment())

            ## API1 - 5까지의 내일 데이터 넣기
            response_tomorrow = {"배경이미지": tommorrow_weather_state.replace(' ', ''), "현재": d3, "시간별정보": d4, "세부코멘트": tomorrow_comments_detail}
            ## API6 - 10까지의 내일 데이터 넣기
            response_tomorrow.update(self.tomorrow(region).items())
            ### 코멘트 넣기
            response_tomorrow['세부코멘트'].update(self.tomorrow_comment())

            return Response({"data": {"오늘": response_today, "내일": response_tomorrow,
                                    "이번주": d5, "업데이트 시간": api1.base_time}}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'/main : Error {e} -----------------------------')
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)

    def today(self, region):
        data = {}
        now = datetime.today()

        # api6
        print(region.api6_id)
        data['미세먼지'] = region.api6_id.pm10Grade1h
        self.today_finedust = data['미세먼지']

        # api7
        data['일몰일출'] = MainApi7TodaySerializer(region.api7).data
        self.today_sunset = data['일몰일출']['일몰']
        self.today_sunrise = data['일몰일출']['일출']

        # api8
        api8 = get_object_or_404(Api8, div_code=region.div_code)
        data['자외선지수'] = MainApi8TodaySerializer(api8).data['ultraviolet']

        # api9
        ## 현재 시간 데이터 찾기
        api9 = get_object_or_404(Api9, div_code=region.div_code)
        api9_temperature = api9.temperature.split('/')
        api9_basetime = api9.base_time
        now_hour = now.strftime("%H")
        index = int(now_hour) - int(api9_basetime)
        if index < 0:
            index = int(now_hour) + 6
        data['체감온도'] = api9_temperature[index]
        self.today_windchill = api9_temperature[index]

        # api10
        today_tem = region.api1.T1H
        yesterdat_tem = api_10()
        #yesterdat_tem = region.api1.T1H
        data['전날기온차이'] = round((float(today_tem) - float(yesterdat_tem)), 2)
        return data

    def tomorrow(self, region):
        data = {}
        now = datetime.now()

        # api6
        data['미세먼지'] = region.api6_id.pm10Value24
        self.tomorrow_finedust = data['미세먼지']

        # api7
        data['일몰일출'] = MainApi7TomorrowSerializer(region.api7).data
        self.tomorrow_sunset = data['일몰일출']['일몰']
        self.tomorrow_sunrise = data['일몰일출']['일출']

        # api8
        api8 = get_object_or_404(Api8, div_code=region.div_code)
        data['자외선지수'] = MainApi8TomorrowSerializer(api8).data['ultraviolet']

        # api9
        ## 현재 시간 데이터 찾기
        api9 = get_object_or_404(Api9, div_code=region.div_code)
        api9_temperature = api9.temperature.split('/')
        api9_basetime = api9.base_time
        now_hour = now.strftime("%H")
        index = int(now_hour) - int(api9_basetime)
        if index < 0:
            index = int(now_hour) + 6
        data['체감온도'] = api9_temperature[index + 24]
        self.tomorrow_windchill = api9_temperature[index]

        # api10
        ## 현재 시간 데이터 찾기
        api3_data = Api3Serializer(region.api3).data
        now_hour = int(now.strftime("%H"))
        today_data = Api3Serializer(region.api3).data['info_' + str(now_hour + 24)]
        today_tem = today_data.split('/')[0]

        yesterdat_tem = region.api1.T1H
        data['전날기온차이'] = round((float(today_tem) - float(yesterdat_tem)), 2)
        return data

    def today_comment(self):
        comments_detail = dict()
        comments_detail['미세먼지'] = finedust(self.today_finedust)
        comments_detail['체감온도'] = windchill(self.today_windchill)
        comments_detail['일몰일출'] = sun(False, self.today_sunrise, self.today_sunset)

        return comments_detail

    def tomorrow_comment(self):
        comments_detail = dict()
        comments_detail['미세먼지'] = finedust(self.tomorrow_finedust)
        comments_detail['체감온도'] = windchill(self.tomorrow_windchill)
        comments_detail['일몰일출'] = sun(True, self.tomorrow_sunrise, self.tomorrow_sunset)

        return comments_detail


## 검색 기능
# 요청받은 지명값 파싱하기 이후 city, district 에서 찾기
class SearchView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        imgs = {
            "비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/지역검색시 날씨일러스트/비.png",
            "맑음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/지역검색시 날씨일러스트/맑음.png",
            "구름많음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/지역검색시 날씨일러스트/구름많음.png",
            "흐림": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/지역검색시 날씨일러스트/흐림.png"
        }

        try:
            str = request.data["data"]
            words = str.split(" ")  # 공백을 기준으로 파싱하기

            if len(words) == 1:  # city 또는 district 만 입력받은 경우
                regions = Region.objects.filter(city__contains=words[0]).values()  # 검색한 것이 -> city 인 경우

                if len(regions) == 0:
                    regions = Region.objects.filter(district__contains=words[0]).values()  # 검색한 것이 -> district 인 경우

            elif len(words) > 1:  # city, district 모두 입력받은 경우 (공백 기준 문자열 2개일 경우)
                regions = Region.objects.filter(city__contains=words[0]).filter(district__contains=words[1]).values()
            else:
                return Response({"data": ""}, status=status.HTTP_200_OK)

            # 해당 objs의 기온과 하늘상태 불러오기 // 기온 -> api2 이용
            d = {}
            h = int(datetime.now().strftime("%H"))
            for region in regions:  # obj는 Region 객체
                print(region)
                key = region["city"] + " " + region["district"]
                print(key)
                api1 = Api1.objects.get(region=region["id"])
                tem = api1.T1H  # 현재 기온
                pty = api1.PTY  # 강수 형태 (코드값으로 받음)

                # 강수 형태 -> 없음 (맑음, 구름많음, 흐림) // 있음 -> 비 기준으로 1차 판별

                # 강수 형태 "없음" -> "하늘상태"로 판별
                if pty == "0":
                    api2 = Api2.objects.get(region=region["id"])
                    field = f'info_{h}'
                    sky = (((api2.serializable_value(field)).replace(" ", "")).split('/'))[1]  # 하늘상태
                    img_url = imgs[sky]

                # 강수 형태 있음 -> "비"로 판단
                else:
                    img_url = imgs["비"]

                d[key] = {"이미지url": img_url, "기온": tem}

            return Response({"data": d}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 경도, 위도 요청시, 카카오 로컬 API를 이용하여 행정구역 데이터 반환하는 API
class FindRegionView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            # 데이터 가져오기
            longitude = request.data["longitude"] # 경도
            latitude = request.data["latitude"] # 위도
            print(f'/find/region : GET {longitude} {latitude} ——————————————')

            # 시, 군구 찾기
            city, district = self.get_region_data(longitude, latitude)
            ## district 띄어쓰기가 있는 경우 없애기
            district = district.replace(' ', '')
            print(city, district)

            # 존재하는 지역인지 확인하기
            region = Region.objects.filter(city=city, district=district)
            
            if len(region) == 0: # 존재하지 않는 지역인 경우
                return Response({'data': '', 'message': f'{city}, {district}에 대한 자원이 존재하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)
            
            # 응답 보내기
            data = {
                'city': city,
                'distinct': district
            }
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'/find/region : Error {e} -----------------------------')
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)


    # 위도, 경도에 대한 행정구역 정보를 kakao API로 요청하는 함수
    def get_region_data(self, longitude, latitude):
        url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'

        # request 요청하기
        ## header 생성하기
        rest_api_key = env('kakao_client_id')
        headers={
            "Authorization": f"KakaoAK {rest_api_key}",
        }

        ## 요청할 데이터 구성하기
        params = {
            'x': longitude,
            'y': latitude,
            'input_coord': 'WGS84',
            'output_coord': 'WGS84'
        }

        try:
            response = requests.get(url, params=params, headers=headers)

            # 응답처리하기
            possible_data = set()
            for ele in response.json()['documents']:
                possible_data.add((ele['region_1depth_name'], ele['region_2depth_name']))

            return list(possible_data)[0]

        except requests.Timeout:
            print(f'api_10: Timeout: -----------------------------')
        except requests.ConnectionError:
            print(f'api_10: ConnectionError: -----------------------------')
        except Exception as e:
            print(f'/kakao 로컬 API : Error {e} -----------------------------')
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)

