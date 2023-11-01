from django.urls import path
from acad.views import *
from . import views

urlpatterns = [
    path('select_course/', views.select_course, name='select_course'),
    path('select_year/<int:course_id>/', views.select_year, name='select_year'),
    path('enroll_student/<int:course_id>/<int:year_level>/', views.enroll_student, name='enroll_student'),
    path('subjects/', views.subjects, name='subjects'),
]

