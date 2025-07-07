# qr_upload/views.py
import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage # S3 Storage 인스턴스를 가져오는 표준 방법
from django.conf import settings
from django.utils import timezone
from datetime import timedelta # QrTemporaryLink 모델이 이미 정의했지만, 뷰에서 직접 계산할 때 사용

from .models import QrTemporaryLink # 새 앱의 모델 임포트

logger = logging.getLogger(__name__)

# S3 Storage 인스턴스 (settings.py에 default_storage가 S3로 설정되어 있어야 함)
# INSTALLED_APPS에 'storages' 추가 및 AWS_STORAGE_BUCKET_NAME 등 설정 가정
s3_storage_instance = default_storage


@csrf_exempt
def upload_photo_from_qr_link(request, token):
    """
    QR 링크를 통해 접근하는 업로드 페이지 (GET) 및 파일 업로드 처리 (POST)
    """
    temp_link = get_object_or_404(QrTemporaryLink, token=token)

    # 링크 유효성 검사
    if not temp_link.is_active or temp_link.is_expired():
        logger.warning(f"Attempt to access expired/inactive link: {token}")
        return HttpResponse("이 링크는 만료되었거나 유효하지 않습니다. 관리자에게 문의해주세요.", status=403)
    
    if temp_link.is_used and request.method == 'POST': # 이미 사용된 링크로 POST 요청 시도 방지
        logger.warning(f"Attempt to reuse a used link for POST: {token}")
        return JsonResponse({'status': 'error', 'message': '이 링크는 이미 사용되었습니다.'}, status=403)


    filename_from_link = temp_link.filename

    if request.method == 'GET':
        context = {
            'filename': filename_from_link,
            # 현재 뷰의 URL을 POST 대상으로 설정
            'upload_url': request.path, 
            'upload_success_url': reverse('qr_upload:qr_upload_success_page') 
        }
        # QR 전용 업로드 템플릿 사용 (기존과 이름 충돌 방지)
        return render(request, 'qr_upload/qr_upload_photo.html', context)

    elif request.method == 'POST':
        uploaded_file = request.FILES.get('photo')
        # 클라이언트에서 보낸 filename (유효성 검사용)
        client_sent_filename = request.POST.get('filename') 

        # 안전을 위해 클라이언트가 보낸 filename이 토큰에 연결된 filename과 일치하는지 확인
        if client_sent_filename != filename_from_link:
            logger.error(f"Filename mismatch: client sent '{client_sent_filename}', link is for '{filename_from_link}'")
            return JsonResponse({'status': 'error', 'message': '파일명이 일치하지 않습니다. 올바른 QR 코드를 사용해주세요.'}, status=400)

        if not uploaded_file:
            logger.error("POST request received without 'photo' file.")
            return JsonResponse({'status': 'error', 'message': '사진 파일을 찾을 수 없습니다.'}, status=400)
        
        # S3에 최종 저장될 파일명은 링크에 명시된 파일명을 사용
        s3_final_filename = filename_from_link 

        try:
            # 파일 확장자 처리 (클라이언트가 확장자 없이 파일명을 보냈을 경우 대비)
            name_part, ext_part = os.path.splitext(s3_final_filename)
            if not ext_part and uploaded_file.name: # 파일명에 확장자가 없다면 원본 파일에서 가져옴
                original_file_name, original_file_ext = os.path.splitext(uploaded_file.name)
                s3_final_filename = f"{name_part}{original_file_ext}"

            logger.info(f"Uploading file '{uploaded_file.name}' to S3 as '{s3_final_filename}'. Content-Type: {uploaded_file.content_type}")

            file_path_on_s3 = s3_storage_instance.save(s3_final_filename, uploaded_file)
            
            logger.info(f"Successfully uploaded to S3: {file_path_on_s3}")

            # 파일이 성공적으로 업로드되었을 때, 해당 링크를 '사용됨'으로 표시
            temp_link.is_used = True
            temp_link.save()
            logger.info(f"Temporary link {token} marked as used after successful upload.")

            # 성공 페이지로 리다이렉트
            return redirect(reverse('qr_upload:qr_upload_success_page') + f'?filename={s3_final_filename}')

        except Exception as e:
            logger.exception(f"Error during S3 upload for '{s3_final_filename}'.")
            return JsonResponse({'status': 'error', 'message': f'파일 업로드 실패: {e}'}, status=500)

    return HttpResponse("Method Not Allowed", status=405)


def generate_temp_upload_link(request):
    """
    WMS 등 외부 시스템에서 호출하여 QR 코드에 사용할 임시 업로드 URL을 반환합니다.
    GET 요청으로 filename 파라미터를 받습니다.
    """
    if request.method == 'GET':
        filename_to_upload = request.GET.get('filename')
        if not filename_to_upload:
            return JsonResponse({'status': 'error', 'message': '파일명을 지정해야 합니다.'}, status=400)

        try:
            temp_link = QrTemporaryLink.objects.create(
                filename=filename_to_upload
                # expires_at은 save()에서 자동 설정됨
            )
            
            # 생성된 토큰을 사용하여 QR 코드에 들어갈 URL 생성
            qr_url = request.build_absolute_uri(
                reverse('qr_upload:upload_photo_from_qr_link', args=[temp_link.token])
            )
            
            return JsonResponse({
                'status': 'success',
                'qr_url': qr_url,
                'token': str(temp_link.token),
                'expires_at': temp_link.expires_at.isoformat(),
                'message': 'QR 업로드 링크가 성공적으로 생성되었습니다.'
            })
        except Exception as e:
            logger.exception(f"Error generating temporary QR link for {filename_to_upload}")
            return JsonResponse({'status': 'error', 'message': f'QR 링크 생성 실패: {e}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'GET 요청만 허용됩니다.'}, status=405)


def qr_upload_success_view(request):
    """
    QR 코드 업로드 성공 페이지
    """
    filename_uploaded = request.GET.get('filename', '알 수 없는 파일')
    context = {
        'filename_uploaded': filename_uploaded,
    }
    # QR 전용 성공 템플릿 사용 (기존과 이름 충돌 방지)
    return render(request, 'qr_upload/qr_upload_success.html', context)
