# Sesssions
# Used for storing session data

# clear_session_variables, get_last_question_set, create_or_retrieve_question_set, display_question_set, submit_test

def clear_session_variables(request):
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

    return None
    