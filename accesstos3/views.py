# your_app/views.py

# ================================================================
# 1. 필요한 모듈 임포트 (기존 import 문은 그대로 유지)
# ================================================================
import logging
import mimetypes 
# import uuid # UUID는 더 이상 사용하지 않으므로 제거하거나 주석 처리합니다.
from urllib.parse import quote 

from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage 

# Django 모델을 사용한다면:
# from .models import UploadedFile 


# ================================================================
# 2. 로거 및 스토리지 객체 초기화 (파일 상단에 한 번만)
# ================================================================
logger = logging.getLogger(__name__)
default_storage = S3Boto3Storage() 


# ================================================================
# 3. 파일 업로드 뷰 (Access -> Django -> S3)
#    - X-Filename 헤더로 파일명 수신
#    - VBA에서 가져온 파일명을 그대로 S3에 저장
# ================================================================
@csrf_exempt 
def upload_file_from_access(request):
    if request.method == 'POST':
        if request.body:
            # Access에서 보낸 X-Filename 헤더 값 가져오기
            raw_filename_from_access = request.META.get('HTTP_X_FILENAME', 'uploaded_from_access.bin')
            
            # Access VBA에서 한글을 Latin-1으로 인코딩하여 보낼 수 있으므로, UTF-8로 디코딩 시도
            # 이 processed_original_filename이 S3에 저장될 파일명이 됩니다.
            processed_original_filename = raw_filename_from_access
            try:
                processed_original_filename = raw_filename_from_access.encode('iso-8859-1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                logger.warning(f"Filename decoding from iso-8859-1 to utf-8 failed for: '{raw_filename_from_access}'. Using raw name.")
            
            logger.info(f"Raw filename from Access (X-Filename header): '{raw_filename_from_access}'")
            logger.info(f"Processed (potentially decoded) original filename (S3 target name): '{processed_original_filename}'")

            # --- 변경된 부분 시작 ---
            # UUID 대신 VBA에서 가져온 processed_original_filename을 S3 저장 파일명으로 사용
            s3_storage_filename = processed_original_filename 
            # --- 변경된 부분 끝 ---
            
            logger.info(f"S3 storage filename (from VBA): '{s3_storage_filename}'")

            try:
                # S3에 파일 저장 시 VBA에서 가져온 파일명 사용
                file_path_on_s3 = default_storage.save(s3_storage_filename, ContentFile(request.body, name=s3_storage_filename))
                
                logger.info(f"File '{s3_storage_filename}' uploaded to S3: {file_path_on_s3}")
                
                # (선택 사항) 원본 파일명과 S3 저장 파일명이 이제 동일하므로,
                # 별도로 DB에 매핑 정보를 저장하는 코드는 필요 없을 수 있습니다.
                # 하지만, 만약을 대비하여 (예: 파일명 이력 관리 등) 모델을 사용한다면
                # 기존 original_filename과 s3_filename 필드를 동일하게 저장할 수 있습니다.
                # 예시:
                # try:
                #     UploadedFile.objects.create(
                #         original_filename=processed_original_filename, # Access에서 받은 이름
                #         s3_filename=s3_storage_filename,             # S3에 저장된 이름 (이제 동일)
                #         s3_path=file_path_on_s3
                #     )
                #     logger.info(f"File metadata saved: {processed_original_filename} -> {s3_storage_filename}")
                # except Exception as db_e:
                #     logger.error(f"Failed to save file metadata: {db_e}", exc_info=True)


                return JsonResponse({
                    'status': 'success',
                    's3_path': file_path_on_s3, # S3에 실제로 저장된 파일명
                    'original_filename_received': processed_original_filename # Access에 확인용으로 반환
                })
            except Exception as e:
                logger.error(f"Error uploading file to S3: {e}", exc_info=True)
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return HttpResponseBadRequest("No file data received.")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")

# 나머지 download_file_from_s3 뷰 함수는 여기에 이어서 작성됩니다.
# ... (download_file_from_s3 함수 코드) ...
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