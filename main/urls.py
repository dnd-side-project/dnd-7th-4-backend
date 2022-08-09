from django.urls import path

from . import views

urlpatterns = [
    # path('main', ),  # 메인 페이지
    path('api/test_swagger/', views.TestView.as_view(), name='test_swagger'),
    path('api/api6/', views.api_6)
]