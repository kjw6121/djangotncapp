# photo_upload/views.py
import logging
import os
import boto3

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.urls import reverse


logger = logging.getLogger(__name__)

s3_storage_instance = S3Boto3Storage()


@csrf_exempt
def upload_photo_from_phone(request):
    # --- 디버깅용 print 문 추가 시작 ---
    print(f"DEBUG: upload_photo_from_phone view called. Request method: {request.method}")
    print(f"DEBUG: Request path: {request.path}")
    print(f"DEBUG: Request GET params: {request.GET}")
    print(f"DEBUG: Request POST params: {request.POST}")
    # --- 디버깅용 print 문 추가 끝 ---

    if request.method == 'GET':
        print("DEBUG: Handling GET request.") # 디버깅
        filename_from_qr = request.GET.get('filename', 'untitled_photo')
        
        context = {
            'filename': filename_from_qr,
            'upload_url': request.path,
            'upload_success_url': reverse('upload_success_page') 
        }
        return render(request, 'photo_upload/upload_photo.html', context)

    elif request.method == 'POST':
        print("DEBUG: Handling POST request.") # 디버깅
        uploaded_file = request.FILES.get('photo')
        s3_target_filename = request.POST.get('filename')

        if not uploaded_file:
            print("DEBUG: No 'photo' file found in POST request.") # 디버깅
            logger.error("POST request received without 'photo' file.")
            return JsonResponse({'status': 'error', 'message': '사진 파일을 찾을 수 없습니다.'}, status=400)
        
        if not s3_target_filename:
            print("DEBUG: No 'filename' for S3 target found in POST request.") # 디버깅
            logger.error("POST request received without 'filename' for S3 target.")
            return JsonResponse({'status': 'error', 'message': '저장할 파일명을 찾을 수 없습니다.'}, status=400)

        try:
            print(f"DEBUG: Processing file: {uploaded_file.name}") # 디버깅
            name_part, ext_part = os.path.splitext(s3_target_filename)
            if not ext_part:
                original_file_name, original_file_ext = os.path.splitext(uploaded_file.name)
                s3_target_filename = f"{name_part}{original_file_ext}"

            logger.info(f"Uploading file '{uploaded_file.name}' to S3 as '{s3_target_filename}'. Content-Type: {uploaded_file.content_type}")
            print(f"DEBUG: Attempting S3 upload for {s3_target_filename}") # 디버깅

            file_path_on_s3 = s3_storage_instance.save(s3_target_filename, uploaded_file)
            
            logger.info(f"Successfully uploaded to S3: {file_path_on_s3}")
            print(f"DEBUG: S3 upload successful. Redirecting to success page: {reverse('upload_success_page') + f'?filename={s3_target_filename}'}") # 디버깅

            return redirect(reverse('upload_success_page') + f'?filename={s3_target_filename}')

        except Exception as e:
            print(f"DEBUG: Caught exception during S3 upload: {e}") # 디버깅
            logger.exception(f"Error during S3 upload for '{s3_target_filename}'.")
            return JsonResponse({'status': 'error', 'message': f'파일 업로드 실패: {e}'}, status=500)

    print("DEBUG: Request method not GET or POST, returning 405.") # 디버깅
    return HttpResponse("Method Not Allowed", status=405)


def upload_success_view(request):
    print(f"DEBUG: upload_success_view called. Request method: {request.method}") # 디버깅
    uploaded_filename = request.GET.get('filename', '알 수 없는 파일') 
    context = {
        'filename_uploaded': uploaded_filename
    }
    return render(request, 'photo_upload/upload_success.html', context)