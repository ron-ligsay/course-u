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

# Create your views here:

def test_home(request):
    return render(request, 'test/test_home.html')

@login_required
def start_test(request):

    question_per_field = 2

    # Clear session variables
    clear_session_variables(request)

    # Check user's QuestionSet if it has incomplete test
    try:
        incomplete = QuestionSet.objects.filter(user=request.user, is_completed=False).first()
        print("incomplete Question Set: ", incomplete)
        last_set = 0
    except QuestionSet.DoesNotExist:
        incomplete = None
        # If none, get the last question set
        last_set = QuestionSet.objects.last()
        print("last_set: ", last_set)

    # If yes, retrieve the last question set
    if incomplete:
        print("You have incomplete test! Retrieving the last question set...")
        incomplete_set_id = incomplete.set_id

        # Store the question set ID in the session
        request.session['question_set_id'] = incomplete_set_id

        # Retrieve the questions for the question set, where set_id = incomplete_set_id
        question_set = UserResponse.objects.filter(set_id=incomplete_set_id)

        # get number of questions
        n_questions = question_set.count()

        # Store the question IDs in the session
        question_ids = list(question_set.values_list('question_id', flat=True))
        request.session['question_set'] = question_ids

        n_questions = len(question_set)
        print("n_questions: ", n_questions, "question_ids: ", question_ids)
        request.session['n_questions'] = n_questions

        # Check if UserResponse with set_id are equal to n_questions
        if n_questions == incomplete.n_questions:
            # If yes, redirect to test_overview
            print("You have complete Responses n_questions: ", n_questions, "incomplete.n_questions: ", incomplete.n_questions, "equal!")
            print("Redirecting to test_overview")

            # need to store session variables!!! -----------------------------------------------------------------------------------------------------!!!

            request.session['test_started'] = True
            print("Test started!")

            return redirect('test_overview')
        else:
            print("You have incomplete Responses n_questions: ", n_questions, "incomplete.n_questions: ", incomplete.n_questions, "not equal!")
            # count number of unfinished response on UserResponse per test Field
            # get unique fields
            unique_fields = question_set.objects.values('field').distinct()

            print("fields: ", unique_fields)


            for field in unique_fields:
                # get UserResponse with set_id 
                n_field_responses = UserResponse.objects.filter(set_id=incomplete_set_id, question__field=field).count()
                print("n_field_responses: ", n_field_responses, "field: ", field)

                if n_field_responses < question_per_field:
                    # get list of question_id in this field
                    question_ids = question_set.filter(question__field=field).values_list('question_id', flat=True)

                    # get current UserResponse in this field
                    current_responses = UserResponse.objects.filter(set_id=incomplete_set_id, question__field=field)

                    # get last question_id in this field
                    last_question_id = current_responses.last().question.question_id
                    
                    # get difference between question_per_field and n_field_responses
                    n_questions_to_add = question_per_field - n_field_responses
                    print("n_questions_to_add: ", n_questions_to_add, "in field:", field)
                    # create UserResponse objects
                    for question in range(n_questions_to_add):
                        # get next question_id for UserResponse in this field
                        next_question_id = last_question_id + 1
                        next_question = Test.objects.get(question_id=next_question_id)
                        print("last question: ", current_responses.last(),"next_question_id: ", next_question_id)
                        UserResponse.objects.create(
                            question=next_question,
                            set_id=incomplete_set_id,
                            is_answered=False,
                        )
                        print("Created a UserResponse object for question: ", next_question_id)    

            # get UserResponses with set_id and is_answered=False
            question_set = UserResponse.objects.filter(set_id=incomplete_set_id, is_answered=False)
            question_ids = list(question_set.values_list('question_id', flat=True))
            # save unfinished question_set to session
            request.session['question_set'] = question_ids

            # number of questions
            n_questions = len(question_set)
            request.session['n_questions'] = n_questions
            print("n_questions: ", n_questions, "question_ids: ", question_ids)
            # questions to be answered, store in session
            request.session['questions_answered'] = 0

            # get first question_id in question_set
            start = question_set.first().question.question_id

            # Start test
            request.session['test_started'] = True
            print("Test started!")
    else:
        # If no, create a new question set
        print("No incomplete test! Creating a new test...")
        # Create new question set
        
        try:
            # get last test
            last_set = QuestionSet.objects.last()
            print("last_set: ", last_set)
            if last_set == 0 or last_set is None:
                # No question set exists, start a new test
                new_set = 1
            else:
                # get last set_id
                new_set = last_set.set_id + 1
            
        except QuestionSet.DoesNotExist:
            print("No question set exists, start a new test!")
            new_set = 1
        except:
            print("Error in getting last_set")
            new_set = 1

        QuestionSet.objects.create(set_id=new_set, user=request.user, n_questions=12, is_completed=False, score=0)

        # Store the question set ID in the session
        request.session['question_set_id'] = new_set

        # Retrieve the questions for the question set, using get_test_questions()
        question_set, start, end = get_test_questions(x=2) # x = 2, 2 questions per Field
        
        question_ids = question_set.values_list('question_id', flat=True)

        # Store the question IDs in the session
        request.session['question_set'] = list(question_ids)

        n_questions = len(question_ids)
        request.session['n_questions'] = n_questions

        # Create new UserResponse objects
        for question in question_set:
            UserResponse.objects.create(
                question=question,
                set_id=new_set,
                is_answered=False,
            )
        
        print("Created new UserResponse objects")

        # store questions_answered in session
        request.session['questions_answered'] = 0

        # Start test
        request.session['test_started'] = True
        
        print("Test started!")


    return redirect('display_question', question_id=start)


