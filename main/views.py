from django.shortcuts import render
from django.shortcuts import get_object_or_404

from drf_yasg.utils       import swagger_auto_schema

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

from .api_test.api_6 import api_6
from .api_test.api_7 import api_7
from .api_test.api_8 import api_8
from .api_test.api_9 import api_9
from .api_test.api_10 import api_10

# Swagger test용 - 이후 삭제
class TestView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("Swagger 연동 테스트")

# 메인 기능
class MainView(APIView):

    # 해당 지역에 대한 데이터 제공
    def post(self, request):
        print(f'MainView: post {request.data} -------------------')
        region = Region.objects.get(city = request.data['city'], district = request.data['district'])
        data = {}

        # 오늘 페이지 데이터 생성하기
        data['today'] = self.today(region)


        # 내일 페이지 데이터 생성하기
        data['tomorrow'] = self.tomorrow(region)

        # 이번주 페이지 데이터 생성하기
        #data['week']

        return Response(data)
    
    def today(self, region) :
        data = {}
        
        # api6
        data['finddust'] = MainApi6TodaySerializer(region.api6_id).data

        # api7
        data['sun'] = MainApi7TodaySerializer(region.api7).data

        return data

    def tomorrow(self, region) :
        data = {}

        # api6
        data['finddust'] = MainApi6TomorrowSerializer(region.api6_id).data

        # api7
        data['sun'] = MainApi7TomorrowSerializer(region.api7).data

        return data




        