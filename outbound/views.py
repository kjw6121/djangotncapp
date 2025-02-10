from django.shortcuts import HttpResponse, render
from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import json
from django.utils.timezone import now  # 현재 시간 가져오기
from .models import ob, ob_today_scandata
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@login_required(login_url='login')  # 로그인되어 있지 않을 때 리다이렉트할 URL
def index(request):
    current_user = request.user.username
    current_time = timezone.now()
    return render(request, 'outbound.html')

@login_required(login_url='login')  # 로그인되어 있지 않을 때 리다이렉트할 URL
def mainhu(request): 
    current_user = request.user.username
    current_time = timezone.now()
    return render(request, 'outbound.html')


@csrf_exempt
def save_scanned_data(request):
    if request.method == 'POST':
        # 요청 데이터 확인
        user = request.POST.get('user', '').strip()
        date = request.POST.get('date', '').strip()
        name = request.POST.get('name', '').strip()

        # 데이터 검증
        if not user or not date or not name:
            return JsonResponse({'status': 'error', 'message': 'No data to save.'})

        # 데이터 저장
        try:
            ob.objects.create(user=user, date=date, name=name)
            return JsonResponse({'status': 'success', 'message': 'Data saved successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error saving data: {str(e)}'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    

def today_scanned_data(request):
        # stored procedure 호출
    results = ob_today_scandata.call_stored_procedure()

    # 결과를 템플릿에 전달
    context = {'results': results}
    return render(request, 'ob_today_data.html', context)
