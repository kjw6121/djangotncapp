from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog, Boxtr, Boxtr_sum, Boxtr_stock, Boxtr_status
from .forms import UserCreationForm, boxform
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



def new(request):
    return render(request, 'polls/new.html')


def home(request):
    boxtr_sums = Boxtr_sum.objects.all()
    return render(request, 'polls/home.html', { 'boxtr_sums': boxtr_sums })


def boxtrstock(request):
    boxtr_stocks = Boxtr_stock.objects.all()
    return render(request, 'polls/boxstock.html', { 'boxtr_stocks': boxtr_stocks })


def boxtrstatus(request):
    boxtr_status = Boxtr_status.objects.all()
    return render(request, 'polls/boxtrstatus.html', { 'boxtr_status': boxtr_status })


# listings/views.py

def detail(request, id):
    boxtr = Boxtr.objects.get(id = id)
    return render(request, 'polls/detail.html', { 'boxtr': boxtr })

# listings/views.py


def delete(request, id):
    delete_boxtr = Boxtr.objects.get(id=id) 
    if delete_boxtr.truck != request.user.username :
       return render(request, 'polls/alert.html')

    if request.method == 'POST':
        delete_boxtr.delete()
        return redirect('polls:home')

    else :
        
        return render(request,
                'polls/delete.html',
                {'delete_boxtr': delete_boxtr})
    

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.writer = request.POST['writer']
    new_blog.body = request.POST['body']
    new_blog.pub_date = timezone.now()
    new_blog.save()

    return redirect('detail', new_blog.id)



def edit(request, id):
    edit_boxtr = Boxtr.objects.get(id= id)
    form = boxform(instance=edit_boxtr)
    context =  {'form': form}

    return render(request, 'polls/edit_new.html', context)



def post_update(request, id):
    boxtr = get_object_or_404(Boxtr, id=id)
    if boxtr.truck != request.user.username :
       return render(request, 'polls/alert.html')
        
    if request.method == 'POST':
        form = boxform(request.POST, instance=boxtr)
        if form.is_valid():
            form.save()
            return redirect('polls:detail', boxtr.id)
    else:   
            form = boxform(instance=boxtr)
            context = {'form': form}
    
    return render(request, 'polls/edit_new.html', context)




# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # 게시글 목록 페이지
            return redirect('polls:home')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'polls/signup.html', context)

def post_new(request):
    
    if request.user.is_authenticated:
            
        if request.method == 'POST':
            form = boxform(request.POST, request.FILES)
            if form.is_valid():
                new_boxtr = Boxtr()
                        
                new_boxtr.truck = request.user.username
                new_boxtr.pub_date = timezone.now()
                new_boxtr.arrival = form.cleaned_data['arrival']
                new_boxtr.wet = form.cleaned_data['wet']
                
                new_boxtr.box1 = form.cleaned_data['box1']
                new_boxtr.box1_qty = form.cleaned_data['box1_qty']
                new_boxtr.box2 = form.cleaned_data['box2']
                new_boxtr.box2_qty = form.cleaned_data['box2_qty']
                new_boxtr.box3 = form.cleaned_data['box3']
                new_boxtr.box3_qty = form.cleaned_data['box3_qty']
                new_boxtr.box4 = form.cleaned_data['box4']
                new_boxtr.box4_qty = form.cleaned_data['box4_qty']
                new_boxtr.box5 = form.cleaned_data['box5']
                new_boxtr.box5_qty = form.cleaned_data['box5_qty']
                if request.user.username == "오성균" :
                    new_boxtr.status = "loading"
                
                new_boxtr.save()
                

            return redirect('polls:home')
        else:   
                form=boxform()
                context = {'form': form}
        
        return render(request, 'polls/post_new.html', context)
    else :
        return render(request, 'polls/alert2.html')


def unloading(request, id) :   
    if request.user.is_authenticated: 
        boxtr = Boxtr.objects.get(id=id)
        boxtr.status = "done"
        boxtr.pub_date = timezone.now()
        boxtr.save()
    else :
        return render(request, 'polls/alert2.html')
        
    
    return redirect('polls:home')

def loading(request, id) :
    if request.user.is_authenticated: 
        boxtr = Boxtr.objects.get(id=id)
        b = Boxtr(truck=request.user.username, arrival=boxtr.arrival, pub_date=timezone.now(), wet='No', status = 'loading',
                box1=boxtr.box1, box1_qty=boxtr.box1_qty, box2=boxtr.box2, box2_qty=boxtr.box2_qty,
                box3=boxtr.box3, box3_qty=boxtr.box3_qty, box4=boxtr.box4, box4_qty=boxtr.box4_qty,
                box5=boxtr.box5, box5_qty=boxtr.box5_qty
                )
        b.save()
        
        boxtr = Boxtr.objects.get(id=id)
        boxtr.status = "done"
        boxtr.pub_date = timezone.now()
        boxtr.save()
        
        
        return redirect('polls:home')
    else :
        return render(request, 'polls/alert2.html')
        

