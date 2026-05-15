from django.urls import path
from .views import (
    task_list,
    create_task,
    edit_task,
    task_detail,
    delete_task,
    task_api,
    export_tasks_csv,
)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('edit/<int:pk>/', edit_task, name='edit_task'),
    path('detail/<int:pk>/', task_detail, name='task_detail'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
    path('api/', task_api, name='task_api'),
    path(
        'export/csv/',
        export_tasks_csv,
        name='export_tasks_csv'
    ),
]