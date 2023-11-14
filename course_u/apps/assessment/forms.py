from django import forms
from apps.assessment.models import UserResponse, Test

class UserResponseForm(forms.ModelForm):
    selected_option = forms.IntegerField()
    class Meta:
        model = UserResponse
        fields = ['selected_option'] 

class TestCreateForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = '__all__'


class TestUpdateForm(forms.ModelForm):
    topic = forms.CharField(max_length=100)
    question = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    options = forms.JSONField()
    correct_option = forms.IntegerField()

    class Meta:
        model = Test
        fields = ['topic', 'question', 'description', 'options', 'correct_option']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        widgets = {
            'options': forms.JSONField()
        }