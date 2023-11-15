from django.contrib import admin
from django.urls import path, include
from . import views



from django.contrib.auth.views import LoginView, LogoutView

from bhqr.views import *

app_name = "bhqr"
urlpatterns = [
    path('index', index, name="index"),
    path('error_page/', error_page, name='error_page'),
    path('save_scan_data/', save_scan_data, name='save_scan_data'),
    path('today_data/', today_data, name='today_data'),
]