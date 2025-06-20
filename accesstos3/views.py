# your_app/views.py
from django.views.decorators.csrf import csrf_exempt # CSRF 보호 비활성화 (보안 주의!)
from django.http import JsonResponse, HttpResponseBadRequest, Http404
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


import mimetypes # 파일 MIME 타입을 추론하기 위함
import os # 파일명에서 기본 이름과 확장자를 분리하기 위함
from storages.backends.s3boto3 import S3Boto3Storage

default_storage = S3Boto3Storage()
logger = logging.getLogger(__name__)

# 기존 upload_file_from_access 함수는 그대로 둡니다.

@csrf_exempt
def download_file_from_s3(request, filename): # URL에서 filename을 인자로 받습니다.
    # S3에 저장된 실제 파일명은 인코딩되지 않은 형태로 와야 합니다.
    # Access VBA에서 X-Filename 헤더를 보낼 때처럼 URL 인코딩 문제가 있을 수 있으므로
    # URL에서 받은 filename이 이미 깨진 한글이라면 여기서 다시 디코딩 시도 필요.
    # 하지만 S3에 UUID로 저장했다면, filename은 영문 UUID일 것이므로 이 과정은 필요 없습니다.
    
    # 만약 Access에서 넘어온 filename이 URL 인코딩되어 있다면, 여기서 디코딩해야 합니다.
    # from urllib.parse import unquote
    # s3_actual_filename = unquote(filename) # URL 디코딩
    s3_actual_filename = filename # S3에 저장된 파일명 (UUID_파일명.확장자 형태라고 가정)


    logger.info(f"Attempting to download file from S3: '{s3_actual_filename}'")

    if not default_storage.exists(s3_actual_filename):
        logger.error(f"File not found on S3: '{s3_actual_filename}'")
        raise Http404("File not found.")

    try:
        # S3에서 파일 열기
        with default_storage.open(s3_actual_filename, 'rb') as s3_file:
            # MIME 타입 추론 (파일 확장자를 기반으로)
            mime_type, _ = mimetypes.guess_type(s3_actual_filename)
            if not mime_type:
                mime_type = 'application/octet-stream' # 기본 바이너리 타입

            # HTTP 응답 생성
            response = HttpResponse(s3_file.read(), content_type=mime_type)
            
            # 다운로드 파일명 설정 (Access에서 받아온 원본 한글 파일명으로 설정)
            # 만약 DB에 원본 파일명이 저장되어 있다면, 그 이름을 사용합니다.
            # 예시:
            # try:
            #     file_meta = UploadedFile.objects.get(s3_filename=s3_actual_filename)
            #     download_name = file_meta.original_filename # DB에 저장된 원본 한글 파일명
            # except UploadedFile.DoesNotExist:
            #     download_name = s3_actual_filename # DB에 없으면 S3 실제 파일명 사용
            download_name = s3_actual_filename # 현재는 S3 실제 파일명으로 다운로드 (영문)

            # 한글 파일명 지원을 위해 인코딩 필요
            # from urllib.parse import quote
            # encoded_download_name = quote(download_name.encode('utf-8')) # UTF-8로 인코딩 후 URL 쿼트

            # Content-Disposition 헤더 설정: 파일을 다운로드하도록 브라우저에 지시
            # filename*=UTF-8''filename.ext 구문은 RFC 6266에 따라 한글 파일명을 지원
            response['Content-Disposition'] = f"attachment; filename*=UTF-8''{download_name}"
            # response['Content-Disposition'] = f"attachment; filename=\"{encoded_download_name}\"" # 구식 브라우저 호환

            logger.info(f"Successfully streamed file '{s3_actual_filename}' for download.")
            return response

    except Exception as e:
        logger.error(f"Error streaming file from S3 '{s3_actual_filename}': {e}")
        return HttpResponse(f"Error downloading file: {e}", status=500)