import os
import boto3
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage

def extract_text_from_image(image_path):
    """AWS Rekognition을 사용해 텍스트 인식"""
    client = boto3.client('rekognition', region_name='ap-northeast-2')  # AWS 리전 설정

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={'Bytes': image_bytes})
    detected_texts = [text['DetectedText'] for text in response['TextDetections']]
    
    return detected_texts

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # 파일 저장 (프론트에서 리사이징 후 전송된 이미지를 저장)
        file_path = default_storage.save(image_file.name, ContentFile(image_file.read()))

        # 디버깅 로그
        print(f"File path: {file_path}")
        print(f"Full file path: {default_storage.path(file_path)}")

        # AWS Rekognition OCR 실행
        detected_text = extract_text_from_image(default_storage.path(file_path))

        # OCR 처리 후 이미지 파일 삭제 (서버 용량 절약)
        os.remove(default_storage.path(file_path))

        return render(request, 'result.html', {'detected_text': detected_text})

    return render(request, 'upload.html')
