from django.urls import path

from . import views

urlpatterns = [
    path('main', views.MainView.as_view()),  # 메인 페이지
    path('api/test_swagger/', views.TestView.as_view(), name='test_swagger'),
    path('api/api6/', views.api_6),
    path('api/api7/', views.api_7),
    path('api/api8/', views.api_8),
    path('api/api9/', views.api_9),
]