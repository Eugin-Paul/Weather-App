
from django.urls import path
from . import views

urlpatterns = [
        path('index', views.index, name = 'index'),
        # path('add_weather', views.add_weather, name = 'add_weather'),
        path('clear', views.clear, name = 'clear'),

        ]