def display_question(request, question_id):
    print("display_question() question_id: ", question_id)
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

    # Retrieve the UserResponse object for the current question and question set
    user_response = UserResponse.objects.filter(question=question, set_id=question_set_id).first()

    # Render the question page with the question and question set information
    return render(request, 'test/test_page.html', {
        'question': question, 'question_set_id': question_set_id,
        'user_response': user_response, 
        })#, 'questions_answered': questions_answered


def test_overview(request):
    print("Test Overview()")
    user = request.user
    is_admin = user.is_superuser

    # Retrieve the current session's question set
    question_set_id = request.session.get('question_set_id')
    #question_set = QuestionSet.objects.get(set_id=question_set_id)
    question_set = request.session.get('question_set', [])
    n_question = request.session.get('n_questions', 0)

    # Retrieve the user's responses for the current question set
    user_responses = UserResponse.objects.filter(set_id=question_set_id)

    # Create a dictionary to store question info and its answered status
    question_info = []

    # Iterate through the questions in the current question set
    for question in question_set:
        # get question is_answered status
         # Get the UserResponse object for the current question
        user_response = user_responses.filter(question=question).first()

        # Get the is_answered status of the UserResponse object
        has_answered = user_response.is_answered if user_response else False

        print("has_answered: ", has_answered, "question: ", question)
        question = Test.objects.get(pk=question)
        # Create a dictionary with question and answered status
        question_info.append({'question': question, 'has_answered': has_answered, 'n_question': n_question})

    return render(request, 'test/test_overview.html', {'question_set_id': question_set_id, 'question_info': question_info, 'is_admin': is_admin})

def next_te12121st(request, question_id):
    print("next_test() question_id: ", question_id)
    try:
        question_set = request.session.get('question_set')
        n_question = request.session.get('n_questions', 0)
        question = get_object_or_404(Test, question_id=question_id + 1)
        #if question not in question_set:
        #    raise Test.DoesNotExist

        if question_id + 1 < n_question:
            #options = question.options
            return render(request, 'test/test_page.html', {'question': question})
        if question_id + 1 == n_question:
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
    return render(request, 'test/test_page.html', {'question': question})#, 'options': options

def prev_test(request, question_id):
    print("prev_test() question_id: ", question_id)
    if question_id <= 1:
        messages.success(request, 'You have reached the first question')
        return redirect('test_overview')

    questions = request.session.get('question_set')
    
    # Ensure that the question_id is within a valid range
    if 1 <= question_id - 1 < len(questions):
        question = get_object_or_404(Test, question_id=question_id - 1)
        #question = questions[question_id - 2]  # Subtract 2 to get the previous question
        #options = question.options
        return render(request, 'test/test_page.html', {'question': question})#, 'options': options
    else:
        # Handle the case where the previous question is out of bounds
        messages.success(request, 'You have reached the first question')
        return redirect('home')


def submit_question(request, question_id):
    print("submit_question() question_id: ", question_id)

    # Retrieve the current question
    question = get_object_or_404(Test, question_id=question_id)

    user_response_key = f'user_response_{question_id}'
    print("user_response_key: ", user_response_key)

    # Get the user's response form data
    if request.method == 'POST':
        form = UserResponseForm(request.POST)
        selected_option = request.POST.get('selected_option')

        if selected_option is not None:
            # Store the user's answer in the session
            request.session[user_response_key] = int(selected_option)

        if form.is_valid():
            selected_option = form.cleaned_data['selected_option']
            is_correct = (selected_option == question.correct_option)

            # Get the current question set ID
            set_id = request.session.get('question_set_id')
            
            # Check if a UserResponse with the same question_id and set_id exists
            existing_response = UserResponse.objects.filter(
                question=question.question_id,set_id=set_id
                ).first()

            if existing_response:
                # If an existing response is found, update it
                existing_response.selected_option = selected_option
                existing_response.is_correct = is_correct
                existing_response.is_answered = True
                existing_response.save()
                messages.success(request, 'Your answer has been updated')
            
            else:
                # Otherwise, create a new UserResponse object
                UserResponse.objects.create( #user=request.user, #response=None,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct,
                    set_id=set_id,
                    is_answered=True,
                )

                messages.success(request, 'Your answer has been submitted')
            
            current_question_id = question_id

            # get questions_ids
            question_ids = request.session.get('question_set', [])

            # Find the index of the current question ID in the list
            try:
                # Calculate the index of the next question
                current_index = question_ids.index(current_question_id)
                next_question_id = question_ids[current_index + 1]

                # Check if this is the last question by comparing with the maximun ID
                max_question_id = max(question_ids)
                if next_question_id == max_question_id:
                    messages.success(request, 'You have completed the test')
                    return redirect('test_overview')

                # Retrieve the next question and its options
                next_question = get_object_or_404(Test, question_id=next_question_id)
                options = next_question.options
                return render(request, 'test/test_page.html', {'question': next_question, 'options': options, 'form': UserResponseForm()})
            
            except ValueError:
                # Handle the case where the current_question_id is not found in the list
                messages.warning(request, 'Invalid question ID')
            except IndexError:
                # Handle the case where there is no next question
                messages.success(request, 'You have completed the test')
                return redirect('home')
        else:
            # Display the question and form again with validation errors
            options = question.options
            return render(request, 'test/test_page.html', {'question': question, 'options': options, 'form': form})
    else:
        # Display the question and form for the first time
        options = question.options
        return render(request, 'test/test_page.html', {'question': question, 'options': options, 'form': UserResponseForm()})

    return redirect('home')

