# qrcode_api/views.py
import qrcode
from PIL import Image
from django.http import HttpResponse
import io

def generate_qr_code(request):
    text_data = request.GET.get('text', '') # GET 파라미터로 'text' 값을 받습니다.

    if not text_data:
        return HttpResponse("No text data provided", status=400)

    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # 이미지를 메모리에 저장
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")