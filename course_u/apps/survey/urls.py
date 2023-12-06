from django.urls import path
from apps.survey.views import survey, thank_you

urlpatterns = [
    path('survey/', survey, name='survey'),
    path('thank_you/', thank_you, name='thank_you'),

]
