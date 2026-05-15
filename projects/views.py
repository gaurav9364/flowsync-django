from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer

from .models import Team
from .forms import TeamForm


@login_required
def project_list(request):
    if request.user.is_superuser or request.user.role == 'admin':
        projects = Project.objects.all()
    else:
        projects = request.user.assigned_projects.all()

    context = {
        'projects': projects
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def create_project(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('project_list')

    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()
            return redirect('project_list')

    context = {
        'form': form
    }
    return render(request, 'projects/create_project.html', context)


@login_required
def delete_project(request, pk):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('project_list')

    project = get_object_or_404(Project, id=pk)
    project.delete()
    return redirect('project_list')

@api_view(['GET'])
def project_api(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@login_required
def team_list(request):
    if request.user.is_superuser or request.user.role == 'admin':
        teams = Team.objects.all()
    else:
        teams = request.user.teams.all()

    return render(request, 'projects/team_list.html', {
        'teams': teams
    })


@login_required
def create_team(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('team_list')

    form = TeamForm()

    if request.method == 'POST':
        form = TeamForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            form.save_m2m()
            return redirect('team_list')

    return render(request, 'projects/create_team.html', {
        'form': form
    })


@login_required
def delete_team(request, pk):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('team_list')

    team = get_object_or_404(Team, id=pk)
    team.delete()

    return redirect('team_list')