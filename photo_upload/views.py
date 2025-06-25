# photo_upload/views.py
import logging
import os
import boto3

from django.shortcuts import render, redirect # redirect 추가
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.urls import reverse # reverse 추가 (URL 이름으로 리다이렉트하기 위해)


logger = logging.getLogger(__name__)

s3_storage_instance = S3Boto3Storage()


@csrf_exempt
def upload_photo_from_phone(request):
    """
    GET 요청: 사진 촬영 웹 페이지를 렌더링하고, QR 코드에서 받은 파일명을 전달합니다.
    POST 요청: 스마트폰에서 촬영된 사진 파일을 받아 S3에 업로드합니다.
    """
    if request.method == 'GET':
        filename_from_qr = request.GET.get('filename', 'untitled_photo')
        
        context = {
            'filename': filename_from_qr,
            'upload_url': request.path, # 현재 뷰의 URL (POST 요청 대상)
            # 업로드 성공 후 이동할 페이지의 URL을 미리 전달하여 JS에서 사용
            'upload_success_url': reverse('upload_success_page') 
        }
        return render(request, 'photo_upload/upload_photo.html', context)

    elif request.method == 'POST':
        uploaded_file = request.FILES.get('photo')
        s3_target_filename = request.POST.get('filename')

        if not uploaded_file:
            logger.error("POST request received without 'photo' file.")
            return JsonResponse({'status': 'error', 'message': '사진 파일을 찾을 수 없습니다.'}, status=400)
        
        if not s3_target_filename:
            logger.error("POST request received without 'filename' for S3 target.")
            return JsonResponse({'status': 'error', 'message': '저장할 파일명을 찾을 수 없습니다.'}, status=400)

        try:
            name_part, ext_part = os.path.splitext(s3_target_filename)
            if not ext_part:
                original_file_name, original_file_ext = os.path.splitext(uploaded_file.name)
                s3_target_filename = f"{name_part}{original_file_ext}"

            logger.info(f"Uploading file '{uploaded_file.name}' to S3 as '{s3_target_filename}'. Content-Type: {uploaded_file.content_type}")

            file_path_on_s3 = s3_storage_instance.save(s3_target_filename, uploaded_file)
            
            logger.info(f"Successfully uploaded to S3: {file_path_on_s3}")

            # 파일이 성공적으로 업로드되었을 때, 별도의 성공 페이지로 리다이렉트
            # 리다이렉트 시 쿼리 파라미터로 업로드된 파일명을 전달
            return JsonResponse({
    'status': 'success',
    'redirect_to': reverse('upload_success_page') + f'?filename={s3_target_filename}'
})


        except Exception as e:
            logger.exception(f"Error during S3 upload for '{s3_target_filename}'.")
            return JsonResponse({'status': 'error', 'message': f'파일 업로드 실패: {e}'}, status=500)

    return HttpResponse("Method Not Allowed", status=405)


# --- 새로운 뷰 함수: 업로드 성공 페이지 ---
def upload_success_view(request):
    """
    파일 업로드 성공 후 보여줄 페이지를 렌더링합니다.
    """
    # 쿼리 파라미터에서 업로드된 파일명을 가져옴
    uploaded_filename = request.GET.get('filename', '알 수 없는 파일') 
    context = {
        'filename_uploaded': uploaded_filename
    }
    return render(request, 'photo_upload/upload_success.html', context)