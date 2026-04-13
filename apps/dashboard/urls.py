from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('evaluation/<int:evaluation_id>/', views.take_evaluation, name='take_evaluation'),
    path('admin/create-course/', views.admin_create_course, name='admin_create_course'),
]
