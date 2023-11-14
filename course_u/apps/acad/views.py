from django.shortcuts import render, redirect
from django.shortcuts import redirect


from apps.acad.models import Course, Subject, Curriculum, StudentProfile, StudentGrades
from apps.acad.forms import StudentGradeForm

from apps.website.models import Skill
from apps.recommender.models import UserSkill

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

    user_id = request.user.id

    # Get the enrolled course of the student and year
    course = student.enrolled_courses_id

    # Get the grades
    grades = StudentGrades.objects.filter(student=student)
    
    # loop through grades and get the score and skills
    for grade in grades:
        # get skils from subject
        subject = Subject.objects.get(pk=grade.subject_id)
        #grade.skills = subject.skills 
        
        # get grade score
        print('grade: ', grade.grade)
        # loop through skills
        for skill in subject.skills.all():
            skill_id = skill.id
            print('skill: ', skill)
            # get or create UserSkill
            # make sure to get only one
            user_skill, created = UserSkill.objects.get_or_create(user_id=user_id, skill_id=skill_id)

            # update score
            level = 0
            if created:
                print('created user skill: ', user_skill)
                user_skill.level = level
            else:
                print('existing user skill: ', user_skill)
                level = user_skill.level
            if grade.grade == 1.00 or grade.grade == 1:
                level += 5
            elif grade.grade == 1.25:
                level += 4
            elif grade.grade == 1.50:
                level += 3
            elif grade.grade == 1.75:
                level += 2
            elif grade.grade == 2.00 or grade.grade == 2:
                level += 1
            elif grade.grade >= 2.25 and grade.grade <= 3.00 or grade.grade >= 2.25 and grade.grade <= 3:
                level += 1
            else:
                level += 0
            user_skill.level = level
            user_skill.save()
            print("saved user skill: ", user_skill)
            # add skill source


    return render(request, 'acad/success_page.html', {
        'student': student,
        'course': course,
        'grades': grades,
    })
