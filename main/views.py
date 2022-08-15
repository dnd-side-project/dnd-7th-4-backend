from django.shortcuts import render, get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from datetime import datetime
import collections

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from main.models import *
from .serializers import *

from .api_test.api_6 import api_6
from .api_test.api_7 import api_7
from .api_test.api_8 import api_8
from .api_test.api_9 import api_9
from .api_test.api_10 import api_10

from .comment_callback_directory.comments import *


# Swagger test용 - 이후 삭제
class TestView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("Swagger 연동 테스트")

pty = {'0': '없음', '1': '비', '2': '비/눈', '5': '빗방울',  # 강수형태코드
           '6': '빗방울눈날림', '7': '눈날림'}


# 메인 화면 - 오늘, 내일, 이번주
class MainView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        current = datetime.now()  # 매 시각 45분 이후부터 호출 가능 --> task에는 45분으로 등록
        base_date = current.strftime("%Y%m%d")
        base_time = current.strftime("%H%M")
        h = int(current.strftime("%H"))

        city = request.data["city"]  # 시
        district = request.data["district"]  # 군, 구
        region = Region.objects.get(city=city, district=district)

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

        field = f'info_{h}'
        str = (api2.serializable_value(field)).replace(" ", "")  # 나중엔 없앨 공백 제거 코드
        f_list = str.split('/')
        SKY = f_list[1]  # 현재 하늘 상태

        d = {"기온": T1H, "하늘상태": SKY, "습도": REH, "풍속": WSD, "강수형태": PTY,
             "1시간강수량": RN1, "강수확률": POP, "최고기온": MAX, "최저기온": MIN}

        ## 코멘트 부분 추가
        comments_detail = dict()
        comments_detail["습도"] = humidity(REH)  # 습도
        comments_detail["강수"] = precipication(RN1)  # 강수
        comments_detail["바람"] = wind(WSD) ## 바람
        ## 이 부분 밑에 추가해주시면 될 것 같아요!!
        ########

        d1 = dict()
        for i in range(h, h+6):  # 현재 시각 ~ 6 시간의 정보
            if i == 24:  # 00 ~ 23시까지의 정보만을 표현
                break
            field = f'info_{i}'
            str = (api2.serializable_value(field)).replace(" ", "")
            d1[i] = str.split('/')

        d2 = dict()
        if h+6 < 24:  # 아직 오늘 날씨가 더 남아있으면 -> API3에서 가져오기 (기온, 하늘 상태, 강수 형태, 1시간 강수량 만 가져오기)
            for i in range(h+6, 24):
                field = f'info_{i}'
                str = (api3.serializable_value(field)).replace(" ", "")
                li = str.split('/')
                new_li = []
                new_li.append(li[0])
                new_li.append(li[1])
                new_li.append(li[3])
                new_li.append(li[5])
                d2[i] = new_li

        # 딕셔너리 합치기 d1 = d1 + d2
        d1.update(d2)

        ##
        ## 내일
        # 내일 특정 h 시간에 대한 정보 제공
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


        # 내일 00시 ~ 23시 정보
        d4 = dict()
        for i in range(24, 48):
            field = f'info_{i}'
            str = (api3.serializable_value(field)).replace(" ", "")
            li = str.split('/')
            new_li = []
            new_li.append(li[0])
            new_li.append(li[1])
            new_li.append(li[3])
            new_li.append(li[5])
            d4[i-24] = new_li

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

            li = ((api3.serializable_value(f'info_{i+24}')).replace(" ", "")).split('/')
            sky1.append(li[1])
            pop1.append(li[4])

            li = ((api3.serializable_value(f'info_{i+48}')).replace(" ", "")).split('/')
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

            li = ((api3.serializable_value(f'info_{i+24}')).replace(" ", "")).split('/')
            sky1.append(li[1])
            pop1.append(li[4])

            li = ((api3.serializable_value(f'info_{i+48}')).replace(" ", "")).split('/')
            sky2.append(li[1])
            pop2.append(li[4])


        SKY0_pm = (collections.Counter(sky0)).most_common(1)[0][0]  # 하늘상태
        POP0_pm = max(pop0)  # 강수확률
        SKY1_pm = (collections.Counter(sky1)).most_common(1)[0][0]  # 하늘상태
        POP1_pm = max(pop1)  # 강수확률
        SKY2_pm = (collections.Counter(sky2)).most_common(1)[0][0]  # 하늘상태
        POP2_pm = max(pop2)  # 강수확률

        d5 = {"0": {"오전 하늘상태": SKY0_am, "오후 하늘상태": SKY0_pm,
                   "오전 강수확률": POP0_am, "오후 강수확률": POP0_pm,
                   "최저기온": api3.info_day0_MIN, "최고기온": api3.info_day0_MAX},
             "1": {"오전 하늘상태": SKY1_am, "오후 하늘상태": SKY1_pm,
                   "오전 강수확률": POP1_am, "오후 강수확률": POP1_pm,
                   "최저기온": api3.info_day1_MIN, "최고기온": api3.info_day1_MAX},
             "2": {"오전 하늘상태": SKY2_am, "오후 하늘상태": SKY2_pm,
                   "오전 강수확률": POP2_am, "오후 강수확률": POP2_pm,
                   "최저기온": api3.info_day2_MIN, "최고기온": api3.info_day2_MAX},

             "3": {"오전 하늘상태": api4.wf3Am, "오후 하늘상태": api4.wf3Pm,
                   "오전 강수확률": api4.rnSt3Am, "오후 강수확률": api4.rnSt3Pm,
                   "최저기온": api5.taMin3, "최고기온": api5.taMax3},
             "4": {"오전 하늘상태": api4.wf4Am, "오후 하늘상태": api4.wf4Pm,
                   "오전 강수확률": api4.rnSt4Am, "오후 강수확률": api4.rnSt4Pm,
                   "최저기온": api5.taMin4, "최고기온": api5.taMax4},
             "5": {"오전 하늘상태": api4.wf5Am, "오후 하늘상태": api4.wf5Pm,
                   "오전 강수확률": api4.rnSt5Am, "오후 강수확률": api4.rnSt5Pm,
                   "최저기온": api5.taMin5, "최고기온": api5.taMax5},
             "6": {"오전 하늘상태": api4.wf6Am, "오후 하늘상태": api4.wf6Pm,
                   "오전 강수확률": api4.rnSt6Am, "오후 강수확률": api4.rnSt6Pm,
                   "최저기온": api5.taMin6, "최고기온": api5.taMax6}
             }

        # 데이터 넣기
        ## 오늘 데이터 넣기
        response_today = {"현재": d, "시간별 정보": d1}
        for k, v in self.today(region).items():
            response_today[k] = v
        
        ## 내일 데이터 넣기
        response_tomorrow = {"내일현재": d3, "시간별 정보": d4}
        for k, v in self.tomorrow(region).items():
            response_tomorrow[k] = v

        return Response({"data": {"오늘": response_today, "세부 코멘트": comments_detail, "내일": response_tomorrow,
                         "이번주": d5}}, status=status.HTTP_200_OK)

    def today(self, region) :
        data = {}
        now = datetime.today()
        
        # api6
        data['미세먼지'] = MainApi6TodaySerializer(region.api6_id).data

        # api7
        data['일몰일출'] = MainApi7TodaySerializer(region.api7).data

        # api8
        api8 = get_object_or_404(Api8, div_code = region.div_code)
        data['자외선지수'] = MainApi8TodaySerializer(api8).data['ultraviolet']

        # api9
        ## 현재 시간 데이터 찾기
        api9 = get_object_or_404(Api9, div_code = region.div_code)
        api9_temperature = api9.temperature.split('/')
        api9_basetime = api9.base_time
        now_hour = now.strftime("%H")
        index = int(now_hour) - int(api9_basetime)
        if index < 0:
            index = int(now_hour) + 6
        data['체감온도'] = api9_temperature[index]

        # api10
        today_tem = region.api1.T1H
        yesterdat_tem = api_10()
        data['전날기온차이'] = str(float(today_tem) - float(yesterdat_tem))[:4]
        print(data)
        return data

    def tomorrow(self, region) :
        data = {}
        now = datetime.now()

        # api6
        data['미세먼지'] = MainApi6TomorrowSerializer(region.api6_id).data

        # api7
        data['일몰일출'] = MainApi7TomorrowSerializer(region.api7).data

        # api8
        api8 = get_object_or_404(Api8, div_code = region.div_code)
        data['자외선지수'] = MainApi8TomorrowSerializer(api8).data['ultraviolet']

        # api9
        ## 현재 시간 데이터 찾기
        api9 = get_object_or_404(Api9, div_code = region.div_code)
        api9_temperature = api9.temperature.split('/')
        api9_basetime = api9.base_time
        now_hour = now.strftime("%H")
        index = int(now_hour) - int(api9_basetime)
        if index < 0:
            index = int(now_hour) + 6
        data['체감온도'] = api9_temperature[index+24]

        # api10
        ## 현재 시간 데이터 찾기
        api3_data = Api3Serializer(region.api3).data
        now_hour = int(now.strftime("%H"))
        today_data = Api3Serializer(region.api3).data['info_'+str(now_hour+24)]
        today_tem = today_data.split('/')[0]

        yesterdat_tem = region.api1.T1H
        data['전날기온차이'] = str(float(today_tem) - float(yesterdat_tem))[:4]
        print(data)
        return data



