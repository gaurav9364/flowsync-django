from django.urls import path
from .views import project_list, create_project, delete_project

from .views import project_api
from django.urls import path


from .views import (
    project_list,
    create_project,
    delete_project,
    team_list,
    create_team,
    delete_team,
    edit_team,
    edit_project,
)

urlpatterns = [
    path('', project_list, name='project_list'),
    path('create/', create_project, name='create_project'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),

    path('teams/', team_list, name='team_list'),
    path('teams/create/', create_team, name='create_team'),
    path('teams/delete/<int:pk>/', delete_team, name='delete_team'),
    path('teams/edit/<int:pk>/', edit_team, name='edit_team'),
    path('edit/<int:pk>/', edit_project, name='edit_project'),
]