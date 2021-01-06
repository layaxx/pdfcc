from django.shortcuts import redirect
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/react', views.analyse, name='analyse'),
    path('ajax/process', views.process, name='process'),
    re_path(r'', lambda request: redirect('/', permanent=True)),
]
