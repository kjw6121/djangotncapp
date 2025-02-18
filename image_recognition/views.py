import boto3
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage

def extract_text_from_image(image_path):
    client = boto3.client('rekognition', region_name='ap-northeast-2')  # AWS 리전 설정 필요

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={'Bytes': image_bytes})
    detected_texts = [text['DetectedText'] for text in response['TextDetections']]
    
    return detected_texts

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image1') and request.FILES.get('image2'):
        # 첫 번째 이미지 처리
        image1_file = request.FILES['image1']
        file_path1 = default_storage.save(f'uploads/{image1_file.name}', ContentFile(image1_file.read()))
        text1 = extract_text_from_image(default_storage.path(file_path1))

        # 두 번째 이미지 처리
        image2_file = request.FILES['image2']
        file_path2 = default_storage.save(f'uploads/{image2_file.name}', ContentFile(image2_file.read()))
        text2 = extract_text_from_image(default_storage.path(file_path2))

        # 텍스트 비교 (리스트 형태이므로 문자열로 변환하여 비교)
        result = "OK" if " ".join(text1) == " ".join(text2) else "NG"

        # DB 저장 (선택 사항)
        UploadedImage.objects.create(image=file_path1)
        UploadedImage.objects.create(image=file_path2)

        return render(request, 'result.html', {'text1': text1, 'text2': text2, 'result': result})

    return render(request, 'upload.html')