## 검색 기능
# 요청받은 지명값 파싱하기 이후 city, district 에서 찾기
class SearchView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        str = request.data["data"]
        words = str.split(" ")  # 공백을 기준으로 파싱하기

        if len(words) == 1:  # city 또는 district 만 입력받은 경우
            objs = Region.objects.filter(city__contains=words[0]).values()  # 검색한 것이 -> city 인 경우

            if len(objs)==0:
                objs = Region.objects.filter(district__contains=words[0]).values()  # 검색한 것이 -> district 인 경우

        elif len(words) > 1:  # city, district 모두 입력받은 경우 (공백 기준 문자열 2개일 경우)
            objs = Region.objects.filter(city__contains=words[0]).filter(district__contains=words[1]).values()
        else:
            return Response({"data": ""}, status=status.HTTP_200_OK)

        # 해당 objs의 기온과 하늘상태 불러오기 // 기온 -> api2 이용
        d = {}
        h = int(datetime.now().strftime("%H"))
        for obj in objs:  # obj는 Region 객체
            print(obj)
            key = obj["city"] + " " + obj["district"]
            print(key)
            api2 = Api2.objects.get(region=obj["id"])
            sky = (((api2.serializable_value(f'info_{h}')).replace(" ", "")).split('/'))[1]  # 현재 하늘상태
            tem = (((api2.serializable_value(f'info_{h}')).replace(" ", "")).split('/'))[0]  # 현재 기온
            d[key] = {"하늘상태": sky, "기온": tem}

        return Response({"data": d}, status=status.HTTP_200_OK)