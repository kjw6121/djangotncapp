# photo_upload/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Access에서 QR 코드를 통해 접근할 URL
    # 예: https://etnclogis.com/upload-photo-to-s3/?filename=my_image.jpg
    path('upload-photo-to-s3/', views.upload_photo_from_phone, name='upload_photo_from_phone'),
]