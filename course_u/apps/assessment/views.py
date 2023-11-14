# System imports
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Case, When, IntegerField, F, Count

# App imports
from apps.assessment.utils import get_test_questions, get_test_question_by_id, create_question_set
from apps.assessment.forms import UserResponseForm, TestCreateForm, TestUpdateForm
from apps.assessment.models import Test, QuestionSet, UserResponse

from apps.website.models import Field, Specialization, UserRecommendations, Skill
from apps.recommender.models import UserSkill

from apps.acad.models import StudentProfile

# Other Imports
import plotly.express as px
from plotly.offline import plot


# Utilities
from utilities.decorators import unauthenticated_user, allowed_users, admin_only, login_required
from utilities.plots import generate_pie_chart
from utilities.sessions import clear_session_variables#, get_last_question_set, create_or_retrieve_question_set, display_question_set, submit_test


def test_home(request):
    return render(request, 'test/test_home.html')

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

    return redirect('test_overview', question_set_id=question_set_id)

# Create your views here:
@login_required
def start_test(request):
    # Check if the user has a student profile
    studentprofile = StudentProfile.objects.filter(user_id=request.user.id).exists()
    if not studentprofile:
        # If the user doesn't have a student profile, redirect to the course selection 
        print("No Student Profile")
        return redirect('select_course')  # Replace 'select_course' with the actual URL name
    else:
        print("Has Student Profile")

    clear_session_variables(request)
    start = None

    # If there is no incomplete set, incomplete is None, last set is the last set
    # If there is an incomplete set, incomplete is the set, last set is None
    incomplete, last_set = get_question_set(request.user)
    print("incomplete: ", incomplete, "last_set: ", last_set)

    if incomplete:
        print("Process Incomplete")
        # process_incomplete_set(request, incomplete)
        return redirect('process_incomplete_set', incomplete=incomplete.set_id)
    else:
        print("Create New Set")
        #start = create_new_question_set(request, last_set)
        #create_new_question_set(request, last_set)
        return redirect('create_new_question_set', last_set=last_set.set_id)
        # Will not return start anymore
        # will have to cut this part and make a different function that will go to display_question
        # if start:
        #     return redirect('display_question', question_id=start)
        # else:
        #     return HttpResponse("Error creating new question set")
    #return redirect('test_overview')

def get_question_set(user):
    print("get_question_set() user: ", user)
    try:
        incomplete = QuestionSet.objects.filter(user=user, is_completed=False).first()
    except QuestionSet.DoesNotExist:
        incomplete = None
    last_set = None

    if not incomplete: # this means that the user has no incomplete sets
        last_set = QuestionSet.objects.last()


    return incomplete, last_set 

def process_incomplete_set(request, incomplete):
    print("process_incomplete_set() incomplete: ", incomplete)
    # Process the incomplete question set
    n_questions = UserResponse.objects.filter(set_id=incomplete).count()
    question_set = QuestionSet.objects.get(set_id=incomplete)
    # get number of questions in the set
    if n_questions == question_set.n_questions:
        print("Complete UserResponse objects")
        # Has complete UserResponse Objects for the set
        #resume_uncompleted_set(request, incomplete)
        return redirect('resume_uncompleted_set', incomplete=incomplete)
    else:
        # Handle incomplete set where UserResponse objects are not equal to n_questions
        # handle_incomplete_user_response(request, incomplete)
        return redirect('handle_incomplete_user_response', incomplete=incomplete)


def handle_incomplete_user_response(request, incomplete):
    print("handle_incomplete_user_response() incomplete: ", incomplete)

    #unique_fields = Field.objects.filter(test__userresponse__set_id=incomplete.set_id).distinct()
    question_set = UserResponse.objects.filter(set_id=incomplete.set_id)
    unique_fields = question_set.objects.values('field').distinct()
    print("unique_fields: ", unique_fields)
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
            

    question_set = UserResponse.objects.filter(set_id=incomplete.set_id, is_answered=False)
    question_ids = list(question_set.values_list('question_id', flat=True))
    request.session['question_set'] = list(question_ids)

    n_questions = UserResponse.objects.filter(set_id=incomplete.set_id).count()
    request.session['n_questions'] = n_questions
    print("n_questions: ", n_questions,"incomplete.n_questions: ", incomplete.n_questions)
    if n_questions == incomplete.n_questions:
        # Has now complete User Response objects
        #handle_incomplete_set(request)
        return redirect('handle_incomplete_set', incomplete=incomplete)
    else:
        # Handle incomplete set where UserResponse objects are not equal to n_questions
        # handle_incomplete_user_response(request, incomplete) # Commented out to avoid infinite loop
        # Critical error, should not happen
        print("Critical error, should not happen")
        return HttpResponse("Critical error, should not happen!")
    return HttpResponse("handle_incomplete_user_response()")


