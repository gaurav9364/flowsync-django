from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .forms import TaskForm, SolutionUploadForm
from .serializers import TaskSerializer


@login_required
def task_list(request):
    if request.user.is_superuser or request.user.role == 'admin':
        tasks = Task.objects.all()
    else:
        tasks = request.user.tasks.all()

    context = {
        'tasks': tasks,
        'today': now().date()
    }

    return render(request, 'tasks/task_list.html', context)


@login_required
def create_task(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('task_list')

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')

    return render(request, 'tasks/create_task.html', {
        'form': form
    })


@login_required
def edit_task(request, pk):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('task_list')

    task = get_object_or_404(Task, id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {
        'form': form
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.user != task.assigned_to and not (
        request.user.is_superuser or request.user.role == 'admin'
    ):
        return redirect('task_list')

    form = SolutionUploadForm(instance=task)

    if request.method == 'POST':
        form = SolutionUploadForm(
            request.POST,
            request.FILES,
            instance=task
        )

        if form.is_valid():
            task = form.save(commit=False)
            task.submitted_at = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.id)

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'form': form
    })


@login_required
def delete_task(request, pk):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('task_list')

    task = get_object_or_404(Task, id=pk)
    task.delete()

    return redirect('task_list')


@api_view(['GET'])
def task_api(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)