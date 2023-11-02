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


# class StudentGradeForm(forms.ModelForm):
#     class Meta:
#         model = StudentGrades
#         fields = ['grade', 'subject']
#         widgets = {
#             'subject': forms.TextInput(attrs={'disabled': True}),
#         }
# class StudentGradeForm(forms.ModelForm):
#     subject_hidden = forms.CharField(widget=forms.HiddenInput())

#     class Meta:
#         model = StudentGrades
#         fields = ['grade']
#         # fields = ['grade', 'subject', 'subject_hidden']
#         # widgets = {
#         #     'subject': forms.TextInput(attrs={'disabled': True}),
#         # }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             self.fields['subject_hidden'].initial = self.instance.subject


# class StudentGradeForm(forms.ModelForm):
#     subject_hidden = forms.CharField(widget=forms.HiddenInput())

#     class Meta:
#         model = StudentGrades
#         fields = ['grade', 'subject_hidden']
#         widgets = {
#             'subject': forms.TextInput(attrs={'disabled': True}),
#         }

#     def __init__(self, *args, **kwargs):
#         subject = kwargs.pop('subject', None)
#         super().__init__(*args, **kwargs)
#         if subject:
#             self.fields['subject_hidden'].initial = subject.subject_name
#             print('Initial value of subject_hidden:', self.fields['subject_hidden'].initial)



class StudentGradeForm(forms.ModelForm):
    class Meta:
        model = StudentGrades
        fields = ['grade']