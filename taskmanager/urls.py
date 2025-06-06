from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('edit/<int:task_id>/',views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('complete/<int:task_id>/', views.task_complete, name='task_complete'),
    path('start_of_day/',views.start_of_day, name='start_of_day'),
    path('template_task_edit/<int:task_id>/',views.template_task_edit, name='template_task_edit'),
    path('template_task_delete/<int:task_id>/',views.template_task_delete, name='template_task_delete'),
    path('report/create/', views.report_create, name='report_create'),
    path('report/list/', views.report_list, name='report_list'),
    path('report/delete/<int:report_id>', views.report_delete, name='report_delete'),
    path('report/edit/<int:report_id>', views.report_edit, name='report_edit'),
]