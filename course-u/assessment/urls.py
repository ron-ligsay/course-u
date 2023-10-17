from django.urls import path, include
import debug_toolbar
from . import views
from django.contrib.auth.views import LogoutView
from datetime import datetime
from django.utils import timezone

urlpatterns = [
    # For quaries testing
    path("test_query/", views.test_query, name="test_query"),
    #path('test/<int:pk>/', views.test, name='test'),
    path('start_test/', views.start_test, name='start_test'),
    path('next_test/<int:question_id>/', views.next_test, name='next_test'),
    path('prev_test/<int:question_id>/', views.prev_test, name='prev_test'),
    #path('test_page/<int:test_id>/', views.test_page, name='test_page'),
    path('question/<int:question_id>/', views.display_question, name='display_question'),
    path('submit_question/<int:question_id>/', views.submit_question, name='submit_question'),
    path('test_home/', views.test_home, name='test_home'),
    path('view_test_results/', views.view_test_results, name='view_test_results'),
    path('test_overview/', views.test_overview, name='test_overview'),
    path('submit_test/', views.submit_test, name='submit_test'),
    path('create_test/', views.create_test, name='create_test'),
    path('update_test/<int:question_id>/', views.update_test, name='update_test'),
    #path('admin_report/', views.admin_test_report, name=('admin_report')),
    path('gradelevel_input/',views.gradelevel_input, name='gradelevel_input'),
    path('subjectgrade_input/',views.subjectgrade_input, name='subjectgrade_input')
]