def handle_incomplete_set(request, incomplete):
    print("handle_incomplete_set() incomplete: ", incomplete)
    
    # Count the number of unanswered user responses
    n_unanswered = UserResponse.objects.filter(set_id=incomplete.set_id, is_answered=False).count()
    request.session['questions_answered'] = incomplete.n_questions - n_unanswered
    request.session['question_set_id'] = incomplete.set_id
    request.session['question_set'] = list(UserResponse.objects.filter(set_id=incomplete.set_id).values_list('question_id', flat=True))
    if n_unanswered == 0: # All questions are answered
        # mark the set as completed
        incomplete.is_completed = True
        incomplete.save()
        # this means that the test is over and redirect to test results
        return redirect('test_results')
    else:
        #resume_uncompleted_set(request)
        # return to resume_uncompleted_set
        return redirect('resume_uncompleted_set', incomplete) 
    


def resume_uncompleted_set(request, incomplete): 
    print("resume_uncompleted_set()")
    request.session['question_set_id'] = incomplete
    request.session['question_set'] = list(UserResponse.objects.filter(set_id=incomplete).values_list('question_id', flat=True))
    request.session['test_started'] = True
    request.session['n_questions'] = UserResponse.objects.filter(set_id=incomplete).count()
    request.session['questions_answered'] = UserResponse.objects.filter(set_id=incomplete, is_answered=True).count()
    print("Test started!")
    return redirect('test_overview', question_set_id=incomplete)

def recreate_overwritten_test(request, new_set):
    print("recreate_overwritten_test() new_set: ", new_set)
    # get Test ids from UserResponse where set_id = new_set
    question_set = UserResponse.objects.filter(set_id=new_set)
    question_set = question_set.values_list('question_id', flat=True)
    start = question_set[0]
    end = question_set[-1]

    question_ids = question_ids_and_session_test(request,question_set)
    
    return question_ids, question_set, start, end

def question_ids_and_session_test(request,question_set):
    print("question_ids_and_session_test()")
    question_ids = question_set.values_list('question_id', flat=True)
    request.session['question_set'] = list(question_ids)
    request.session['n_questions'] = len(question_ids)
    request.session['questions_answered'] = 0
    request.session['test_started'] = True
    
    return question_ids


def create_new_question_set(request, last_set):
    print("create_new_question_set() last_set: ", last_set)
    
    start = None

    if not last_set or last_set == 0:
        last_set = 1
    else:
        last_set = last_set + 1

     # Verify first if the User has already taken the test in his current StudentProfile year
    # Get year of User's StudentProfile
    if request.user.is_authenticated:
        try:
            year = StudentProfile.objects.get(user_id=request.user.id).current_year
        except ObjectDoesNotExist:
            year = None  # or some default value
    else:
        year = None  # or some default value
    # Check if the User has already taken the test in his current StudentProfile year
    has_taken_test = QuestionSet.objects.filter(user=request.user, year=year).exists()

    if has_taken_test:
        # If the User has already taken the test in his current StudentProfile year, return an error
        # return HttpResponse("You have already taken the test in your current StudentProfile year.")
        
        # Have you Completed the School Year? Yes or No, goes to handle_school_year
        print("Has Take Test")
        return redirect('check_school_year')
    
        # handle_school_year
        #print("has_taken_test: ", has_taken_test, "overwritten: ", overwritten, "no_record: ", no_record, "completed_year: ", completed_year)
    else: # No test in current year
        # QuestionSet.objects.create(set_id=new_set, user=request.user, n_questions=12, is_completed=False, score=0)
        print("No overwritten, no_record, and completed_year")
        no_record = True
        # year = StudentProfile.objects.get(user_id=request.user.id).current_year
        # continue to create new question set
        # continue_create_new_question_set # no record
        # basically this is a new set for the user
        return redirect('continue_create_new_question_set', last_set=last_set)
    
    return HttpResponse("create_new_question_set()")

