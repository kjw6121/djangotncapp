from django.contrib import admin
from django.urls import path, include
from . import views



from django.contrib.auth.views import LoginView, LogoutView

from outbound.views import *

app_name = 'outbound'
urlpatterns = [
    path('index/', index, name='index'),
    path('mainhu/', mainhu, name='mainhu'),
    path('save_scanned_data/', save_scanned_data, name='save_scanned_data'),
]