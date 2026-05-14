from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .forms import SignupForm
from tasks.models import Task
from projects.models import Project

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'users/signup.html', context)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.is_superuser or request.user.role == 'admin':
        total_projects = Project.objects.count()
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(
            status='completed'
        ).count()

        overdue_tasks = Task.objects.filter(
            due_date__lt=now().date()
        ).exclude(
            status='completed'
        ).count()

    else:
        total_projects = request.user.assigned_projects.count()
        total_tasks = request.user.tasks.count()

        completed_tasks = request.user.tasks.filter(
            status='completed'
        ).count()

        overdue_tasks = request.user.tasks.filter(
            due_date__lt=now().date()
        ).exclude(
            status='completed'
        ).count()

    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
    }

    return render(
        request,
        'users/dashboard.html',
        context
    )

@api_view(['GET'])
def user_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)