def check_school_year(request):
    print("Render check_school_year.html")
    return render(request, 'test/check_school_year.html')

def check_school_year_choice(request, choice):
    print('handle_school_year() choice: ', choice)
    if choice == 'yes':
        # User has completed the school year
        # completed_year = True
        
        #return HttpResponse("You have completed the school year. You can proceed.")
        # to check_school_year
        return redirect('check_school_year_status', status='completed')
    elif choice == 'no':
        # User hasn't completed the school year
        # completed_year = False

        #return HttpResponse("Sorry, you need to finish the school year to retake the test.")
        return redirect('check_school_year_status', status='not_completed')
    # Handle other cases or invalid choices
    return HttpResponse("Invalid choice.")

def check_school_year_status(request, status=None):
    print('check_school_year() status: ', status)
    if status == 'completed':
        messages.info(request, "You have completed the school year. You can proceed.")       
        course_id = StudentProfile.objects.get(user_id=request.user.id).enrolled_courses_id
        return redirect('select_year', course_id=course_id)
    
    elif status == 'not_completed':
        messages.info(request, 'Sorry, you need to finish the school year to retake the test.')
        # if user is admin
        if request.user.is_superuser:
            return render(request, 'test/create_or_overwrite_test.html',)

        
        # return to test home
        return redirect('test_home')
    else:
        return HttpResponse("check_school_year Invalid status.")

def create_or_overwrite_test(request, action):
    print('create_or_overwrite_test() action: ', action)
    year = request.user.studentprofile.current_year
    if action == 'delete':
        # Handle the "Delete Existing Test" action
        # For example, delete the existing test and display a message
        QuestionSet.objects.filter(user=request.user, year=year).delete()
        messages.success(request, 'Your existing test has been deleted. You can now start a new test.')
        # return redirect('test_home')
        # Continue to create new question set
        # continue_create_new_question_set # No record
        return redirect('continue_create_new_question_set', last_set=0)

    elif action == 'overwrite':
        # Handle the "Overwrite Existing Test" action
        # For example, update the existing test or perform necessary actions
        # Overwrite the existing test (you can modify this part as needed)
        existing_test = QuestionSet.objects.get(user=request.user, year=year)
        existing_test.n_questions = 12  # Update the number of questions or any other relevant changes
        existing_test.is_completed = False
        existing_test.score = 0
        existing_test.save()

         # remove selected options from UserResponse
        user_responses = UserResponse.objects.filter(set_id=existing_test.set_id)
        for user_response in user_responses:
            user_response.selected_option = None
            user_response.is_correct = None
            user_response.is_answered = False
            user_response.save()

        # overwritten = True # no_record = False
        # return redirect('continue_create_new_question_set', last_set=None, overwritten=True, no_record=False)
        # return this to resume_uncompleted_set
        return redirect('resume_uncompleted_set', existing_test)
    elif action == 'just_delete':
         # Handle the "Delete Existing Test" action
        # For example, delete the existing test and display a message
        QuestionSet.objects.filter(user=request.user, year=year).delete()
        messages.success(request, 'Your existing test has been deleted. You can now start a new test.')
        return redirect('test_home')
        # Continue to create new question set
        # continue_create_new_question_set

    elif action == 'home':
        return redirect('test_home')
    
    else:
        return HttpResponse("Invalid action provided.")
    
    # Handle other cases or invalid choices
    return HttpResponse("Invalid choice.")

def continue_create_new_question_set(request, last_set):
    print('continue_create_new_question_set() last_set: ', last_set)
    new_set = None
    if last_set == 0 or last_set == None:
        # get last set
        try:
            last_set = QuestionSet.objects.last().set_id
        except:
            print("No Sets, Exception: ", Exception)
            last_set = None
        if last_set == 0 or last_set == None:
            new_set = 1
        else:
            new_set = last_set + 1
    else:
        new_set = last_set + 1 

    year = StudentProfile.objects.get(user_id=request.user.id).current_year
    
    print("if no_record, Set: ", new_set, "created for user: ", request.user)
    request.session['question_set_id'] = new_set
    
    
    question_set, start, end = get_test_questions(x=2)
    question_ids = question_ids_and_session_test(request,question_set)      


    # Create QuestionSet object
    QuestionSet.objects.create(
        set_id=new_set,
        user=request.user,
        n_questions=len(question_ids),
        is_completed=False,
        score=0,
        year=year,
    )

    for question in question_set:
        UserResponse.objects.create(
            question=question,
            set_id=new_set,
            is_answered=False,
        )
        print("Created new UserResponse objects")
    start = question_ids[0]

    return redirect('display_question', question_id=start)


