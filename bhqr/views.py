from django.shortcuts import HttpResponse, render
from django.views import generic

# Create your views here.


def index(request):
    return render(request, 'polls/bhqr.html')