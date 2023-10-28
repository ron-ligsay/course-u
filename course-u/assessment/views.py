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

# App imports
from assessment.utils import get_test_questions, get_test_question_by_id, create_question_set
from assessment.forms import UserResponseForm, TestCreateForm, TestUpdateForm, MBTIResponseForm
from assessment.models import Test, QuestionSet, UserResponse, MBTI, MBTISet, MBTIResponse

# Other Imports
import plotly.express as px

# Create your views here:



def test_home(request):
    return render(request, 'test/test_home.html')

def start_test(request):
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

    # Retrieve the last question set
    last_set = QuestionSet.objects.last()
    print("last_set: ", last_set)
    if last_set == 0 or last_set is None:
         set_id = 1
    else:
        # check if questionset is completed
        if last_set.is_completed:
            messages.success(request, 'You started a new Test!')
            print("Completed Test!")
            set_id = last_set.set_id + 1

            print("SET ID: ", set_id)
   
            question_ids = []
            question_ids = request.session.get('question_set', [])
            print("123 question_ids: ", question_ids)
            question_ids = []
        
            request.session['test_started'] = True
            # Store the question set ID in the session
            request.session['question_set_id'] = set_id

            # Retrieve the questions for the question set
            question_set, start, end = get_test_questions(x=5)  # Modify this function to filter questions based on the set
            question_ids = question_set.values_list('question_id', flat=True)

            # Store the question IDs in the session
            request.session['question_set'] = list(question_ids)
            #request.session['question_set'] = question_set
            request.session['questions_answered'] = 0
            #request.session['n_questions'] = len(question_ids)
            n_questions = len(question_ids)
            print("n_questions: ", n_questions, ", compare to start - end: ", end - start + 1)
            print("question_ids: ", question_ids)
            request.session['n_questions'] = end - start + 1

            # Create QuestionSet on database
            QuestionSet.objects.create(set_id=set_id, user=request.user, n_questions=n_questions, is_completed=False, score=0)
        else :
            messages.success(request, 'You have an incomplete Test!')
            print("Incomplete Test!")
            set_id = last_set.set_id
            
            # get number of unfinished response on UserResponse
            unfinished_response = UserResponse.objects.filter(set_id=set_id, is_answered=False).count()
            print("unfinished_response: ", unfinished_response) 

            request.session['test_started'] = True
            # Store the question set ID in the session
            request.session['question_set_id'] = set_id

             # Retrieve the questions for the question set
            question_set, start, end = get_test_questions(x=5)  # Modify this function to filter questions based on the set
            question_ids = question_set.values_list('question_id', flat=True)

            # Store the question IDs in the session
            request.session['question_set'] = list(question_ids)
            #request.session['question_set'] = question_set
            request.session['questions_answered'] = 0
            #request.session['n_questions'] = len(question_ids)
            n_questions = len(question_ids)
            print("n_questions: ", n_questions, ", compare to start - end: ", end - start + 1)
            print("question_ids: ", question_ids)
            request.session['n_questions'] = end - start + 1

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
        # Check if the user has answered this question
        has_answered = user_responses.filter(is_answered=1).exists()
        question = Test.objects.get(pk=question)
        # Create a dictionary with question and answered status
        question_info.append({'question': question, 'has_answered': has_answered, 'n_question': n_question})

    return render(request, 'test/test_overview.html', {'question_set_id': question_set_id, 'question_info': question_info})

def next_test(request, question_id):
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
                # Redirect to the next question or a completion page
                next_question_id = question_id + 1
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
            return redirect('test_results')
        else:
            messages.success(request, 'You have not started the test')
            print('You have not started the test')
            return redirect('home')
    else:
        messages.success(request, 'You have not answered all questions')
        print("unfinished_response: ", unfinished_response, "YOU ARE NOT YET FINISHED!")
        # back to test_overview
        return redirect('test_overview')


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


def student_test_report(request):

    # get user results from QuestionSet
    user_id = request.user.id
    user_results = QuestionSet.objects.filter(user_id=user_id)

    # get user name
    username = User.objects.get(id=user_id)

    # for each user_result get set_id
    my_id = []
    for result in user_results:
        my_id.append(result.set_id)
    
    # for each my_id get all responses
    # user_responses = []
    # for id in my_id:
    #     user_responses.append(UserResponse.objects.filter(set_id=id))
    
    # get all user responses for the user
    user_responses = UserResponse.objects.filter(Q(set_id__in=my_id))

    # in Test, count number of correct answer per Test.topic and store in a dictionary
    topics = Test.objects.values('topic')
    topics = [topic['topic'] for topic in topics]
    correct_answers = []
    for topic in topics:
        correct_answers.append(UserResponse.objects.filter(is_correct=True).count())
    
    # create a dictionary of topics and correct answers
    topic_correct_answers = dict(zip(topics, correct_answers))

    # create a ploty pie chart
    fig = px.pie(values=correct_answers, names=topics, title='Correct Answers per Topic')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    # convert fig to html
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    # get top 3 topics
    top_topics = sorted(topic_correct_answers.items(), key=lambda x: x[1], reverse=True)[:3]

    # how to access the topic name 
    

    return render(request, 'test/test_result.html', {
        'username' : username,
        #'user_results' : user_results, 'user_responses' : user_responses, 'topic_correct_answers' : topic_correct_answers, 
        'top_topics' : top_topics, 
        'graph' : graph
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