def test_overview(request, question_set_id=None):
    print("Test Overview()")
    user = request.user
    is_admin = user.is_superuser
    
    question_set = request.session.get('question_set', [])
    print("question_set: ", question_set)
    question_set_id = request.session.get('question_set_id')
    print("question_set_id: ", question_set_id)
    questions_answered = request.session.get('questions_answered', 0)
    print("questions_answered: ", questions_answered)
    if not question_set_id:
        return HttpResponse("Invalid session data.")

    try:
        question_set = request.session.get('question_set', [])
        if not question_set:
            try:
                question_set = QuestionSet.objects.get(set_id=question_set_id)
            except QuestionSet.DoesNotExist:
                return HttpResponse("Invalid question set provided.")
    except ValueError:
        return HttpResponse("Invalid question set provided.")
    
    n_question = request.session.get('n_questions', 0)
    if n_question != len(question_set) or n_question != 12:
        print("Some UserResponse Objects are missing")
        n_question = len(question_set)
        request.session['n_questions'] = n_question


    # Retrieve the user's responses for the current question set
    try:
        user_responses = UserResponse.objects.filter(set_id=question_set_id)
    except:
        return HttpResponse("Invalid question set provided.")
    
    # Create a dictionary to store question info and its answered status
    question_info = []
    # Iterate through the questions in the current question set
    for question in question_set:
        # get question is_answered status
        # Get the UserResponse object for the current question
        try:
            user_response = user_responses.filter(question=question).first()
        except UserResponse.DoesNotExist:
            return HttpResponse("Invalid question set provided.")
        
        # Get the is_answered status of the UserResponse object
        has_answered = user_response.is_answered if user_response else False
        is_correct = user_response.is_correct if user_response else False

        print("has_answered: ", has_answered, "question: ", question)
        question = Test.objects.get(pk=question)
        # Create a dictionary with question and answered status
        question_info.append({'question': question, 'has_answered': has_answered, 'n_question': n_question, 'is_correct': is_correct})

    return render(request, 'test/test_overview.html', {
        'question_set_id': question_set_id, 
        'question_info': question_info, 
        'is_admin': is_admin,
        'n_question': n_question,
        'questions_answered': questions_answered,
        })


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
    print("Selected option: ", user_response.selected_option)
    return render(request, 'test/test_page.html', {
        'question': question,
        'question_set_id': question_set_id,
        'user_response': user_response,
    })


def next_test(request, question_id, question_set_id):
    question_set = request.session.get('question_set')
    n_question = request.session.get('n_questions', 0)

    if question_id + 1 < n_question:
        question = get_object_or_404(Test, question_id=question_id + 1)
        #return render(request, 'test/test_page.html', {'question': question})
        return redirect('display_question', question_id=question_id + 1)

    if question_id + 1 == n_question:
        messages.success(request, 'You have completed the test')
        return redirect('test_overview', question_set_id=question_set_id)
    else:
        messages.success(request, 'You have completed the test')
        return redirect('home')


def prev_test(request, question_id, question_set_id):
    if question_id <= 1:
        messages.success(request, 'You have reached the first question')
        return redirect('test_overview', question_set_id=question_set_id)

    questions = request.session.get('question_set')

    if 1 <= question_id - 1 < len(questions):
        question = get_object_or_404(Test, question_id=question_id - 1)
        #return render(request, 'test/test_page.html', {'question': question})
        return redirect('display_question', question_id=question_id - 1)
    else:
        messages.success(request, 'You have reached the first question')
        return redirect('home')
    
from django.shortcuts import get_object_or_404

    # The submit_question view function is responsible for handling the submission of a test question answer.
