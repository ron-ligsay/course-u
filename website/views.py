from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from website.forms import SignUpForm #UserResponseForm
from website.models import Specialization, Test, JobPosting
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
import json

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

# def next_test(request, pk):
#     if request.user.is_authenticated:
#         test = Test.objects.get(question_id=pk+1)
#         return render(request, 'test.html', {'test': test})
#     else:
#         return redirect('home')

# def prev_test(request, pk):
#     if request.user.is_authenticated:
#         test = Test.objects.get(question_id=pk-1)
#         return render(request, 'test.html', {'test': test})
#     else:
#         return redirect('home')
    

def next_test(request, question_id):
    if request.user.is_authenticated:
        try:
            question = Test.objects.get(question_id=question_id+ 1)
            options = question.options
            return render(request, 'test_page.html', {'question': question, 'options': options})
        except Test.DoesNotExist:
            # Handle the case where there is no next question
            messages.success(request, 'You have completed the test')
            return redirect('home')
    else:
        return redirect('home')

def prev_test(request, question_id):
    if request.user.is_authenticated:
        if question_id > 1:
            question = Test.objects.get(question_id=question_id - 1)
            options = question.options
            return render(request, 'test_page.html',{'question': question, 'options': options})
        else:
            # Handle the case where there is no previous question
            messages.success(request, 'You have reached the first question')
            return redirect('home')
    else:
        return redirect('home')

# def test_page(request, test_id):
#     test = Test.objects.get(pk=test_id)
#     questions = Question.objects.filter(test=test)

#     if request.method == 'POST':
#         form = UserResponseForm(request.POST)
#         if form.is_valid():
#             user_response = form.save(commit=False)
#             user_response.user = request.user  # Set the user for the response
#             user_response.save()
#             return redirect('test_page', test_id=test_id)  # Redirect to the same page to continue the test
#     else:
#         form = UserResponseForm()

#     return render(request, 'test/test_page.html', {'test': test, 'questions': questions, 'form': form})

def display_question(request, question_id):
    question = Test.objects.get(pk=question_id)
    options = question.options
    
    return render(request, 'test_page.html', {'question': question, 'options': options})


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




# def job_list(request):
#     job_postings = JobPosting.objects.all()
#     return render(request, 'job_list.html', {'job_postings': job_postings})

def job_list(request, job_id=None):
    job_postings = JobPosting.objects.all()
    selected_job = None

    if job_id:
        selected_job = get_object_or_404(JobPosting, pk=job_id)

    return render(request, 'job_list.html', {'job_postings': job_postings, 'selected_job': selected_job})

def job_detail(request, job_id):
    job_posting = JobPosting.objects.get(pk=job_id)
    return render(request, 'job_detail.html', {'job_posting': job_posting})

def specialization_page(request, item_id):
    # Retrieve the selected specialization item or return a 404 error if it doesn't exist
    specialization_item = get_object_or_404(Specialization, pk=item_id)

    # Render the specialization_page template with the item
    return render(request, 'specialization_page.html', {'specialization_item': specialization_item})