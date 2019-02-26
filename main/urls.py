
from django.contrib import admin
from django.urls import path, include
from main.views import MainView

app_name = 'main'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]
