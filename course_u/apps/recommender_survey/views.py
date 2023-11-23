from django.shortcuts import render, redirect
from .models import Survey
from .forms import SurveyForm
from apps.recommender.models import UserRecommendations


def survey(request):
    # Get the last UserRecommendation where user = request.user
    last_recommendation = UserRecommendations.objects.filter(user_id=request.user).last()
    
    # If there's no recommendation, don't ask survey
    if not last_recommendation:
        return redirect('recommender')  # or wherever you want to redirect

    # If there's a recommendation and no answered survey, go to survey
    survey = Survey.objects.filter(recommendation_id=last_recommendation.recommendation_id).first()
    if not survey:
        if request.method == 'POST':
            form = SurveyForm(request.POST)
            if form.is_valid():
                # Save userrecommendation_id to recommender survey
                survey = form.save(commit=False)
                survey.recommendation_id = last_recommendation.recommendation_id
                survey.save()
                return redirect('thank_you')
        else:
            form = SurveyForm()

        return render(request, 'recommendersurvey/survey.html', {'form': form})

    # If there's a recommendation and have answered survey, go to recommendedr
    else:
        return redirect('recommender')

def thank_you(request):
    return render(request, 'recommendersurvey/thank_you.html')