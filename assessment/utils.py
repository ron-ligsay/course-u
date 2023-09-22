
from assessment.models import Test
from django.contrib.sessions.models import Session


def logger(message):
    print(message)
    return

def get_test_questions(x=None, y=None, topic=None):
    start = None
    end = None
    if x is not None:
        if y is not None:
            queryset = Test.objects.filter(question_id__gte=x, question_id__lte=y)
        else:
            start = 1
            end = x
            queryset = Test.objects.filter(question_id__gte=start, question_id__lte=end)
    else:
        queryset = Test.objects.all()

    if topic is not None:
        queryset = queryset.filter(topic=topic)
    
    return queryset, start, end

def create_question_set(request):
    # get last question_set_id
    #last_question_set_id = QuestionSet.objects.last().set_id
    question_set = request.session.get['question_set']
    last_question_set_id = question_set.objects.last().set_id
    # create new question_set_id
    if last_question_set_id is None:
        new_question_set_id = 1
    else:
        new_question_set_id = last_question_set_id + 1
    return new_question_set_id

def get_test_question_by_id(question_id):
    return Test.objects.get(question_id=question_id)