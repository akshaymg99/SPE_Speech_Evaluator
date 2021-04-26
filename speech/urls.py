from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('record', views.record, name='record'),
    path('result', views.result, name='result')
]
