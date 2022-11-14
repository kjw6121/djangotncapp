from django.contrib import admin
from django.urls import path

from polls.views import *


urlpatterns = [
    ##path('', views.index, name='index'),
    path('', index, name="index"), 
    ##path('home/', home, name="home"), 
    path('hello/', hello, name="hello"),
    path('new/', new, name="new"),
    path('<str:id>', detail, name="detail"),
    path('create/', create, name="create"),
    path('edit/<str:id>', edit, name="edit"),
    path('update/<str:id>', update, name="update"),
    path('delete/<str:id>', delete, name="delete"),
]