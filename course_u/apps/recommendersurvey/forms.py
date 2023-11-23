from django import forms
from .models import Survey

class Survey(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'