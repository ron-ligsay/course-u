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
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name='login_user'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('recovery/', views.recovery, name='recovery'),
    path('test/<int:pk>/', views.test, name='test'),
    path('next_test/<int:pk>/', views.next_test, name='next_test'),
    path('prev_test/<int:pk>/', views.prev_test, name='prev_test'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout/success/', LogoutView.as_view(template_name='logout_success.html'), name='logout_success'),
    path('test_home/', views.test_home, name='test_home'),
    path('view_test_results/', views.view_test_results, name='view_test_results'),
]


