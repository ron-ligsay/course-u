from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Error logging in')
            return redirect('login')
    else:
        return render(request, 'login.html')