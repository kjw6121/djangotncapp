import boto3
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedImage

def extract_text_from_image(image_path):
    # AWS Rekognition 클라이언트를 리전 설정과 함께 생성
    client = boto3.client('rekognition', region_name='us-west-2')  # 리전 추가
    
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_text(Image={'Bytes': image_bytes})
    detected_texts = [text['DetectedText'] for text in response['TextDetections']]
    
    return detected_texts

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image1') and request.FILES.get('image2'):
        # 첫 번째 이미지 처리
        image_file1 = request.FILES['image1']
        file_path1 = default_storage.save(f'uploads/{image_file1.name}', ContentFile(image_file1.read()))

        # 두 번째 이미지 처리
        image_file2 = request.FILES['image2']
        file_path2 = default_storage.save(f'uploads/{image_file2.name}', ContentFile(image_file2.read()))

        # 첫 번째 이미지에서 텍스트 추출
        detected_text1 = extract_text_from_image(default_storage.path(file_path1))

        # 두 번째 이미지에서 텍스트 추출
        detected_text2 = extract_text_from_image(default_storage.path(file_path2))

        # 텍스트 비교
        if set(detected_text1) == set(detected_text2):
            result = "OK"
        else:
            result = "NG"

        # DB 저장 (필요시)
        UploadedImage.objects.create(image=file_path1)
        UploadedImage.objects.create(image=file_path2)

        return render(request, 'result.html', {'detected_text1': detected_text1, 'detected_text2': detected_text2, 'result': result})

    return render(request, 'upload.html')
