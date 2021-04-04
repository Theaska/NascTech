from django.urls import path
from .views import MainViewAPI, MainViewDetail

app_name = 'main'

urlpatterns = [
    path('', MainViewAPI.as_view(), name='index'),
    path('func_<str:name>', MainViewDetail.as_view(), name='detail'),
]