def submit_question(request, question_id):
    # The function first retrieves the question object from the database using the get_object_or_404 function.
    question = get_object_or_404(Test, question_id=question_id)
    user_response_key = f'user_response_{question_id}'
    # The function then checks the request method. If it is a POST request, it means that the user is submitting an answer.
    if request.method == 'POST':
        form = UserResponseForm(request.POST)
        selected_option = request.POST.get('selected_option')

        # The function then checks if the selected option is not None. If it is, it means that the user has selected an option.
        if selected_option is not None:
            request.session[user_response_key] = int(selected_option)
            print("Selected option: ", selected_option)
        # The function then checks if the form is valid. If it is, it means that the user has selected an option.
        if form.is_valid():
            set_id = request.session.get('question_set_id')
            is_correct = (int(selected_option) == int(question.correct_option))
            print("selected option: ", selected_option, "correct option: ", question.correct_option, "is_correct: ", is_correct)
            #The function then checks if the answer exists in the database. If it does, it means that the user has already answered the question.
            existing_response = UserResponse.objects.filter(question=question.question_id, set_id=set_id).first()

            if existing_response:
                if existing_response.selected_option != None:
                    #messages.warning(request, 'You have already answered this question')
                    print("You have already answered this question")
                else:
                    questions_answered = request.session.get('questions_answered', 0)
                    request.session['questions_answered'] = questions_answered + 1
                    print("questions_answered: ", questions_answered, " and added to session variables")
                existing_response.selected_option = selected_option
                existing_response.is_correct = is_correct
                existing_response.is_answered = True
                existing_response.save()
                print("Existing response: ", existing_response, "selected option", selected_option)
                #messages.success(request, 'Your answer has been updated')
                print("Updated!")
                # Note that if the user has already answered the question, the function will update the existing UserResponse object instead of creating a new one.
                # But is should record the answer at questions_answered session variables at first
            else: 
                userresponse = UserResponse.objects.create(
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct,
                    set_id=set_id,
                    is_answered=True,
                )
                userresponse.save()
                messages.success(request, 'Your answer has been submitted')
                # add questions answered
                questions_answered = request.session.get('questions_answered', 0)
                request.session['questions_answered'] = questions_answered + 1

            print("Submitted!")
            current_question_id = question_id
            question_ids = request.session.get('question_set', [])
            
            #The function then checks if there are more questions in the set. If there are, it means that the test is not over.
            try:
                current_index = question_ids.index(current_question_id)
                next_question_id = question_ids[current_index + 1]
                
                if next_question_id == max(question_ids):
                    messages.success(request, 'You have completed the test')
                    return redirect('test_overview', question_set_id=set_id)
                # else
                next_question = get_object_or_404(Test, question_id=next_question_id)
                options = next_question.options
                return render(request, 'test/test_page.html', {
                    'question_set_id': set_id,
                    'question': next_question, 'options': options, 'form': UserResponseForm()
                    })
            except (ValueError, IndexError):
                messages.warning(request, 'Invalid question ID')
            
            # The function then redirects the user to the test overview page.
            return redirect("test_overview", question_set_id=set_id)            
        # If the form is not valid, it means that the user has not selected an option.
        else:
            options = question.options
            return render(request, 'test/test_page.html', {'question': question, 'options': options, 'form': form})
    #If the request method is not a POST request, it means that the user is not submitting an answer.
    else:
        options = question.options
        return render(request, 'test/test_page.html', {'question': question, 'options': options, 'form': UserResponseForm()})


def submit_test(request):
    question_set_id = request.session.get('question_set_id')
    unfinished_response = UserResponse.objects.filter(set_id=question_set_id, is_answered=False).count()

    if unfinished_response == 0:
        test_started = request.session.get('test_started', False)
        #question_set_id = request.session.get('question_set_id')
        
        if test_started:
            question_set = QuestionSet.objects.get(set_id=question_set_id)
            question_set.is_completed = True
            total_correct = UserResponse.objects.filter(set_id=question_set_id, is_correct=True).count()
            question_set.score = total_correct
            question_set.save()
            save_user_skills(request, question_set_id)
            clear_session_variables(request)
            messages.success(request, 'You have completed the test')
            return redirect('student_test_report', question_set_id=question_set_id)
        else:
            messages.success(request, 'You have not started the test')
            return redirect('home')
    else:
        messages.success(request, 'You have not answered all questions')
        question_set_id = request.session.get('question_set_id')
        #return redirect('test_overview', question_set_id=question_set_id)
        return redirect('test_overview', question_set_id=question_set_id)

