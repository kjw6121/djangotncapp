from django.contrib import admin
from django.urls import path, include
from . import views



from django.contrib.auth.views import LoginView, LogoutView

from bhqr.views import *

app_name = "bhqr"
urlpatterns = [
    path('', index, name="index"),
    path('error_page/', error_page, name='error_page'),
]