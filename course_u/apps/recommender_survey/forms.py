from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['ques1','ques2','ques3','ques4','ques5','ques6','ques7']