def save_user_skills(request, set_id):
    skill_correct_counts = Skill.objects.filter(
        test__userresponse__set_id=set_id,
        test__userresponse__is_correct=True
    ).annotate(correct_count=Count('test__userresponse'))

    # save to userskill
    for skill in skill_correct_counts:
        print("skill: ", skill)
        userskill = UserSkill.objects.create(
            user=request.user,
            skill=skill,
            level=skill.correct_count,
        )
        userskill.save()

    return



def view_test_results(request):
    return render(request, 'test/test_home.html')

def create_test(request):
    
    form = TestCreateForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = TestCreateForm(request.POST)
        if form.is_valid():
            form.save()
            print('form is valid!')
            messages.success(request, 'Your test has been created!')
            #return redirect('/')
            return HttpResponse('Your test has been created!')
        else:
            messages.success(request, 'Your test has not been created!')
            print("form is not valid!")
            #return redirect('/')
            return HttpResponse('Your test has not been created!')
    
    context = {'form' : form}
    return render(request, 'test/create_test.html', context)



def update_test(request, question_id):
    
    return render(request, 'test/update_test.html')


@login_required
def admin_test_report(request):

    # from questionset get all
    #set = QuestionSet.objects.all()
    scores =  QuestionSet.objects.values('score')
    user_ids = QuestionSet.objects.values('user_id')
    user_ids = [user_id['user_id'] for user_id in user_ids]
    # get username using user_id from set
    username = []
    for id in user_ids:
        username.append(User.objects.get(id=id))
    
    scores_list = []
    for score in scores:
        scores_list.append(QuestionSet.objects.filter(score=score).count())

    student_scores = dict(zip(username, scores))


    return render(request, 'test/admin_test_report.html', {'student_scores' : student_scores})


