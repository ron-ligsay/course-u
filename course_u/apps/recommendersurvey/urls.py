from django.urls import path
from apps.recommendersurvey.views import survey, thank_you

urlpatterns = [
    path('recommendersurvey/', survey, name='survey'),
    path('recommender_thank_you/', thank_you, name='thank_you'),

]
