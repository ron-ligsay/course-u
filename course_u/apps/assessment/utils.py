from django.contrib.sessions.models import Session
from django.db.models import Count

from apps.assessment.models import Test, QuestionSet, UserResponse

from django.contrib.auth.models import User

# random
import random


def logger(message):
    print(message)
    return

def get_test_questions(x=None, topic=None, set_id=None):
    print('get_test_questions()')
    """
    Returns a List of Test Question IDs
    Parameters:
    x: int
        number of questions per field
    topic: str
        topic of questions
    set_id: int
        id of question set
    """
    start = None
    end = None
    answered_questions_id = []

    if set_id is not None:
        # Get user_id from set_id
        try:
            user_id = QuestionSet.objects.get(set_id=set_id).user_id
        except:
            print('set_id does not exist')
            return None, None, None
        # get existing question sets
        question_sets = QuestionSet.objects.filter(user_id=user_id)
        # get user response questions from question set and store in the answered_questions list
        for question_set in question_sets:
            user_responses = UserResponse.objects.filter(set_id=question_set.set_id)
            for user_response in user_responses:
                answered_questions_id.append(user_response.question_id)
        print("answered_questions_id: ", answered_questions_id)

    if x is not None:
        #start = 1
        #end = x
        
        ## group questions by topic and count the number of questions for each topic
        #field_counts = Test.objects.values('field_id').annotate(count=Count('question_id'))
        #print("field_counts: ", field_counts)
        # select 5 questions for each topic
        
        if topic is not None:
            # field equal to topic
            fields = Test.objects.filter(field_id=topic).values('field_id').distinct()
        else:
            # get all unique fields
            fields = Test.objects.values('field_id').distinct()
        print('fields: ', fields)
        
        queryset = Test.objects.none()
        # for field_count in field_counts:
        #     field_queryset = Test.objects.filter(field_id=field_count['field_id'])[:x]
        #     queryset = queryset.union(field_queryset)
        #     print("Getting questions for field: ", field_count['field_id'])
        
        for field in fields:
            # get list of id of questions in field
            field_questions = Test.objects.filter(field_id=field['field_id']).values('question_id')
            print('field_questions: ', field_questions)
            # get x number of questions for each field
            for i in range(x):
                # get random numbner from field_questions list
                random_question = random.choice(field_questions)
                # not in answered_questions_id
                while random_question['question_id'] in answered_questions_id:
                    random_question = random.choice(field_questions)
                # add question to answered_questions_id
                answered_questions_id.append(random_question['question_id'])
                print('answered_questions_id: ', answered_questions_id)
                # add to queryset
                queryset = queryset.union(Test.objects.filter(question_id=random_question['question_id']))
                print("Getting questions for field: ", field['field_id'])
        # get lowest question_id from queryset
        start = queryset.order_by('question_id').first().question_id
        # get total number of questions
        end = queryset.count()
         
                

    else:
        queryset = Test.objects.all()

    # if topic is not None:
    #     queryset = queryset.filter(topic=topic)
    
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