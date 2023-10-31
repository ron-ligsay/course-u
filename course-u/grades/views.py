from django.shortcuts import render, redirect
from .forms import GradeForm

def grade_input(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = GradeForm()
    return render(request, 'grades/grade_input.html', {'form': form})
