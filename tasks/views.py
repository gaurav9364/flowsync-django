from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Task
from .forms import TaskForm


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

    context = {
        'form': form
    }

    return render(request, 'tasks/create_task.html', context)


@login_required
def update_task_status(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.user != task.assigned_to and not (
    request.user.is_superuser or request.user.role == 'admin'
):
        return redirect('task_list')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()

    return redirect('task_list')


@login_required
def delete_task(request, pk):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('task_list')

    task = get_object_or_404(Task, id=pk)
    task.delete()

    return redirect('task_list')