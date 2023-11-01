# System imports
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.db.models import Q, Avg
from django.db.models import Sum, Case, When, IntegerField, F, Count

# App imports
from assessment.utils import get_test_questions, get_test_question_by_id, create_question_set
from assessment.forms import UserResponseForm, TestCreateForm, TestUpdateForm, MBTIResponseForm
from assessment.models import Test, QuestionSet, UserResponse, MBTI, MBTISet, MBTIResponse

from website.models import Field, Specialization, UserRecommendations, Skill

# Other Imports
import plotly.express as px
from plotly.offline import plot

# Create your views here:



def test_home(request):
    return render(request, 'test/test_home.html')

def start_test(request):

    question_per_field = 2

    # delete session vairables
    if 'test_started' in request.session:
        del request.session['test_started']
    if 'question_set_id' in request.session:
        del request.session['question_set_id']
    if 'question_set' in request.session:
        del request.session['question_set']
    if 'questions_answered' in request.session:
        del request.session['questions_answered']
    if 'n_questions' in request.session:
        del request.session['n_questions']


    # Check user's QuestionSet if it has incomplete test
    try:
        incomplete = QuestionSet.objects.filter(user=request.user, is_completed=False).first()
        print("incomplete: ", incomplete)
        last_set = 0
    except QuestionSet.DoesNotExist:
        incomplete = None
        # If none, get the last question set
        last_set = QuestionSet.objects.last()
        print("last_set: ", last_set)

    # If yes, retrieve the last question set
    if incomplete:
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
        request.session['n_questions'] = n_questions

        # Check if UserResponse with set_id are equal to n_questions
        if n_questions == incomplete.n_questions:
            # If yes, redirect to test_overview
            print("You have complete Responses n_questions: ", n_questions, "incomplete.n_questions: ", incomplete.n_questions, "equal!")
            return redirect('test_overview')
        else:
            print("You have incomplete Responses n_questions: ", n_questions, "incomplete.n_questions: ", incomplete.n_questions, "not equal!")
            # count number of unfinished response on UserResponse per test Field
            # get unique fields
            unique_fields = question_set.objects.values('field').distinct()

            print("fields: ", unique_fields)


            for field in fields:
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
        
        # store questions_answered in session
        request.session['questions_answered'] = 0

        # Start test
        request.session['test_started'] = True



    return redirect('display_question', question_id=start)



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
    return render(request, 'test/test_page.html', {'question': question, 'question_set_id': question_set_id})#, 'questions_answered': questions_answered

def test_overview(request):
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

def next_test(request, question_id):
    print("next_test() question_id: ", question_id)
    if not request.user.is_authenticated:
        return redirect('home')

    try:
        mbti_question_set = request.session.get('mbti_question_set')
        mbti_n_question = request.session.get('mbti_n_questions', 0)
        question = get_object_or_404(Test, question_id=question_id + 1)
        #if question not in question_set:
        #    raise Test.DoesNotExist

        if question_id + 1 < mbti_n_question:
            #options = question.options
            return render(request, 'test/test_page.html', {'question': question})
        if question_id + 1 == mbti_n_question:
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
        return render(request, 'test/test_page.html', {'question': question})#, 'options': options
    else:
        # Handle the case where the previous question is out of bounds
        messages.success(request, 'You have reached the first question')
        return redirect('home')

