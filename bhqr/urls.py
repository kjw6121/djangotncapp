from django.contrib import admin
from django.urls import path, include
from . import views



from django.contrib.auth.views import LoginView, LogoutView

from bhqr.views import *

app_name = "bhqr"
urlpatterns = [
    path('', index, name="index"),
]