def student_test_report(request, question_set_id):
    print("student_test_report() question_set_id: ", question_set_id)

     # get user results from QuestionSet
    user_id = request.user.id
    user_results = QuestionSet.objects.filter(user_id=user_id)

    # get user name
    username = User.objects.get(id=user_id)

    field_correct_answers = Field.objects.filter(
        test__userresponse__set_id=question_set_id,
    ).annotate(
        total_correct=Sum(
            Case(
                When(test__userresponse__is_correct=True, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
    )

    # You can access the field_name and total_correct values
    for field in field_correct_answers:
        print(field.field_name, field.total_correct)
    
    
    print("values: ", field_correct_answers.values("total_correct"))
    print("names: " , field_correct_answers.values("field_name"))        

    # Create a plotly pie chart
    fig = generate_pie_chart(field_correct_answers, 'Correct Answers per Field')

    # Get top 3 fields with the most correct answers
    top_fields = field_correct_answers.order_by('-total_correct')[:3]

    # You can access the field_name and total_correct values
    for field in top_fields:
        print(field.field_name, field.total_correct)

    
     # Save recommendation to UserRecommendation
    user_recommendation = UserRecommendations.objects.create(
        user=request.user,
        field_1=top_fields[0],
        field_2=top_fields[1],
        field_3=top_fields[2],
        score_1=top_fields[0].total_correct,
        score_2=top_fields[1].total_correct,
        score_3=top_fields[2].total_correct,
        # Additional Info Goes here, for example explanation of the recommendation
    )  

    # Save the recommendation 
    user_recommendation.save()

    # check  if user_recommendation is saved
    print("user_recommendation: ", user_recommendation)

    
#    # Get all the UserResponse instances related to the question_set_id and where is_correct=True
#     correct_responses = UserResponse.objects.filter(set_id=question_set_id, is_correct=True)

#     # Get all the Test instances related to these UserResponse instances
#     tests = Test.objects.filter(userresponse__in=correct_responses)

#     # Get a count of correct user responses for each skill
#     skill_correct_counts = Skill.objects.filter(
#         tests__in=tests
#     ).annotate(correct_count=Count('tests'))

#     # Create a bar graph for correct skill counts
#     skill_names = list(skill_correct_counts.values_list("skill", flat=True))
#     correct_counts = list(skill_correct_counts.values_list("correct_count", flat=True))

#     if len(skill_names) == 0:
#         skill_names = ["No Skills"]
#         correct_counts = [0]
    # Get a count of correct user responses for each skill
    skill_correct_counts = Skill.objects.filter(
        test__userresponse__set_id=question_set_id,
        test__userresponse__is_correct=True
    ).annotate(correct_count=Count('test__userresponse'))

    # Create a bar graph for correct skill counts
    skill_names = list(skill_correct_counts.values_list("skill", flat=True))
    correct_counts = list(skill_correct_counts.values_list("correct_count", flat=True))


    print("skill_names: ", skill_names)
    print("correct_counts: ", correct_counts)

    bar_fig = px.bar(
        x=skill_names,
        y=correct_counts,
        labels={'x': 'Skill', 'y': 'Correct Count'},
        title='Correct Responses per Skill'
    )

    bar_plot = plot(bar_fig, output_type='div')

    return render(request, 'test/test_result.html', {
        'username': username,
        'top_fields': top_fields,
        'graph': fig.to_html(full_html=False, default_height=500, default_width=700),
        'bar_plot': bar_plot 
    })


@login_required
def student_test_report_overall(request):

    # Get user results from all QuestionSets
    user_id = request.user.id
    user_results = QuestionSet.objects.filter(user_id=user_id)

    if user_results.count() != 0:
        print("user_results: ", user_results)
        # Get user name
        username = User.objects.get(id=user_id)

        # Query to get total correct answers per field for all QuestionSets
        field_correct_answers = Field.objects.filter(
            test__userresponse__set__user_id=user_id,
        ).annotate(
            total_correct=Sum(
                Case(
                    When(test__userresponse__is_correct=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )

        # You can access the field_name and total_correct values
        for field in field_correct_answers:
            print(field.field_name, field.total_correct)

        # Create a plotly pie chart
        fig = generate_pie_chart(field_correct_answers, 'Correct Answers per Field')

        # Get top 3 fields with the most correct answers
        top_fields = field_correct_answers.order_by('-total_correct')[:3]

        # You can access the field_name and total_correct values
        for field in top_fields:
            print(field.field_name, field.total_correct)

        # Initialize dictionaries to store skill counts
        skill_correct_counts = {}
        skill_total_counts = {}

        # Loop through each question set and collect skill counts
        for question_set in user_results:
            # Fetch user responses for the question set
            user_responses = UserResponse.objects.filter(set=question_set)
            for user_response in user_responses:
                if user_response.is_correct:
                    # Increment the correct count for each skill associated with the correct response
                    for skill in user_response.question.skills.all():
                        skill_name = skill.skill
                        skill_correct_counts[skill_name] = skill_correct_counts.get(skill_name, 0) + 1
                # Increment the total count for each skill associated with the response
                for skill in user_response.question.skills.all():
                    skill_name = skill.skill
                    skill_total_counts[skill_name] = skill_total_counts.get(skill_name, 0) + 1

        # Create a bar graph for correct skill counts
        skill_names = list(skill_correct_counts.keys())
        correct_counts = list(skill_correct_counts.values())

        # print("skill_names: ", skill_names)
        # print("correct_counts: ", correct_counts)
        try:
            bar_fig = px.bar(
                x=skill_names,
                y=correct_counts,
                labels={'x': 'Skill', 'y': 'Correct Count'},
                title='Correct Responses per Skill'
            )

            bar_plot = plot(bar_fig, output_type='div')
        except:
            bar_plot = None
            #logger.error("Error in creating bar graph for correct skill counts")
            print("Error in creating bar graph for correct skill counts")

        return render(request, 'test/test_result.html', {
            'username': username,
            'top_fields': top_fields,
            'graph': fig.to_html(full_html=False, default_height=500, default_width=700),
            'bar_plot': bar_plot
        })
    else:
        # Handle the case where the user has not taken any tests
        print("You have not taken any tests yet.")
        return HttpResponse("You have not taken any tests yet.")

def test_query(request):
    questions,start,end = get_test_questions(x=1, y=5)
    return render(request, 'test_queries/test_query.html', {'questions': questions})



################################
#           Test CRUD          #
################################



class QuestionListView(ListView):
    model = Test
    template_name = 'question_list.html'
    context_object_name = 'questions'

class QuestionCreateView(CreateView):
    model = Test
    template_name = 'question_form.html'
    fields = '__all__'

class QuestionUpdateView(UpdateView):
    model = Test
    template_name = 'question_form.html'
    fields = '__all__'

class QuestionDeleteView(DeleteView):
    model = Test
    template_name = 'question_confirm_delete.html'
    success_url = reverse_lazy('question_list')