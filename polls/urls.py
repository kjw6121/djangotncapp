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
    path('post_edit/<str:id>', edit, name="post_edit"),
    path('detail/<str:id>', detail, name="detail"),
    path('delete/<str:id>', delete, name="delete"),
    path('login/', LoginView.as_view(template_name="polls/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('post_new/', post_new, name='post_new'),
    path('post_update/<str:id>', post_update, name='post_update'),
    path('unloading/<str:id>', unloading, name='unloading'),
    path('loading/<str:id>', loading, name='loading'),
    path('boxtrstock/', boxtrstock, name='boxtrstock'),
    path('boxtrstatus/', boxtrstatus, name='boxtrstatus'),
    path('post_rbkb/', post_rbkb, name='post_rbkb'),
    path('update_rbkb/', update_rbkb, name='update_rbkb'),

    
    
    ]