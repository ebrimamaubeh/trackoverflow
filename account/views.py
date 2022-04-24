from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import NewUserForm

# Create your views here.
def register_user(request):
    if request.method == 'POST': 
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect('question:index') 
        else: # the else fixed the errors in the form, 
            return render(request, "account/register.html", context={'register_form': form})
    form = NewUserForm()
    return render(request, "account/register.html", context={'register_form': form})



def login_user(request):
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                messages.info(request, "You are successfully logged in.")
                return redirect('question:index')
        else: 
            messages.error(request, "Invalid username or password!")
            return render(request, "account/login.html", context={'login_form': form})
     
    form = AuthenticationForm()
    return render(request, "account/login.html", context={'login_form': form})


def logout_user(request):
    if request.user.is_authenticated: 
        logout(request)
        messages.info(request, "Successfully Logged out!")
        return redirect('question:index')
    else: 
        messages.info(request, "Not logged in")
        return redirect('account:login')


