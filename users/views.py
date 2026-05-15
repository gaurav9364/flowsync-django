from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .forms import SignupForm, ProfileForm
from tasks.models import Task
from projects.models import Project

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .models import ActivityLog



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

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'users/home.html')


@login_required
def profile_view(request):
    form = ProfileForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            profile = form.save(commit=False)
            profile.updated_by = request.user.username
            profile.save()

            return redirect('profile')

    return render(request, 'users/profile.html', {
        'form': form
    })

@login_required
def notification_view(request):
    notifications = request.user.notifications.all().order_by(
        '-created_at'
    )

    notifications.update(is_read=True)

    return render(request, 'users/notifications.html', {
        'notifications': notifications
    })

@login_required
def activity_view(request):
    if request.user.is_superuser or request.user.role == 'admin':
        activities = ActivityLog.objects.all().order_by(
            '-created_at'
        )
    else:
        activities = request.user.activities.all().order_by(
            '-created_at'
        )

    return render(request, 'users/activity.html', {
        'activities': activities
    })