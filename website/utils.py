
from website.models import Test

"""
    Retrieve data rows from the 'Test' table within the specified question ID range and topic (optional).

    Args:
        
        if x is only given then return all questions from 0 to x

        if with x and y then return all questions from x to y
        x (int): The starting question ID.
        y (int): The ending question ID.
        
        topic (str, optional): The topic to filter by.

    Returns:
        QuerySet: A QuerySet containing the filtered data rows.
    """
def get_test_questions():
    queryset = Test.objects.all()
    return queryset

def get_test_questions(x):
    queryset = Test.objects.filter(question_id__gete=0, question_id__lte=x)
    return queryset

def get_test_questions(x, y):
    queryset = Test.objects.filter(question_id__gete=x, question_id__lte=y)
    return queryset

def get_test_questions(x, y, topic=None):
    queryset = Test.objects.filter(question_id__gete=x, question_id__lte=y)
    if topic:
        queryset = queryset.filter(topic=topic)
    return queryset

