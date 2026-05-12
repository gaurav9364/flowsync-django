from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignupForm


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


@login_required
def dashboard_view(request):
    total_projects = request.user.assigned_projects.count()

    context = {
        'total_projects': total_projects
    }

    return render(request, 'users/dashboard.html', context)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    return redirect('login')