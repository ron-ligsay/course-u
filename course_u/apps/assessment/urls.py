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
    #path('next_test/<int:question_id>/', views.next_test, name='next_test'),
    path('next_test/<int:question_id>/<int:question_set_id>/', views.next_test, name='next_test'),
    #path('prev_test/<int:question_id>/', views.prev_test, name='prev_test'),
    path('prev_test/<int:question_id>/<int:question_set_id>/', views.prev_test, name='prev_test'),
    #path('test_page/<int:test_id>/', views.test_page, name='test_page'),
    path('question/<int:question_id>/', views.display_question, name='display_question'),
    
    path('process_incomplete_set/<int:incomplete>/', views.process_incomplete_set, name='process_incomplete_set'),
    path('handle_incomplete_set/<int:incomplete>/', views.handle_incomplete_set, name='handle_incomplete_set'),
    path('handle_incomplete_user_response/<int:incomplete>/', views.handle_incomplete_user_response, name='handle_incomplete_user_response'),
    path('resume_uncompleted_set/<int:incomplete>/', views.resume_uncompleted_set, name='resume_uncompleted_set'),
    path('recreate_overwritten_test/<int:new_set>/', views.recreate_overwritten_test, name='recreate_overwritten_test'),
    path('create_new_question_set/', views.create_new_question_set, name='create_new_question_set'),
    path('create_new_question_set/<int:last_set>/', views.create_new_question_set, name='create_new_question_set'),
    #path('create_new_question_set/<int:question_id>/', views.create_new_question_set, name='create_new_question_set'),
    path('check_school_year/', views.check_school_year, name='check_school_year'),
    
    path('check_school_year_choice/<str:choice>/', views.check_school_year_choice, name='check_school_year_choice'),
    path('check_school_year_status/<str:status>/', views.check_school_year_status, name='check_school_year_status'),
    
    path('create_or_overwrite_test/', views.create_or_overwrite_test, name='create_or_overwrite_test'),
    path('create_or_overwrite_test/<str:action>/', views.create_or_overwrite_test, name='create_or_overwrite_test'),
    path('continue_create_new_question_set/<int:last_set>', views.continue_create_new_question_set, name='continue_create_new_question_set'),

    path('submit_question/<int:question_id>/', views.submit_question, name='submit_question'),
    path('test_home/', views.test_home, name='test_home'),
    
    path('test_overview/<int:question_set_id>', views.test_overview, name='test_overview'),
    path('submit_test/', views.submit_test, name='submit_test'),
    

    path('test_reults/<int:question_set_id>',views.student_test_report,name='student_test_report'),
    path('test_results_overall/',views.student_test_report_overall,name='test_results_overall'),


    path('create_test/', views.create_test, name='create_test'),
    path('update_test/<int:question_id>/', views.update_test, name='update_test'),
    #path('admin_report/', views.admin_test_report, name=('admin_report')),


    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]


