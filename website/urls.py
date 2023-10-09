
from django.urls import path, include
import debug_toolbar
from . import views
from django.contrib.auth.views import LogoutView
# import datetime and timezone
from datetime import datetime
from django.utils import timezone

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('field/', views.home_field, name='home_field'),
    path('field/<int:field_id>/', views.home_field, name='home_field'),

    # For Authentication
    path('login_user/', views.login_user, name='login_user'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('recovery/', views.recovery, name='recovery'),
   
    # For User Page
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('settings/', views.settings, name='settings'),
    
    # Logout
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout/success/', LogoutView.as_view(template_name='user/logout_success.html'), name='logout_success'),
    
    # For Specialization
    path('specialization_page/<int:item_id>/', views.specialization_page, name='specialization_page'),
]


