from django.urls import path
from . import views

urlpatterns = [
    path('recommender/', views.recommender, name='recommender'),
    path('recommendation/<int:field_id>/', views.recommendation_field, name='recommendation_field'),
    path('specialization/<int:field_id>/', views.recommendation_specialization, name='recommendation_specialization'),
    path('course/<int:field_id>/', views.recommendation_course, name='recommendation_course'),

    # path('recommendation/jobs/<int:field_id>/', views.recommendation_jobs, name='recommendation_jobs'),
    # path('recommendation/jobs/<int:field_id>/<int:job_id>/', views.recommendation_jobs, name='recommendation_jobs_with_details')

]