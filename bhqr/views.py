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


@csrf_exempt  # 임시로 CSRF 보호 해제 (실제로는 안전한 방법으로 대체해야 함)
def save_scan_data(request):
    if request.method == "POST":
        scan_message = request.POST.get("scan_message", "")
        user = request.user if request.user.is_authenticated else None

        if scan_message:
            scan_data = ScanData.objects.create(user=user, scan_message=scan_message)
            return JsonResponse({"status": "success", "data_id": scan_data.id})
        else:
            return JsonResponse({"status": "error", "message": "Scan message is empty"})
