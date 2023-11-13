from django.shortcuts import render, redirect
from django.shortcuts import redirect


from apps.acad.models import Course, Subject, Curriculum, StudentProfile, StudentGrades
from apps.acad.forms import StudentGradeForm


def select_course(request):
    courses = Course.objects.all()
    print("Courses: ", courses)
    # return warning if ther are no courses
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

    print("Student enrolled in course: ", student.enrolled_courses_id)

    return redirect('subjects_grade_input')


def subjects_grade_input(request):
    # Get the Student Profile
    student = StudentProfile.objects.get(user=request.user)

    # Get the enrolled course of the student and year level
    course = student.enrolled_courses_id
    course_name = Course.objects.get(pk=course)
    year_level = student.current_year
    print("year level:", year_level)

    # Get the curriculum for the course and year level
    curriculum = Curriculum.objects.filter(course_id=course, year=year_level)

    # Get subject_id from curriculum
    subject_id = []
    for subject in curriculum:
        subject_id.append(subject.subject_id)

    # Get the subjects for the curriculum
    subjects = Subject.objects.filter(pk__in=subject_id)


    print("Subjects: ", subjects)

    if request.method == 'POST':
        forms = [StudentGradeForm(request.POST, prefix=str(subject.id)) for subject in subjects]
        if all(form.is_valid() for form in forms):
            for form, subject in zip(forms, subjects):
                grade_value = form.cleaned_data.get('grade')
                if grade_value is not None:
                    grade, created = StudentGrades.objects.get_or_create(student=student, subject=subject)
                    grade.grade = grade_value
                    grade.save()
                else:
                    print(f"Grade value for subject {subject.id} is None or 0")
            return redirect('success_page')
        else:
            # Handle errors or form validation errors
            for form in forms:
                print(form.errors)
    else:
        forms = [StudentGradeForm(prefix=str(subject.id)) for subject in subjects]
    
    # return warning if there are no subjects available

    return render(request, 'acad/subject_grade_input.html', {'form_subject_pairs': zip(forms, subjects), 'course': course_name, 'year_level': year_level})
    
def success_page(request):
    # Get the Student Profile
    student = StudentProfile.objects.get(user=request.user)

    # Get the enrolled course of the student and year
    course = student.enrolled_courses_id

    # Get the grades
    grades = StudentGrades.objects.filter(student=student)
    
    # return warning if failed to save grades

    return render(request, 'acad/success_page.html', {
        'student': student,
        'course': course,
        'grades': grades,
    })
