from django.urls import path
from .views import task_list, create_task, update_task_status, delete_task

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('update/<int:pk>/', update_task_status, name='update_task_status'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
]