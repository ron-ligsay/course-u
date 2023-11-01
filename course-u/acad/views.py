from django.shortcuts import render, redirect
from acad.models import Course, Subject, Curriculum, StudentProfile

def select_course(request):
    courses = Course.objects.all()
    print("Courses: ", courses)
    return render(request, 'acad/select_course.html', {'courses': courses})

def select_year(request, course_id):
    course = Course.objects.get(pk=course_id)
    print("Selected course: ", course)
        
    # Get the number of years from the selected course
    number_of_years = course.number_of_years
    print("Number of years: ", number_of_years)

    return render(request, 'acad/select_year_level.html', {'course': course, 'number_of_years': number_of_years})

def enroll_student(request, course_id, year_level):
    course = Course.objects.get(pk=course_id)
    
    student, created = StudentProfile.objects.get_or_create(user=request.user)
    student.enrolled_courses_id = course.id
    student.current_year = year_level
    student.save()

    print("Student enrolled in course: ", student.enrolled_course)

    return render(request, 'acad/enrollment_success.html')

def subjects(request):
    
    user = request.user
    student = StudentProfile.objects.get(user=user)

    # Get the enrolled course of the student and year
    course = student.enrolled_courses_id
    year_level = student.current_year

    # Get the subjects for the course and year through curriculum
    curriculum = Curriculum.objects.filter(course_id=course, year=year_level)
    
    print("Curriculum: ", curriculum)

    # get subject_id from curriculum
    subject_id = []
    for subject in curriculum:
        subject_id.append(subject.subject_id)

    print("Subject ID: ", subject_id)

    # Get the subjects for the curriculum
    subjects = Subject.objects.filter(pk__in=subject_id)
    print("Subjects: ", subjects)

    return render(request, 'acad/subject.html', {'subjects': subjects})

def submit_grades(request):
    if request.method == 'POST':
        subject_id = request.POST['subject_id']
        student_id = request.POST['student_id']
        grade = request.POST['grade']

        student = StudentProfile.objects.get(pk=student_id)
        subject = Subject.objects.get(pk=subject_id)

        # Add the grade to the student's grades
        student.grades[subject.subject_name] = grade
        student.save()

        return redirect('subjects')
    else:
        return render(request, 'submit_grades.html')

