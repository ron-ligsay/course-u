
from assessment.models import Test
from django.contrib.sessions.models import Session
from django.db.models import Count


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
            
            ## group questions by topic and count the number of questions for each topic
            field_counts = Test.objects.values('field_id').annotate(count=Count('question_id'))
            print("field_counts: ", field_counts)
            # select 5 questions for each topic
            queryset = Test.objects.none()
            for field_count in field_counts:
                field_queryset = Test.objects.filter(field_id=field_count['field_id'])[:x]
                queryset = queryset.union(field_queryset)
                print("Getting questions for field: ", field_count['field_id'])
            

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