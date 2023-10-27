from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from assessment.models import UserResponse, Test, MBTIResponse
# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Choice
#         fields = ['question_id', 'question']
#         widgets = {
#             'question': forms.RadioSelect,  # Use radio buttons for multiple-choice questions
#         }


# class UserResponseForm(forms.ModelForm):
#     class Meta:
#         model = UserResponse
#         fields = ['selected_option']

class UserResponseForm(forms.ModelForm):
    selected_option = forms.IntegerField()
    class Meta:
        model = UserResponse
        fields = ['selected_option']  # Include only the selected_option field

class TestCreateForm(forms.ModelForm):
    # topic = forms.CharField(max_length=100)
    # question = forms.CharField(max_length=100)
    # description = forms.CharField(max_length=100)
    # options = forms.JSONField()
    # correct_option = forms.IntegerField()

    class Meta:
        model = Test
        #fields = ['topic', 'question', 'description', 'options', 'correct_option']
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

class MBTIResponseForm(forms.ModelForm):
    selected_option = forms.CharField(max_length=1)
    class Meta:
        model = MBTIResponse
        fields = ['selected_option']  # Include only the selected_option field