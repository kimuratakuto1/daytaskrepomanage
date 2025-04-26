from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('edit/<int:task_id>/',views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('complete/<int:task_id>/', views.task_complete, name='task_complete'),
    path('end_of_day/',views.end_of_day, name='end_of_day'),
    path('start_of_day/',views.start_of_day, name='start_of_day'),
    path('template_task_edit/<int:task_id>/',views.template_task_edit, name='template_task_edit'),
    path('template_task_delete/<int:task_id>/',views.template_task_delete, name='template_task_delete'),
]