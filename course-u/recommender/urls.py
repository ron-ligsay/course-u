from django.urls import path
from . import views

urlpatterns = [
    path('recommender/', views.predictor, name='predictor'),
]