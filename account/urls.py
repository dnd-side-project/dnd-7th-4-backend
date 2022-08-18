from django.urls import path

from . import views

urlpatterns = [
    path('kakao', views.front),
    path('kakao/oauth', views.back),
    path('kakao/logout', views.logout),

    path('login', views.login),  # 백엔드 테스트용
]