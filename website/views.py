from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from website.models import Specialization, Test
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render

# Create your views here.
def home(request):
    specialization_items = Specialization.objects.all()
    return render(request, 'home.html', {'specialization_items': specialization_items})

def login_user(request):
    if request.method == 'POST':
        #email = request.POST['email']
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Error logging in')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def sign_in(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, 'You have successfully created an account')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'sign_in.html', {'form': form})
    return render(request, 'sign_in.html', {'form': form})


def forgot_password(request):
    return render(request, 'forgot_password.html')

def recovery(request):
    return render(request, 'recovery.html')

def test(request, pk):
    if request.user.is_authenticated:
        test = Test.objects.get(question_id=pk)
        return render(request, 'test.html', {'test': test})
    else:
        return redirect('home')

def next_test(request, pk):
    if request.user.is_authenticated:
        test = Test.objects.get(question_id=pk+1)
        return render(request, 'test.html', {'test': test})
    else:
        return redirect('home')

def prev_test(request, pk):
    if request.user.is_authenticated:
        test = Test.objects.get(question_id=pk-1)
        return render(request, 'test.html', {'test': test})
    else:
        return redirect('home')

@login_required  # Ensure that the user is logged in to access the profile
def user_profile(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user_profile.html', context)


def edit_profile(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user_profile.html', context)

def terms_and_conditions(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user_profile.html', context)

def settings(request):
    user = request.user
    # Query additional user profile data if using a custom user profile model
    context = {'user': user}
    return render(request, 'user_profile.html', context)

class CustomLogoutView(LogoutView):
    template_name = 'custom_logout.html'  # Optionally, specify a custom logout template

    def get_next_page(self):
        # Customize the redirection logic if needed
        next_page = super().get_next_page()
        # You can add additional logic here if required
        return next_page

def test_home(request):
    return render(request, 'test_home.html')


def view_test_results(request):
    return render(request, 'test_home.html')