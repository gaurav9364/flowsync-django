from django.urls import path
from .views import project_list, create_project, delete_project

from .views import project_api

urlpatterns = [
    path('', project_list, name='project_list'),
    path('create/', create_project, name='create_project'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),

    path('api/', project_api, name='project_api'),
]