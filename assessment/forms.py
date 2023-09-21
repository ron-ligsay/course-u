from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from assessment.models import UserResponse

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