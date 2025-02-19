import os
import boto3
import io
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage
from PIL import Image, ImageEnhance
import io

def resize_image(image_file, max_size=(1000, 1000)):
    """이미지를 리사이징하여 OCR 성능을 최적화"""
    image = Image.open(image_file)

    # 텍스트 선명도 향상
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)  # 선명도를 2배로 증가

    # 원본 비율 유지하면서 최대 크기 조정
    image.thumbnail(max_size, Image.LANCZOS)  # 기존 Image.ANTIALIAS 대신 Image.LANCZOS 사용

    # 메모리에 저장
    img_io = io.BytesIO()
    image_format = image.format if image.format else "JPEG"  # 포맷 확인
    image.save(img_io, format=image_format)
    img_io.seek(0)

    return img_io


def extract_text_from_image(image_path):
    """AWS Rekognition을 사용해 텍스트 인식"""
    client = boto3.client('rekognition', region_name='ap-northeast-2')  # 리전 수정됨 ✅

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={'Bytes': image_bytes})
    detected_texts = [text['DetectedText'] for text in response['TextDetections']]
    
    return detected_texts

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # 이미지 리사이징 적용
        resized_image = resize_image(image_file)

        # 파일 저장 (메모리에서 변환된 이미지 저장)
        file_path = default_storage.save(f'{image_file.name}', ContentFile(resized_image.read()))

        # 디버깅 로그
        print(f"File path: {file_path}")
        print(f"Full file path: {default_storage.path(file_path)}")

        # AWS Rekognition OCR 실행
        detected_text = extract_text_from_image(default_storage.path(file_path))

        # 이미지 파일 삭제 (서버 용량을 줄이기 위해) path(f'uplads/{file_path}'))
        os.remove(default_storage.path(f'uplads/{file_path}'))

        return render(request, 'result.html', {'detected_text': detected_text})

    return render(request, 'upload.html')
