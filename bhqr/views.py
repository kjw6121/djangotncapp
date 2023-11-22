from django.shortcuts import HttpResponse, render
from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from .models import ScanData, today_scandata
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url='login')  # 로그인되어 있지 않을 때 리다이렉트할 URL
def index(request):
    current_user = request.user.username
    current_time = timezone.now()
    return render(request, 'bhqr.html', {'current_user': current_user, 'current_time': current_time})


def error_page(request):
    return render(request, 'error.html')

# views.py


import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_scan_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = request.user if request.user.is_authenticated else None
        scan_message = data.get('scan_message')

        if user and scan_message:
            # 스캔 데이터를 모델에 저장
            scan_data = ScanData(user=user, scan_message=scan_message)
            scan_data.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})


def today_data(request):
        # stored procedure 호출
    results = today_scandata.call_stored_procedure()

    # 결과를 템플릿에 전달
    context = {'results': results}
    return render(request, 'today_data.html', context)
