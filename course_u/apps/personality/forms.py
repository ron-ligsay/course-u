from django import forms
from apps.personality.models import  MBTIResponse

class MBTIResponseForm(forms.ModelForm):
    selected_option = forms.CharField(max_length=1)
    class Meta:
        model = MBTIResponse
        fields = ['selected_option']  # Include only the selected_option field

