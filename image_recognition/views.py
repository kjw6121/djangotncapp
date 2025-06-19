# image_recognition/views.py

import os
import boto3
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage # 필요하다면 유지
from django.conf import settings # settings.py에서 AWS_STORAGE_BUCKET_NAME을 가져오기 위해 추가

# 함수 시그니처 변경: 이미지 경로 대신 S3 버킷 이름과 객체 키를 받도록 변경
def extract_text_from_image(bucket_name, object_key):
    """AWS Rekognition을 사용해 S3의 이미지에서 텍스트 인식"""
    client = boto3.client('rekognition', region_name=settings.AWS_S3_REGION_NAME) # settings에서 리전 가져오기

    response = client.detect_text(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key, # S3 객체 키 (file_path)
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
        file_path = default_storage.save(image_file.name, ContentFile(image_file.read()))

        # 디버깅 로그 (이제 default_storage.path()는 사용할 수 없습니다.)
        print(f"File path (S3 object key): {file_path}")
        # print(f"Full file path: {default_storage.path(file_path)}") # 삭제!

        # AWS Rekognition OCR 실행
        # S3 버킷 이름과 S3 객체 키(file_path)를 전달
        detected_text = extract_text_from_image(settings.AWS_STORAGE_BUCKET_NAME, file_path)

        # OCR 처리 후 이미지 파일 삭제 (S3에서 삭제)
        # S3에서 파일을 삭제하려면 default_storage.delete()를 사용합니다.
        # os.remove(default_storage.path(file_path)) # 삭제!
        default_storage.delete(file_path) # S3에서 파일 삭제

        return render(request, 'result.html', {'detected_text': detected_text})

    return render(request, 'upload.html')