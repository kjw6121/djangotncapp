from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Boxtd
from .models import Blog

def index(request): 
    boxtds = Boxtd.objects.all()
    context = {'boxtds':boxtds}
    return render(request, 'polls/index.html', context)

def welcome(request):
    return render(request, 'polls/welcome.html')


def hello(request):
    userName = request.GET["name"]
    return render(request, "polls/hello.html", {'userName' : userName})

def new(request):
    return render(request, 'polls/new.html')


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'polls/home.html', { 'blogs': blogs })


def detail(request, id):
    blog = Blog.objects.get(id = id)
    return render(request, 'polls/detail.html', { 'blog': blog })


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.writer = request.POST['writer']
    new_blog.body = request.POST['body']
    new_blog.pub_date = timezone.now()
    new_blog.save()

    return redirect('detail', new_blog.id)

def edit(request, id):
    edit_blog = Blog.objects.get(id= id)
    return render(request, 'polls/edit.html', {'blog': edit_blog})

def update(request, id):
    update_blog = Blog.objects.get(id= id)
    update_blog.title = request.POST['title']
    update_blog.writer = request.POST['writer']
    update_blog.body = request.POST['body']
    update_blog.pub_date = timezone.now()
    update_blog.save()

    return redirect('detail', update_blog.id)

def delete(request, id):
    delete_blog = Blog.objects.get(id= id)
    delete_blog.delete()

    return redirect('home')