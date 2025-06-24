# photo_upload/views.py
import logging
import os
import boto3 # S3 직접 연동을 위해 boto3 사용 (django-storages가 내부적으로 사용)

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # 모바일 웹 페이지에서는 CSRF 토큰 처리가 번거로우므로 비활성화 (보안 주의!)
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage # django-storages S3 백엔드 사용


logger = logging.getLogger(__name__)

# S3Boto3Storage 인스턴스를 전역적으로 생성하여 재사용 (옵션)
# settings.py에 DEFAULT_FILE_STORAGE가 설정되어 있다면 필요 없을 수도 있습니다.
s3_storage_instance = S3Boto3Storage()


@csrf_exempt # CSRF 토큰 검증을 비활성화. 실제 운영 환경에서는 보안 강화를 고려해야 합니다.
def upload_photo_from_phone(request):
    """
    GET 요청: 사진 촬영 웹 페이지를 렌더링하고, QR 코드에서 받은 파일명을 전달합니다.
    POST 요청: 스마트폰에서 촬영된 사진 파일을 받아 S3에 업로드합니다.
    """
    if request.method == 'GET':
        # QR 코드 스캔 시 접속. URL 파라미터에서 파일명을 가져옵니다.
        # 예: /upload-photo/?filename=my_document.jpg
        filename_from_qr = request.GET.get('filename', 'untitled_photo') # 기본값 설정
        
        context = {
            'filename': filename_from_qr,
            'upload_url': request.path # POST 요청을 보낼 현재 뷰의 URL (폼 action)
        }
        return render(request, 'photo_upload/upload_photo.html', context)

    elif request.method == 'POST':
        # 스마트폰에서 촬영된 사진 파일 (input type="file"의 name이 'photo')
        uploaded_file = request.FILES.get('photo')
        # 숨겨진 필드로 전달된 최종 S3 파일명 (Access에서 QR 코드에 넣은 이름)
        s3_target_filename = request.POST.get('filename')

        if not uploaded_file:
            logger.error("POST request received without 'photo' file.")
            return JsonResponse({'status': 'error', 'message': '사진 파일을 찾을 수 없습니다.'}, status=400)
        
        if not s3_target_filename:
            logger.error("POST request received without 'filename' for S3 target.")
            return JsonResponse({'status': 'error', 'message': '저장할 파일명을 찾을 수 없습니다.'}, status=400)

        try:
            # S3에 저장할 최종 파일명 결정
            # Access에서 받은 파일명(s3_target_filename)을 그대로 사용하되, 
            # 확장자가 없다면 업로드된 파일의 확장자를 붙여줍니다.
            name_part, ext_part = os.path.splitext(s3_target_filename)
            if not ext_part: # 파일명에 확장자가 없다면
                original_file_name, original_file_ext = os.path.splitext(uploaded_file.name)
                s3_target_filename = f"{name_part}{original_file_ext}" # 원본 업로드 파일의 확장자를 붙임

            logger.info(f"Uploading file '{uploaded_file.name}' to S3 as '{s3_target_filename}'. Content-Type: {uploaded_file.content_type}")

            # django-storages를 사용하여 S3에 파일 저장
            # save() 메서드는 파일 객체를 받아 S3에 저장하고 저장된 경로(상대 경로)를 반환합니다.
            file_path_on_s3 = s3_storage_instance.save(s3_target_filename, uploaded_file)
            
            logger.info(f"Successfully uploaded to S3: {file_path_on_s3}")

            # 파일이 성공적으로 업로드되었음을 클라이언트에게 알림
            return JsonResponse({
                'status': 'success',
                'message': '사진이 S3에 성공적으로 업로드되었습니다.',
                'filename_uploaded': s3_target_filename, # S3에 저장된 최종 파일명
                's3_path': file_path_on_s3 # S3 내부 경로
            })

        except Exception as e:
            logger.exception(f"Error during S3 upload for '{s3_target_filename}'.") # exc_info=True로 스택 트레이스 기록
            return JsonResponse({'status': 'error', 'message': f'파일 업로드 실패: {e}'}, status=500)

    # POST/GET 외의 다른 요청 방식은 허용하지 않음
    return HttpResponse("Method Not Allowed", status=405)