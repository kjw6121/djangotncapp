import boto3
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage

def extract_text_from_image(image_path):
    
    client = boto3.client('rekognition', region_name='ap-northeast-2')  # 리전 추가
    
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={'Bytes': image_bytes})
    detected_texts = [text['DetectedText'] for text in response['TextDetections']]
    
    return detected_texts

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        file_path = default_storage.save(f'uploads/{image_file.name}', ContentFile(image_file.read()))

        # 파일 경로 출력 (디버깅 용)
        print(f"File path: {file_path}")
        print(f"Full file path: {default_storage.path(file_path)}")


        # AWS Rekognition OCR 실행
        detected_text = extract_text_from_image(default_storage.path(file_path))

        # DB 저장
        UploadedImage.objects.create(image=file_path)

        return render(request, 'result.html', {'detected_text': detected_text})

    return render(request, 'upload.html')
