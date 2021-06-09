from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate

from .forms import CreateUserForm

from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            messages.success(request, 'successfully logged in')
            return redirect('index')
        
    messages.error(request, 'Invalid Username or Password')
    return render(request, 'accounts/login.html') 

def register(request):
    form = CreateUserForm()

    if request.method == 'POST': 
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully registered, please log in')
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
