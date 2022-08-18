from django.urls import path

from . import views

urlpatterns = [
    path('main', views.MainView.as_view()),  # 메인 페이지
    path('api/api6/', views.api_6),
    path('api/api7/', views.api_7),
    path('api/api8/', views.api_8),
    path('api/api9/', views.api_9),

    path('search', views.SearchView.as_view()),  # 검색,
    path('region', views.RegionView.as_view()),  # 사용자의 지역 생성, 삭제
]