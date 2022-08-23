from django.urls import path

from . import views

urlpatterns = [
    # path('kakao', views.front),
    path('kakao/oauth', views.back),
    path('kakao/logout', views.logout),

    path('login', views.login),  # 백엔드 테스트용

    # 유저 관련 기능들
    path('region', views.RegionView.as_view()),  # 사용자의 지역 생성, 삭제
    path('alarm', views.KakaoAlarmView.as_view()), # 카카오톡 알림 설정 및 설정 취소
    path('myregions', views.RegisterRegionView.as_view()),  # 등록한 지역 가져오기
    path('alarm/region', views.KakaoRegionView.as_view()) # 카카오톡 알림 지역 설정
]