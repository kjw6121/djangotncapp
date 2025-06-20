# your_app/views.py

# ================================================================
# 1. 필요한 모듈 임포트
# ================================================================
import logging
import mimetypes # 파일 MIME 타입을 추론하기 위함
import uuid # 파일 업로드 시 UUID 생성을 위함 (옵션, 한글 깨짐 방지용)
from urllib.parse import quote # 한글 파일명 URL 인코딩을 위함

from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt # CSRF 보호 비활성화 (보안 주의!)
from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage # django-storages S3 백엔드 사용

# Django 모델을 사용한다면:
# from .models import UploadedFile # models.py에 정의된 UploadedFile 모델을 가정


# ================================================================
# 2. 로거 및 스토리지 객체 초기화 (파일 상단에 한 번만)
# ================================================================
logger = logging.getLogger(__name__)
default_storage = S3Boto3Storage() # S3Boto3Storage를 default_storage로 사용


# ================================================================
# 3. 파일 업로드 뷰 (Access -> Django -> S3)
#    - X-Filename 헤더로 파일명 수신
#    - 한글 파일명 깨짐 방지를 위해 S3에는 UUID 기반의 영문 파일명으로 저장 권장
# ================================================================
@csrf_exempt # Access에서 POST 요청 시 CSRF 토큰을 보내기 어려우므로 일시적으로 비활성화
def upload_file_from_access(request):
    if request.method == 'POST':
        if request.body:
            # Access에서 보낸 X-Filename 헤더 값 가져오기
            raw_filename_from_access = request.META.get('HTTP_X_FILENAME', 'uploaded_from_access.bin')
            
            # Access VBA에서 한글을 Latin-1으로 인코딩하여 보낼 수 있으므로, UTF-8로 디코딩 시도
            processed_original_filename = raw_filename_from_access
            try:
                processed_original_filename = raw_filename_from_access.encode('iso-8859-1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                logger.warning(f"Filename decoding from iso-8859-1 to utf-8 failed for: '{raw_filename_from_access}'. Using raw name.")
            
            logger.info(f"Raw filename from Access (X-Filename header): '{raw_filename_from_access}'")
            logger.info(f"Processed (potentially decoded) original filename: '{processed_original_filename}'")

            # S3에 저장할 새로운 영문 파일명 (UUID 기반) 생성
            # 이것이 핵심: 한글 깨짐 문제 방지 및 S3 파일명 관리 용이
            file_extension = processed_original_filename.split('.')[-1] if '.' in processed_original_filename else ''
            s3_storage_filename = f"{uuid.uuid4()}.{file_extension}" 
            
            logger.info(f"Generated S3 storage filename (UUID-based): '{s3_storage_filename}'")

            try:
                # S3에 파일 저장 시 UUID 기반의 영문 파일명 사용
                file_path_on_s3 = default_storage.save(s3_storage_filename, ContentFile(request.body, name=s3_storage_filename))
                
                logger.info(f"File '{s3_storage_filename}' uploaded to S3: {file_path_on_s3}")
                
                # (권장) 원본 한글 파일명과 S3에 저장된 영문 파일명을 데이터베이스에 매핑하여 저장
                # 예시:
                # try:
                #     UploadedFile.objects.create(
                #         original_filename=processed_original_filename,
                #         s3_filename=s3_storage_filename,
                #         s3_path=file_path_on_s3
                #     )
                #     logger.info(f"File metadata saved: {processed_original_filename} -> {s3_storage_filename}")
                # except Exception as db_e:
                #     logger.error(f"Failed to save file metadata: {db_e}", exc_info=True)


                return JsonResponse({
                    'status': 'success',
                    's3_path': file_path_on_s3,
                    'original_filename_received': processed_original_filename # Access에 확인용으로 반환
                })
            except Exception as e:
                logger.error(f"Error uploading file to S3: {e}", exc_info=True)
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return HttpResponseBadRequest("No file data received.")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")


# ================================================================
# 4. 파일 다운로드 뷰 (Access -> Django -> S3)
#    - URL 경로에서 파일명 수신
#    - S3에서 파일을 읽어 HTTP 응답으로 스트리밍
# ================================================================
@csrf_exempt
def download_file_from_s3(request, filename): # URL에서 filename을 인자로 받습니다.
    # Access VBA에서 넘겨받은 filename (예: RE10084.pdf)은 S3에 저장된 실제 영문 파일명으로 가정
    s3_actual_filename = filename 

    logger.info(f"Attempting to download file from S3: '{s3_actual_filename}'")

    # 파일이 S3에 존재하는지 확인
    if not default_storage.exists(s3_actual_filename):
        logger.error(f"File not found on S3: '{s3_actual_filename}'")
        raise Http404(f"File '{s3_actual_filename}' not found.") 

    try:
        # S3에서 파일 열기 (s3_file_object는 스트리밍 가능한 파일 객체)
        s3_file_object = default_storage.open(s3_actual_filename, 'rb')

        # MIME 타입 추론
        mime_type, _ = mimetypes.guess_type(s3_actual_filename)
        if not mime_type:
            mime_type = 'application/octet-stream' # 기본 바이너리 타입

        # HTTP 응답 생성: S3 파일 객체를 직접 응답으로 전달 (메모리 효율적)
        response = HttpResponse(s3_file_object, content_type=mime_type)
        
        # 다운로드될 파일명 설정
        # (만약 DB에 원본 한글 파일명이 저장되어 있다면, 그 이름을 사용하도록 수정)
        download_name_for_client = s3_actual_filename # 기본적으로 S3 파일명 사용
        
        # 예시: DB에서 원본 한글 파일명 가져와 Content-Disposition에 사용
        # try:
        #     file_meta = UploadedFile.objects.get(s3_filename=s3_actual_filename)
        #     download_name_for_client = file_meta.original_filename # DB에 저장된 원본 한글 파일명
        # except UploadedFile.DoesNotExist:
        #     logger.warning(f"Metadata not found for S3 file: '{s3_actual_filename}'. Using S3 filename for download.")
        # except Exception as db_e:
        #     logger.error(f"Error retrieving metadata for {s3_actual_filename}: {db_e}", exc_info=True)
        #     logger.warning("Falling back to S3 filename for Content-Disposition.")


        # Content-Disposition 헤더 설정: 파일을 다운로드하도록 브라우저에 지시
        # 한글 파일명 지원을 위해 RFC 6266 (filename*=UTF-8'') 형식 사용
        # download_name_for_client가 한글을 포함할 수 있다면 quote 처리
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(download_name_for_client.encode('utf-8'))}"
        # 만약 순수 영문 파일명이라면 아래처럼 간단하게도 가능:
        # response['Content-Disposition'] = f"attachment; filename=\"{download_name_for_client}\""


        logger.info(f"Successfully streamed file '{s3_actual_filename}' for download (Download name: '{download_name_for_client}').")
        return response

    except Exception as e:
        logger.error(f"Error streaming file from S3 '{s3_actual_filename}': {e}", exc_info=True)
        # 사용자에게 상세한 에러 메시지를 노출하지 않도록 일반적인 메시지 반환
        return HttpResponse("파일을 다운로드하는 중 오류가 발생했습니다. 서버 로그를 확인해주세요.", status=500)