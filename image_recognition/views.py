import os # 이 모듈은 더 이상 직접적으로 필요하지 않을 수 있습니다.
import boto3
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage # 필요하다면 유지
from django.conf import settings # settings.py에서 AWS_STORAGE_BUCKET_NAME을 가져오기 위해 추가

# 함수 시그니처 변경: 이미지 경로 대신 S3 버킷 이름과 객체 키를 받도록 변경
def extract_text_from_image(bucket_name, object_key): # <--- 파라미터 변경
    """AWS Rekognition을 사용해 S3의 이미지에서 텍스트 인식"""
    # settings에서 리전 가져오기 (만약 .env에서 가져오지 않는다면 직접 설정도 가능)
    client = boto3.client('rekognition', region_name=settings.AWS_S3_REGION_NAME)

    # S3에 저장된 이미지를 직접 Rekognition으로 전달합니다.
    # 로컬 파일을 열 필요가 없습니다.
    response = client.detect_text(
        Image={
            'S3Object': {
                'Bucket': bucket_name, # S3 버킷 이름
                'Name': object_key,   # S3 객체 키 (파일 이름)
            }
        }
    )
    detected_texts = [text['DetectedText'] for text in response['TextDetections']]

    return detected_texts

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # 파일 저장 (이때 파일은 S3에 직접 저장됩니다.)
        # file_path는 S3 버킷 내의 객체 키(예: 'image_name.jpg')를 반환합니다.
        # 파일 이름 중복 방지를 위해 UUID 사용을 강력히 권장
        import uuid
        import os.path
        file_extension = os.path.splitext(image_file.name)[1]
        unique_filename = f"uploads/{uuid.uuid4()}{file_extension}" # S3 폴더 구조를 원한다면 'uploads/' 추가
        file_path = default_storage.save(unique_filename, ContentFile(image_file.read())) # <--- 고유한 파일 이름 사용

        # 디버깅 로그 (이제 default_storage.path()는 사용할 수 없습니다.)
        print(f"File path (S3 object key): {file_path}") # 이제 이 로그는 S3 객체 키를 출력합니다.
        # print(f"Full file path: {default_storage.path(file_path)}") # <--- 이 라인 반드시 제거 또는 주석 처리!

        # AWS Rekognition OCR 실행
        # S3 버킷 이름과 S3 객체 키(file_path)를 전달
        detected_text = extract_text_from_image(settings.AWS_STORAGE_BUCKET_NAME, file_path) # <--- 파라미터 변경

        # OCR 처리 후 이미지 파일 삭제 (S3에서 삭제)
        # 로컬 파일 시스템에 대한 os.remove() 대신 S3에 대한 delete()를 사용합니다.
        # os.remove(default_storage.path(file_path)) # <--- 이 라인 반드시 제거 또는 주석 처리!
        default_storage.delete(file_path) # S3에서 파일 삭제

        return render(request, 'result.html', {'detected_text': detected_text})

    return render(request, 'upload.html')