from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse', views.analyse, name='analyse'),
    path('process', views.process, name='process'),
    path('result', views.result, name='result'),
    path('ajax', views.ajax, name='ajax')
]
