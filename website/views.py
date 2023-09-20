from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from website.forms import SignUpForm, UserResponseForm
from website.models import Specialization, Test, JobPosting, QuestionSet, UserResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
import json
from django.http import HttpResponse 
import logging
from .utils import *

from django.contrib.sessions.models import Session

logger = logging.getLogger(__name__)

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


#########################################################################
# ----------------------------for job--------------------------------- #
#########################################################################

def test_home(request):
    return render(request, 'test_home.html')

def test_overview(request):
    user = request.user  # Get the current user
    #question_sets = QuestionSet.objects.filter(user=user).all()  # Retrieve question sets for the user
    # retrieve session 
    test_started = request.session.get('test_started', False)  # Use parentheses here

    if test_started:
        question_set_id = request.session.get('question_set_id')
        question_set = request.session.get('question_set')
        questions_answered = request.session.get('questions_answered')

        return render(request, 'test_overview.html', {'question_set_id': question_set_id, 'question_set': question_set, 'questions_answered': questions_answered})
    else:
        # Handle the case where there is no active question set
        return render(request, 'home.html')


def next_test(request, question_id):
    if not request.user.is_authenticated:
        return redirect('home')

    try:
        question_set = request.session.get('question_set')
        question = get_object_or_404(Test, question_id=question_id + 1)
        #if question not in question_set:
        #    raise Test.DoesNotExist

        if question_id + 1 < len(question_set):
            #options = question.options
            return render(request, 'test_page.html', {'question': question})
        if question_id + 1 == len(question_set):
            # This is the last question
            messages.success(request, 'You have completed the test')
            return redirect('test_overview')
        else:
            # Handle the case where the next question is out of bounds
            messages.success(request, 'You have completed the test')
            return redirect('home')

    except: #Test.DoesNotExist:
        messages.success(request, 'You have completed the test')
        return redirect('test_overview')

    #options = question.options
    return render(request, 'test_page.html', {'question': question})#, 'options': options

def prev_test(request, question_id):
    if not request.user.is_authenticated:
        return redirect('home')

    if question_id <= 1:
        messages.success(request, 'You have reached the first question')
        return redirect('test_overview')

    questions = request.session.get('question_set')
    
    # Ensure that the question_id is within a valid range
    if 1 <= question_id - 1 < len(questions):
        question = get_object_or_404(Test, question_id=question_id - 1)
        #question = questions[question_id - 2]  # Subtract 2 to get the previous question
        #options = question.options
        return render(request, 'test_page.html', {'question': question})#, 'options': options
    else:
        # Handle the case where the previous question is out of bounds
        messages.success(request, 'You have reached the first question')
        return redirect('home')



def start_test(request):
    request.session['test_started'] = True

    # Retrieve the last question set
    last_set = QuestionSet.objects.last()

    if last_set:
        # Store the question set ID in the session
        request.session['question_set_id'] = last_set.set_id

        # Retrieve the questions for the question set
        question_set = get_test_questions(x=5)  # Modify this function to filter questions based on the set
        question_ids = question_set.values_list('question_id', flat=True)

        # Store the question IDs in the session
        request.session['question_set'] = list(question_ids)
        request.session['questions_answered'] = 0
        request.session['n_questions'] = len(question_ids)
        # Redirect to the first question
        return redirect('display_question', question_id=question_ids[0])
    else:
        # Handle the case where there's no question set
        return HttpResponse("No question set available.")

