# qr_upload/urls.py
from django.urls import path
from . import views

app_name = 'qr_upload' # 앱 이름을 정의하여 reverse()에서 충돌 방지

urlpatterns = [
    # WMS 등에서 임시 링크를 생성하기 위해 호출할 API URL
    path('generate-link/', views.generate_temp_upload_link, name='generate_temp_upload_link'),

    # QR 코드에 삽입될 실제 업로드 URL (토큰 포함)
    path('upload/<uuid:token>/', views.upload_photo_from_qr_link, name='upload_photo_from_qr_link'),

    # QR 코드 업로드 성공 시 리다이렉트될 페이지 URL
    path('success/', views.qr_upload_success_view, name='qr_upload_success_page'),
]
