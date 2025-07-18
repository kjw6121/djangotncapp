from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from mysite.views import *

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('bhqr/', include('bhqr.urls')),
    path('outbound/', include('outbound.urls')),
    path('image_recognition/', include('image_recognition.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('main/', main, name='main'),
    path('accesstos3/', include('accesstos3.urls')),
    path('qr/', include('qrcode_api.urls')),
    path('photo/', include('photo_upload.urls')),

    path('qr-upload/', include('qr_upload.urls')), # <--- 이 부분 변경
 ]
