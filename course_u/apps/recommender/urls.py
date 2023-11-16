from django.urls import path
from . import views

urlpatterns = [
    path('recommender/', views.recommender, name='recommender'),
    path('recommendation/<int:field_id>/', views.recommendation_field, name='recommendation_field'),
]