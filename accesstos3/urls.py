# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload-from-access/', views.upload_file_from_access, name='upload_from_access'),
    path('download/<path:filename>/', views.download_file_from_s3, name='download_from_s3'),
]
    # ... 다른 URL들 ...