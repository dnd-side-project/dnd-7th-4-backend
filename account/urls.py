from django.urls import path

from . import views

urlpatterns = [
    # path('kakao', views.front),
    path('kakao/oauth', views.back),
    path('kakao/logout', views.logout),

    path('login', views.login),  # 백엔드 테스트용
    path('alarm', views.KakaoAlarmView.as_view()), # 카카오톡 알림 설정 및 설정 취소
]