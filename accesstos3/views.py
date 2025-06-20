# your_app/views.py
from django.views.decorators.csrf import csrf_exempt # CSRF 보호 비활성화 (보안 주의!)
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)

@csrf_exempt # Access에서 POST 요청 시 CSRF 토큰을 보내기 어려우므로 일시적으로 비활성화
def upload_file_from_access(request):
    if request.method == 'POST':
        # Access에서 보낸 파일 데이터를 처리
        # Access VBA에서 어떻게 데이터를 보내는지에 따라 이 부분은 달라질 수 있습니다.
        # 예시: 파일 내용을 raw body로 보낸 경우
        if request.body:
            file_name = request.META.get('HTTP_X_FILENAME', 'uploaded_from_access.bin') # 커스텀 헤더로 파일 이름 받기


            # --- 디버깅을 위한 추가 코드 ---
            logger.info(f"Received file_name from Access: '{file_name}'")
            # --- 디버깅을 위한 추가 코드 끝 ---


            content_type = request.META.get('CONTENT_TYPE', 'application/octet-stream')

            try:
                # ContentFile로 래핑하여 default_storage.save()에 전달
                file_path_on_s3 = default_storage.save(file_name, ContentFile(request.body, name=file_name))
                logger.info(f"File '{file_name}' uploaded to S3: {file_path_on_s3}")
                return JsonResponse({'status': 'success', 's3_path': file_path_on_s3})
            except Exception as e:
                logger.error(f"Error uploading file to S3: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return HttpResponseBadRequest("No file data received.")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")
# Create your views here.
