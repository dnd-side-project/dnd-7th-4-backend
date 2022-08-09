from django.shortcuts import render

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .api_test.api_6 import api_6
from .api_test.api_7 import api_7

# Swagger test용 - 이후 삭제
class TestView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("Swagger 연동 테스트")