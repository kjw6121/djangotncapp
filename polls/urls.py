from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from polls.views import *

app_name = "polls"
urlpatterns = [
    path('', home, name="home"), 
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('edit/<str:id>', edit, name="edit"),
    path('update/<str:id>', update, name="update"),
    path('detail/<str:id>', detail, name="detail"),
    path('delete/<str:id>', delete, name="delete"),
    path('login/', LoginView.as_view(template_name="polls/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    
    
    ]