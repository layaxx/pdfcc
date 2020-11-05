from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse', views.analyse, name='analyse'),
    path('process', views.process, name='process'),
]
