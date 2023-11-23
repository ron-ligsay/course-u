from django.shortcuts import render, redirect
from .forms import SurveyForm

def survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = SurveyForm()

    return render(request, 'survey/survey.html', {'form': form})

def thank_you(request):
    return render(request, 'survey/thank_you.html')