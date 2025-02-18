from django.contrib import admin
from django.urls import path, include
from . import views



from django.contrib.auth.views import LoginView, LogoutView

from image_recognition.views import *

app_name = 'image_recognition'
urlpatterns = [
    path('/upload_image', upload_image, name='upload_image'),
]