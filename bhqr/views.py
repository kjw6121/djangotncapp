from django.shortcuts import HttpResponse, render
from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ScanData


# Create your views here.

def index(request):
    current_user = request.user.username
    current_time = timezone.now()
    return render(request, 'bhqr.html', {'current_user': current_user, 'current_time': current_time})


def error_page(request):
    return render(request, 'error.html')

# views.py


@csrf_exempt
def save_scan_data(request):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        scan_message = request.POST.get('scan_message')
        
        if user and scan_message:
            # 스캔 데이터를 모델에 저장
            scan_data = ScanData(user=user, scan_message=scan_message)
            scan_data.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})