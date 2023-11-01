# from website.models import Specialization, Test, JobPosting, QuestionSet, UserResponse
# from .utils import *

# def context_question_sets(request):
#     question_set_id = create_question_set()
#     question_sets = get_test_questions(x=1,y=5)
#     return {'question_set_id': question_set_id, 'question_sets': question_sets}


# Context Processors
# used to pass variables to all templates
# example of a context processor
# def context_specializations(request):
#     specializations = Specialization.objects.all()
#     return {'specializations': specializations}
#
# def context_test(request):
#     test = Test.objects.all()
#     return {'test': test}
#

# Create utility functions for common operations that are repeated in your views. 
# Here are some utility functions that you can create:

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from assessment.models import Test 

# Utility function to get the next question
def get_next_question(request, question_id):
    try:
        n_question = request.session.get('n_questions', 0)
        if question_id + 1 < n_question:
            next_question = get_object_or_404(Test, question_id=question_id + 1)
            options = next_question.options
            return render(request, 'test/test_page.html', {'question': next_question, 'options': options})
        elif question_id + 1 == n_question:
            messages.success(request, 'You have completed the test')
            return redirect('test_overview')
    except Test.DoesNotExist:
        messages.success(request, 'You have completed the test')
        return redirect('test_overview')
    return None  # No more questions

# Utility function to get the previous question
def get_previous_question(request, question_id):
    # Implementation of the get_previous_question function
    pass

# Utility function to submit a question
def submit_user_response(request, question_id):
    # Implementation of the submit_user_response function
    pass

# Utility function to check if the test is completed
def is_test_completed(request):
    # Implementation of the is_test_completed function
    pass

# Utility function to start a new test
def start_new_test(request):
    # Implementation of the start_new_test function
    pass

# Utility function to retrieve user responses for a question set
def get_user_responses(request):
    # Implementation of the get_user_responses function
    pass

# Utility function to handle test submission
def handle_test_submission(request):
    # Implementation of the handle_test_submission function
    pass
