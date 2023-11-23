from django.shortcuts import render, redirect
from .forms import Survey

def survey(request):
    if request.method == 'POST':
        form = Survey(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = Survey()

    return render(request, 'recommendersurvey/survey.html', {'form': form})

def thank_you(request):
    return render(request, 'recommendersurvey/thank_you.html')