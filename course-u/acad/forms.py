from django import forms
from .models import UserProfile, Course

class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['enrolled_courses', 'current_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrolled_courses'].queryset = Course.objects.all()