def display_question(request, question_id):
    # Retrieve the question set and answered questions from the session
    question_set_id = request.session.get('question_set_id')
    question_ids = request.session.get('question_set', [])
    #questions_answered = request.session.get('questions_answered', 0)

    if not question_set_id:
        # Handle the case where the question set ID is not found in the session
        return HttpResponse("No question set ID found in the session.")

    if not question_ids:
        # Handle the case where the list of question IDs is not found in the session
        return HttpResponse("No question IDs found in the session.")

    if not question_id:
        # Handle the case where the question ID is not provided
        return HttpResponse("No question ID provided.")

    if int(question_id) not in question_ids:
        # Handle the case where the provided question ID is not in the list of question IDs
        return HttpResponse("Invalid question ID provided.")

    # Retrieve the question based on the provided question ID
    question = get_test_question_by_id(question_id)

    # Render the question page with the question and question set information
    return render(request, 'test_page.html', {'question': question, 'question_set_id': question_set_id})#, 'questions_answered': questions_answered



def submit_question(request, question_id):
    if request.user.is_authenticated:
        question = get_object_or_404(Test, question_id=question_id)
        user_response_key = f'user_response_{question_id}'
        if request.method == 'POST':
            form = UserResponseForm(request.POST)
            selected_option = request.POST.get('selected_option')
            if selected_option is not None:
                # Store the user's answer in the session
                request.session[user_response_key] = int(selected_option)

            if form.is_valid():
                selected_option = form.cleaned_data['selected_option']
                is_correct = (selected_option == question.correct_option)

                # Check if a UserResponse with the same question_id and set_id exists
                set_id = request.session.get('question_set_id')
                existing_response = UserResponse.objects.filter(
                    question=question,
                    set_id=set_id,
                ).first()

                if existing_response:
                    # If an existing response is found, update it
                    existing_response.selected_option = selected_option
                    existing_response.is_correct = is_correct
                    existing_response.save()
                else:
                    # Otherwise, create a new UserResponse object
                    UserResponse.objects.create(
                        #user=request.user,
                        question=question,
                        selected_option=selected_option,
                        is_correct=is_correct,
                        set_id=set_id
                    )

                # Redirect to the next question or a completion page
                next_question_id = question_id + 1
                try:
                    next_question = Test.objects.get(pk=next_question_id)
                    options = next_question.options
                    return render(request, 'test_page.html', {'question': next_question, 'options': options, 'form': UserResponseForm()})
                except Test.DoesNotExist:
                    # Handle the case where there is no next question
                    messages.success(request, 'You have completed the test')
                    return redirect('home')
            else:
                # Display the question and form again with validation errors
                options = question.options
                return render(request, 'test_page.html', {'question': question, 'options': options, 'form': form})
        else:
            # Display the question and form for the first time
            options = question.options
            return render(request, 'test_page.html', {'question': question, 'options': options, 'form': UserResponseForm()})
    else:
        return redirect('home')

def submit_test(request):
    if request.method == 'POST':
        # process the submitted test
        
        # retrieve session variables
        #question_set_id = request.session['question_set_id']
        #question_set = QuestionSet.objects.get(pk=question_set_id)
        #questions_answered = request.session['questions_answered']
        test_started = request.session.get('test_started', False)
        questions_answered = request.session.get('questions_answered', 0)

        if test_started:
            # perform actions based on the session data

            # delete session vairables
            del request.session['test_started']
            del request.session['question_set_id']
            del request.session['question_set']
            del request.session['questions_answered']

    return render(request, 'submit_test.html')


def view_test_results(request):
    return render(request, 'test_home.html')



#########################################################################
# ----------------------------for job--------------------------------- #
#########################################################################

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



#########################################################################
# ----------------------------for job--------------------------------- #
#########################################################################
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

#########################################################################
# ----------------------------for job--------------------------------- #
#########################################################################


def specialization_page(request, item_id):
    # Retrieve the selected specialization item or return a 404 error if it doesn't exist
    specialization_item = get_object_or_404(Specialization, pk=item_id)

    # Render the specialization_page template with the item
    return render(request, 'specialization_page.html', {'specialization_item': specialization_item})

#########################################################################
# --------------------- for query testing ----------------------------- #
#########################################################################


def test_query(request):
    questions = get_test_questions(x=1, y=3)
    return render(request, 'test_queries/test_query.html', {'questions': questions})