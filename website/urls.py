"""
URL configuration for dcrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import debug_toolbar
from . import views
from django.contrib.auth.views import LogoutView
# import datetime and timezone
from datetime import datetime
from django.utils import timezone

urlpatterns = [
    path('', views.home, name='home'),
    path('__debug__/',include('debug_toolbar.urls')),
    # For quaries testing
    path("test_query/", views.test_query, name="test_query"),


    # For Authentication
    path('login_user/', views.login_user, name='login_user'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('recovery/', views.recovery, name='recovery'),
    
    # For Test
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
    # For User Page
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('settings/', views.settings, name='settings'),
    
    # Logout
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout/success/', LogoutView.as_view(template_name='logout_success.html'), name='logout_success'),
    


    # For Specialization
    path('specialization_page/<int:item_id>/', views.specialization_page, name='specialization_page'),
]


