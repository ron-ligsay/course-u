# System imports
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from django.db.models import Sum, Case, When, IntegerField, F, Count

# App imports
from apps.assessment.utils import get_test_questions, get_test_question_by_id, create_question_set
from apps.assessment.forms import UserResponseForm, TestCreateForm, TestUpdateForm
from apps.assessment.models import Test, QuestionSet, UserResponse

from apps.website.models import Field, Specialization, UserRecommendations, Skill

# Other Imports
import plotly.express as px
from plotly.offline import plot


# Utilities
from utilities.decorators import unauthenticated_user, allowed_users, admin_only, login_required
from utilities.plots import generate_pie_chart
from utilities.sessions import clear_session_variables#, get_last_question_set, create_or_retrieve_question_set, display_question_set, submit_test

def session_test(request):

    # Test Started is a boolean that indicates if the test has started
    # You cannot exit or start a new test if the test has started
    request.session['test_started'] = True
    test_started = request.session['test_started']
    
    # Question Set ID is the current question set
    request.session['question_set_id'] = 1
    question_set_id = request.session['question_set_id']
    
    # Question Set is a list of User Response objects for the current question set
    # This list are the question ids that needed to be answered
    request.session['question_set'] = [1,2,3,4,5,6,7,8,9,10,11,12]
    question_set = request.session['question_set']
    
    # Number of questions in the question set
    request.session['n_questions'] = 12
    n_questions = request.session['n_questions']

    # Number of questions answered
    request.session['questions_answered'] = 0 
    questions_answered = request.session['questions_answered']

    return redirect('test_overview')

# Create your views here:
@login_required
def start_test(request):
    clear_session_variables(request)

    # If there is no incomplete set, incomplete is None, last set is the last set
    # If there is an incomplete set, incomplete is the set, last set is None
    incomplete, last_set = get_question_set(request.user)

    if incomplete:
        process_incomplete_set(request, incomplete)
    else:
        start = create_new_question_set(request, last_set)

    return redirect('display_question', question_id=start)

def get_question_set(user):
    try:
        incomplete = QuestionSet.objects.filter(user=user, is_completed=False).first()
    except QuestionSet.DoesNotExist:
        incomplete = None
    last_set = None

    if not incomplete: # this means that the user has no incomplete sets
        last_set = QuestionSet.objects.last()


    return incomplete, last_set 

def process_incomplete_set(request, incomplete):
    # Process the incomplete question set
    n_questions = UserResponse.objects.filter(set_id=incomplete.set_id).count()

    if n_questions == incomplete.n_questions:
        # Has answered all questions, but marks as incomplete
        resume_uncompleted_set(request)
    else:
        # Handle incomplete set where UserResponse objects are not equal to n_questions
        handle_incomplete_user_response(request, incomplete)


def handle_incomplete_user_response(request, incomplete):

    unique_fields = incomplete.objects.values('field').distinct()

    for field in unique_fields:
        # get UserResponse objects with the same set_id and field
        n_field_responses = UserResponse.objects.filter(set_id=incomplete.set_id, question__field=field).count()
        
        if n_field_responses < 2: # if the user has not answered 3 questions for this field

            question_ids = incomplete.filter(question__field=field).values_list('question_id', flat=True)

            current_responses = UserResponse.objects.filter(set_id=incomplete.set_id, question__field=field)

            last_question_id = current_responses.last().question.question_id

            n_question_to_add = 2 - n_field_responses

            for question in range(n_question_to_add):
                next_question_id = last_question_id + 1
                next_question = Test.objects.get(question_id=next_question_id)  #get_test_question_by_id(next_question_id)
                UserResponse.objects.create(
                    question=next_question,
                    set_id=incomplete.set_id,
                    is_answered=False,
                )

    question_ids = incomplete.values_list('question_id', flat=True)
    request.session['question_set'] = list(question_ids)

    n_questions = UserResponse.objects.filter(set_id=incomplete.set_id).count()
    request.session['n_questions'] = n_questions
    if n_questions == incomplete.n_questions:
        # Has now complete User Response objects
        handle_incomplete_set(request)
    else:
        # Handle incomplete set where UserResponse objects are not equal to n_questions
        # handle_incomplete_user_response(request, incomplete) # Commented out to avoid infinite loop
        # Critical error, should not happen
        print("Critical error, should not happen")
        pass
        


def handle_incomplete_set(request, incomplete):
    
    # Count the number of unanswered user responses
    n_unanswered = UserResponse.objects.filter(set_id=incomplete.set_id, is_answered=False).count()
    request.session['questions_answered'] = incomplete.n_questions - n_unanswered
    request.session['question_set_id'] = incomplete.set_id
    if n_unanswered == 0: # All questions are answered
        # mark the set as completed
        incomplete.is_completed = True
        incomplete.save()
        # this means that the test is over and redirect to test results
        return redirect('test_results')
    else:
        resume_uncompleted_set(request)


def resume_uncompleted_set(request): 
    request.session['test_started'] = True
    print("Test started!")
    return redirect('test_overview')


def create_new_question_set(request, last_set):
    if not last_set or last_set == 0:
        new_set = 1
    else:
        new_set = last_set.set_id + 1

    QuestionSet.objects.create(set_id=new_set, user=request.user, n_questions=12, is_completed=False, score=0)
    
    request.session['question_set_id'] = new_set
    question_set, start, end = get_test_questions(x=2)
    question_ids = question_set.values_list('question_id', flat=True)

    request.session['question_set'] = list(question_ids)
    request.session['n_questions'] = len(question_ids)
    request.session['questions_answered'] = 0
    request.session['test_started'] = True

    for question in question_set:
        UserResponse.objects.create(
            question=question,
            set_id=new_set,
            is_answered=False,
        )

    print("Created new UserResponse objects")
    return start


def display_question(request, question_id):
    question_set_id = request.session.get('question_set_id')
    question_ids = request.session.get('question_set', [])

    if not (question_set_id and question_ids):
        return HttpResponse("Invalid session data.")

    try:
        question_id = int(question_id)
    except ValueError:
        return HttpResponse("Invalid question ID provided.")

    if question_id not in question_ids:
        return HttpResponse("Invalid question ID provided.")

    question = get_test_question_by_id(question_id)
    user_response = UserResponse.objects.filter(question=question, set_id=question_set_id).first()

    return render(request, 'test/test_page.html', {
        'question': question,
        'question_set_id': question_set_id,
        'user_response': user_response,
    })