def submit_test(request):
    print("submit_test()")
    # process the submitted test
    set_id = request.session.get('question_set_id')
    unfinished_response = UserResponse.objects.filter(set_id=set_id, is_answered=False).count()
    print("unfinished_response: ", unfinished_response) 

    if unfinished_response == 0:       
        # retrieve session variables
        #question_set_id = request.session['question_set_id']
        #question_set = QuestionSet.objects.get(pk=question_set_id)
        #questions_answered = request.session['questions_answered']
        test_started = request.session.get('test_started', False)
        print("test_started: ", test_started)
        questions_answered = request.session.get('questions_answered', 0)
        question_set_id = request.session.get('question_set_id')
        if test_started:
            # perform actions based on the session data

            # update QuestionSet object where set_id = question_set_id
            question_set = QuestionSet.objects.get(set_id=question_set_id)
            question_set.is_completed = True
            # count number of correct answers on UserResponse objects where set_id = question_set_id
            total_correct = UserResponse.objects.filter(set_id=question_set_id, is_correct=True).count()
            question_set.score = total_correct
            question_set.save()
            print("Saving QuestionSet object: ", question_set)
            print("Total correct: ", total_correct, "is completed: ", question_set.is_completed, "score: ", question_set.score)
            print("QuestionSet object saved!")
            # Clear session variables
            clear_session_variables(request)

            messages.success(request, 'You have completed the test')
            print('You have completed the test')
            return redirect('student_test_report', question_set_id=question_set_id)
        else:
            messages.success(request, 'You have not started the test')
            print('You have not started the test')
            return redirect('home')
    else:
        messages.success(request, 'You have not answered all questions')
        print("unfinished_response: ", unfinished_response, "YOU ARE NOT YET FINISHED!")
        # get question_set_id
        question_set_id = request.session.get('question_set_id')
        # back to test_overview
        return redirect('test_overview', question_set_id=question_set_id)


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

    # Get a count of correct user responses for each skill
    skill_correct_counts = Skill.objects.filter(
        test__userresponse__set_id=question_set_id,
        test__userresponse__is_correct=True
    ).annotate(correct_count=Count('test__userresponse'))

    # Create a bar graph for correct skill counts
    skill_names = list(skill_correct_counts.values_list("skill", flat=True))
    correct_counts = list(skill_correct_counts.values_list("correct_count", flat=True))

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






def check_school_year(request):
    if request.method == 'POST':
        completed_year = request.POST.get('completed_year', '')

        if completed_year == 'yes':
            # User has completed the school year, redirect to the 'create_or_overwrite_test' view
            return redirect('create_or_overwrite_test')

        elif completed_year == 'no':
            # User hasn't completed the school year, display a message
            return HttpResponse("Sorry, you need to finish the school year to retake the test.")
    
    return render(request, 'check_school_year.html')



def create_or_overwrite_test(request):
    year = request.user.studentprofile.current_year

    # Check if the User has already taken the test in their current StudentProfile year
    has_taken_test = QuestionSet.objects.filter(user=request.user, year=year).exists()

    if has_taken_test:
        # If the User has already taken the test in their current StudentProfile year, provide options
        if request.method == 'POST':
            option = request.POST.get('option', '')

            if option == 'delete':
                # Delete the existing test
                QuestionSet.objects.filter(user=request.user, year=year).delete()
                return HttpResponse("Your existing test has been deleted. You can now start a new test.")

            elif option == 'overwrite':
                # Overwrite the existing test (you can modify this part as needed)
                existing_test = QuestionSet.objects.get(user=request.user, year=year)
                existing_test.n_questions = 12  # Update the number of questions or any other relevant changes
                existing_test.is_completed = False
                existing_test.score = 0
                existing_test.save()
                return HttpResponse("Your existing test has been overwritten. You can now start a new test.")

        return render(request, 'options.html')  # Render a template with options (delete or overwrite)
    else:
        # Create a new test if the User hasn't taken the test in their current StudentProfile year
        new_set = Test.objects.create_set()  # You should implement the method to create a new set
        QuestionSet.objects.create(set_id=new_set, user=request.user, year=year, n_questions=12, is_completed=False, score=0)
        return HttpResponse("A new test has been created for you.")