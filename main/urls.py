from django.urls import path

from . import views

urlpatterns = [
    path('main', views.MainView.as_view()),  # 메인 페이지
    #path('kakao_alarm', views.send_kakao_alarm), # 카카오톡 알림 서비스 테스트 URL

    path('search', views.SearchView.as_view()),  # 검색,
    path('find/region', views.FindRegionView.as_view()), # 행정구역반환
]