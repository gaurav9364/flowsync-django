from django.urls import path
from .views import project_list, create_project, delete_project

urlpatterns = [
    path('', project_list, name='project_list'),
    path('create/', create_project, name='create_project'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),
]