from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # 게시글 목록 페이지
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


@login_required(login_url='login')  # 로그인되어 있지 않을 때 리다이렉트할 URL
def main(request):
    return render(request, 'main.html')

def your_protected_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
