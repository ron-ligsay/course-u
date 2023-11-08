
def create_new_question_set(request, last_set):
    print("create_new_question_set() last_set: ", last_set)
    
    start = None

    if not last_set or last_set == 0:
        new_set = 1
    else:
        new_set = last_set.set_id + 1

    # Verify first if the User has already taken the test in his current StudentProfile year
    # Get year of User's StudentProfile
    if request.user.is_authenticated:
        try:
            year = StudentProfile.objects.get(user_id=request.user.id).current_year
        except ObjectDoesNotExist:
            year = None  # or some default value
    else:
        year = None  # or some default value
    # Check if the User has already taken the test in his current StudentProfile year
    has_taken_test = QuestionSet.objects.filter(user=request.user, year=year).exists()
    
    overwritten = False
    no_record = False
    completed_year = False

    
    if has_taken_test:
        # If the User has already taken the test in his current StudentProfile year, return an error
        # return HttpResponse("You have already taken the test in your current StudentProfile year.")
        overwritten, no_record, completed_year = check_school_year(request)
        print("has_taken_test: ", has_taken_test, "overwritten: ", overwritten, "no_record: ", no_record, "completed_year: ", completed_year)
    else: # No test in current year
        # QuestionSet.objects.create(set_id=new_set, user=request.user, n_questions=12, is_completed=False, score=0)
        print("No overwritten, no_record, and completed_year")
        no_record = True
        year = StudentProfile.objects.get(user_id=request.user.id).current_year
        

    if completed_year:
        # go to select_year
        course_id = StudentProfile.objects.get(user_id=request.user.id).enrolled_courses_id
        return redirect('select_year', course_id=course_id)
    if no_record:
        print("if no_record, Set: ", new_set, "created for user: ", request.user)
        request.session['question_set_id'] = new_set
        
        if overwritten:
            question_ids, question_set, start, end = recreate_overwritten_test(request, new_set)
        else:
            question_set, start, end = get_test_questions(x=2)
            question_ids = question_ids_and_session_test(request,question_set)      

        if not overwritten:
            # Create QuestionSet object
            QuestionSet.objects.create(
                set_id=new_set,
                user=request.user,
                n_questions=len(question_ids),
                is_completed=False,
                score=0,
                year=year,
            )

            for question in question_set:
                UserResponse.objects.create(
                    question=question,
                    set_id=new_set,
                    is_answered=False,
                )
                print("Created new UserResponse objects")
        start = question_ids[0]
        return start
    elif overwritten:
        print("elif overwritten:")
        question_ids, question_set, start, end = recreate_overwritten_test(request, new_set)
        return start
    
    return start


def check_school_year(request):
    print("check_school_year()")
    #completed_year = False
    #overwritten = False
    #no_record = False
    if request.method == 'POST':
        completed_year = request.POST.get('completed_year', '')

        if completed_year == 'yes':
            # User has completed the school year, redirect to the 'create_or_overwrite_test' view
            return redirect('create_or_overwrite_test')
            #overwritten, no_record = create_or_overwrite_test(request)
            #completed_year = True
            #return overwritten, no_record, completed_year

        elif completed_year == 'no':
            # User hasn't completed the school year, display a message
            return HttpResponse("Sorry, you need to finish the school year to retake the test.")
            #completed_year = False
            #return overwritten, no_record, completed_year
    # else:
    #     print("Please select an option to proceed.")
    #     return render(request, 'test/check_school_year.html')
    # return render(request, 'check_school_year.html')
    #print("Dont know what happen")
    #return overwritten, no_record, completed_year
    return render(request, 'check_school_year.html') 



#@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='login')  # Requires admin or superuser
def create_or_overwrite_test(request):
    print("create_or_overwrite_test()")
    overwritten = False
    no_record = False

    year = request.user.studentprofile.current_year

    # Check if the User has already taken the test in their current StudentProfile year
    question_set = QuestionSet.objects.filter(user=request.user, year=year)
    # or has_taken_test

    if question_set: # If the User has already taken the test in their current StudentProfile year
        # If the User has already taken the test in their current StudentProfile year, provide options
        if request.method == 'POST':
            option = request.POST.get('option', '')

            if option == 'delete':
                # Delete the existing test
                QuestionSet.objects.filter(user=request.user, year=year).delete()
                return HttpResponse("Your existing test has been deleted. You can now start a new test.")
                #messages.success(request, 'Your existing test has been deleted. You can now start a new test.')
                #return redirect('test_home')

            elif option == 'overwrite':
                # Overwrite the existing test (you can modify this part as needed)
                existing_test = QuestionSet.objects.get(user=request.user, year=year)
                existing_test.n_questions = 12  # Update the number of questions or any other relevant changes
                existing_test.is_completed = False
                existing_test.score = 0
                existing_test.save()

                # remove selected options from UserResponse
                user_responses = UserResponse.objects.filter(set_id=existing_test.set_id)
                for user_response in user_responses:
                    user_response.selected_option = None
                    user_response.is_correct = None
                    user_response.is_answered = False
                    user_response.save()
                

                print("Your existing test has been overwritten. You can now start a new test.")
                # go to test_overview
                #return redirect('test_overview', existing_test)
                #overwritten = True
                #return overwritten, no_record
            # else:
            #     # If the user didn't choose an option, show a message
            #     # return HttpResponse("Please select an option to proceed.")
            #     return redirect('create_or_overwrite_test')
            
        return render(request, 'test/create_or_overwrite_test.html')  # Render a template with options (delete or overwrite)
        #print("Please select an option to proceed.")
        #return redirect('create_or_overwrite_test')
    else: # no test in current year
        # Create a new test if the User hasn't taken the test in their current StudentProfile year
        new_set = Test.objects.create_set()  # You should implement the method to create a new set
        QuestionSet.objects.create(set_id=new_set, user=request.user, year=year, n_questions=12, is_completed=False, score=0) 
        return HttpResponse("A new test has been created for you.")
        #no_record = True
        #return overwritten, no_record
