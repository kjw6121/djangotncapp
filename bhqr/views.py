from django.shortcuts import HttpResponse, render
from django.views import generic
from django.shortcuts import render
from django.utils import timezone

# Create your views here.

def index(request):
    current_user = request.user
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'bhqr.html', {'current_user': current_user, 'current_time': current_time})


def error_page(request):
    return render(request, 'error.html')