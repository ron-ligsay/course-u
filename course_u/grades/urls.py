from django.urls import path
from . import views

urlpatterns = [
    path('grade_input/', views.grade_input, name='grade_input'),
    # Add other URLs as needed
]