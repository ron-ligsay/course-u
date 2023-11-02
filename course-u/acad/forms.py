from django import forms

from acad.models import StudentProfile, Course, Subject, Curriculum, StudentGrades

# Not used
class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['enrolled_courses', 'current_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrolled_courses'].queryset = Course.objects.all()



class StudentGradeForm(forms.ModelForm):
    class Meta:
        model = StudentGrades
        fields = ['grade']