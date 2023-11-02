
from django.urls import path
from . import views


urlpatterns = [
    path('mbti/initialize/', views.initialize_mbti_test, name='initialize_mbti_test'),
    path('mbti/', views.mbti_test, name='mbti_test'),
    path('mbti/<int:mbti_set_id>/', views.mbti_test, name='mbti_test'),
    path('mbti/results/', views.mbti_results, name='mbti_results'),
    path('mbti/results/<int:mbti_set_id>/', views.mbti_results, name='mbti_results'),
]