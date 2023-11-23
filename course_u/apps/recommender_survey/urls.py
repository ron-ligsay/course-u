from django.urls import path
from apps.recommender_survey.views import survey, thank_you

urlpatterns = [
    path('recommendersurvey/', survey, name='recommender_survey'),
    path('recommender_thank_you/', thank_you, name='thank_you'),

]
