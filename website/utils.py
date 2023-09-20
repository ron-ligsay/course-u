
from website.models import Test
from django.contrib.sessions.models import Session

question_set_id = 0



def get_test_questions(x=None, y=None, topic=None):
    
    if x is not None:
        if y is not None:
            queryset = Test.objects.filter(question_id__gte=x, question_id__lte=y)
        else:
            queryset = Test.objects.filter(question_id__gte=0, question_id__lte=x)
    else:
        queryset = Test.objects.all()

    if topic:
        queryset = queryset.filter(topic=topic)
    return queryset

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

