from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/react', views.analyse, name='analyse'),
    path('ajax/process', views.process, name='process'),
]
