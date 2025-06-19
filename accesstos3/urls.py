# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload-from-access/', views.upload_file_from_access, name='upload_from_access'),
    # ... 다른 URL들 ...
]