from django.urls import path
from . import views


urlpatterns = [
    # For job
    path('job_list/', views.job_list, name='job_list'),
    path('job_list/field:<int:field_id>/', views.job_list, name='job_list_with_field'),
    path('job_list/job:<int:job_id>/', views.job_list, name='job_list_with_detail'),
    path('job_list/field:<int:field_id>/job:<int:job_id>/', views.job_list, name='job_list_with_field_and_detail'),
    #path('job_detail/<int:job_id>/', views.job_detail, name='job_detail'),
]

