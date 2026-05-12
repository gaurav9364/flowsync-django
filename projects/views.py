from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


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