def submit_question(request, question_id):
    print("submit_question() question_id: ", question_id)
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
                existing_response = UserResponse.objects.filter(question=question.question_id,set_id=set_id).first()

                if existing_response:
                    # If an existing response is found, update it
                    existing_response.selected_option = selected_option
                    existing_response.is_correct = is_correct
                    existing_response.is_answered = True
                    existing_response.save()
                    messages.success(request, 'Your answer has been updated')
                else:
                    # Otherwise, create a new UserResponse object
                    UserResponse.objects.create(
                        #user=request.user,
                        #response=None,
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
                    current_index = question_ids.index(current_question_id)
                except ValueError:
                    # Handle the case where the current_question_id is not found in the list
                    current_index = -1
                if current_index >= 0 and current_index < len(question_ids) - 1:
                    # If the current question ID is found and it's not the last question in the list
                    next_question_id = question_ids[current_index + 1]
                    # You can use the next_question_id here for further processing
                else:
                    # Handle the case where there is no next question
                    n_question = request.session.get('n_questions', 0)
                    next_question_id = n_question
                    pass  # You may display a message or perform some other action

                try:
                    n_question = request.session.get('n_questions', 0)
                    if next_question_id == n_question:
                        # This is the last question
                        messages.success(request, 'You have completed the test')
                        return redirect('test_overview')
                    else:
                        next_question = Test.objects.get(pk=next_question_id)
                        options = next_question.options
                        return render(request, 'test/test_page.html', {'question': next_question, 'options': options, 'form': UserResponseForm()})
                except Test.DoesNotExist:
                    # Handle the case where there is no next question
                    messages.success(request, 'You have completed the test')
                    return redirect('home')
            else:
                # Display the question and form again with validation errors
                options = question.options
                return render(request, 'tes/test_page.html', {'question': question, 'options': options, 'form': form})
        else:
            # Display the question and form for the first time
            options = question.options
            return render(request, 'test/test_page.html', {'question': question, 'options': options, 'form': UserResponseForm()})
    else:
        return redirect('home')

def submit_test(request):
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

            # delete session vairables
            del request.session['test_started']
            del request.session['question_set_id']
            del request.session['question_set']
            del request.session['questions_answered']

            messages.success(request, 'You have completed the test')
            print('You have completed the test')
            return redirect('test_results', question_set_id=question_set_id)
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
    fig = px.pie(
        values=list(field_correct_answers.values_list("total_correct", flat=True)),
        names=list(field_correct_answers.values_list("field_name", flat=True)),
        title='Correct Answers per Field'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

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

def student_test_report_overall(request):

    # Get user results from all QuestionSets
    user_id = request.user.id
    user_results = QuestionSet.objects.filter(user_id=user_id)

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
    fig = px.pie(
        values=list(field_correct_answers.values_list("total_correct", flat=True)),
        names=list(field_correct_answers.values_list("field_name", flat=True)),
        title='Correct Answers per Field'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

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

def test_query(request):
    questions,start,end = get_test_questions(x=1, y=5)
    return render(request, 'test_queries/test_query.html', {'questions': questions})

def gradelevel_input(request):
    return render(request, 'user/grade level.html')

def subjectgrade_input(request):
    return render(request, 'user/subject.html')

def course_input(request):
    return render(request,'user/course.html')




################################
#       MBTI TEST VIEWS        #
################################


from django.db.models import Max

def initialize_mbti_test(request):
    user = request.user

    # Check if there is an unfinished MBTISet for the user
    unfinished_set = MBTISet.objects.filter(user=user, is_completed=False).first()

    if unfinished_set:
        # If there is an unfinished set, continue that test
        mbti_set = unfinished_set
    else:
        # If no unfinished set exists, create a new one with a set_id one greater than the maximum set_id
        last_set = MBTISet.objects.aggregate(Max('mbti_set_id'))
        new_set_id = last_set['mbti_set_id__max'] + 1 if last_set['mbti_set_id__max'] else 1
        mbti_set = MBTISet.objects.create(user=user, mbti_set_id=new_set_id)

    # Create responses for all MBTI questions
    mbti_questions = MBTI.objects.all()
    for question in mbti_questions:
        MBTIResponse.objects.get_or_create(mbti_set=mbti_set, mbti=question)

    return redirect('mbti_test', mbti_set_id=mbti_set.pk)

def mbti_test(request, mbti_set_id):
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)
    responses = MBTIResponse.objects.filter(mbti_set=mbti_set, is_answered=False)
    
    if request.method == 'POST':
        # Process user responses
        for response in responses:
            option = request.POST.get(f'question_{response.mbti_id}')
            if option:
                response.selected_option = int(option)
                response.is_answered = True
                response.save()
        
        # set id
        print("def mbti_test() mbti_set.id: ", mbti_set.mbti_set_id)
        # All questions answered, calculate personality
        calculate_personality(request.user, mbti_set.mbti_set_id)
        return redirect('mbti_results', mbti_set_id=mbti_set_id)

    return render(request, 'test/mbti_test.html', {'mbti_set': mbti_set, 'responses': responses})


def calculate_personality(user, mbti_set_id):
    #  # Try to get the user's existing MBTISet instance
    # mbti_set = MBTISet.objects.filter(user=user).first()
     # Get the MBTI set using the provided mbti_set_id
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)
    if not mbti_set:
        # If it doesn't exist, create a new one
        mbti_set = MBTISet.objects.create(user=user, mind=0, energy=0, nature=0, tactics=0)

    print("def calculate_personality() mbti_set: ", mbti_set)
    print("def calculate_personality() mbti_set_id: ", mbti_set.pk)
    # number of objects
    print("MBTI.objects.count(): ", MBTI.objects.count())
    # Calculate mind, energy, nature, and tactics here
    # filter by id, from 1 to 5
    mbti_mind = MBTI.objects.filter(mbti__range=(1, 5))
    mbti_energy = MBTI.objects.filter(mbti__range=(6, 10))
    mbti_nature = MBTI.objects.filter(mbti__range=(11, 15))
    mbti_tactics = MBTI.objects.filter(mbti__range=(16, 20))
    print("mbti_mind: ", mbti_mind, "mbti_energy: ", mbti_energy, "mbti_nature: ", mbti_nature, "mbti_tactics: ", mbti_tactics)

    mind = MBTIResponse.objects.filter(mbti__in=mbti_mind, mbti_set=mbti_set)
    energy = MBTIResponse.objects.filter(mbti__in=mbti_energy, mbti_set=mbti_set)
    nature = MBTIResponse.objects.filter(mbti__in=mbti_nature, mbti_set=mbti_set)
    tactics = MBTIResponse.objects.filter(mbti__in=mbti_tactics, mbti_set=mbti_set)
    print("mind: ", mind, "energy: ", energy, "nature: ", nature, "tactics: ", tactics)

    # get average of selected_option
    mind = mind.aggregate(average_rating=Avg('selected_option'))['average_rating']
    energy = energy.aggregate(average_rating=Avg('selected_option'))['average_rating']
    nature = nature.aggregate(average_rating=Avg('selected_option'))['average_rating']
    tactics = tactics.aggregate(average_rating=Avg('selected_option'))['average_rating']
    print("mind: ", mind, "energy: ", energy, "nature: ", nature, "tactics: ", tactics)
    
    # Update the user's MBTI set instance with the calculated values
    mbti_set.mind = mind
    mbti_set.energy = energy
    mbti_set.nature = nature
    mbti_set.tactics = tactics
    mbti_set.save()

    # Determine the personality type and update the user's MBTI instance
    personality_type = ''
    if mind >= 2.5:
        personality_type += 'I'
    else:
        personality_type += 'E'
    if energy >= 2.5:
        personality_type += 'N'
    else:
        personality_type += 'S'
    if nature >= 2.5:
        personality_type += 'F'
    else:
        personality_type += 'T'
    if tactics >= 2.5:
        personality_type += 'P'
    else:
        personality_type += 'J'
    print("Personality Type: ", personality_type)
    mbti_set.identity = personality_type

    # marks as completed
    mbti_set.is_completed = True
    mbti_set.save()


def mbti_results(request, mbti_set_id):
    mbti_set = MBTISet.objects.get(pk=mbti_set_id)

    # Convert float into percentage
    mbti_set.mind = int(mbti_set.mind * 20)
    mbti_set.energy = int(mbti_set.energy * 20)
    mbti_set.nature = int(mbti_set.nature * 20)
    mbti_set.tactics = int(mbti_set.tactics * 20)

    

    return render(request, 'test/mbti_results.html', {'mbti_set': mbti_set})


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